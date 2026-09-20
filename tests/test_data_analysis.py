import pandas as pd
import pytest

from data_analysis import (
    calculate_key_metrics,
    get_top_material_usage_trend,
    load_data,
    summarize_building_costs,
    summarize_cost_share,
    summarize_material_costs,
    summarize_monthly_costs,
)


REQUIRED_COLUMNS = [
    "项目", "楼栋", "材料", "数量", "单位", "单价", "采购日期", "供应商", "总成本"
]


def valid_row(**changes):
    row = {
        "项目": "示例工程",
        "楼栋": "1#楼",
        "材料": "钢筋",
        "数量": 10,
        "单位": "吨",
        "单价": 4000,
        "采购日期": "2026-01-05",
        "供应商": "示例供应商",
        "总成本": 40000,
    }
    row.update(changes)
    return row


def write_csv(tmp_path, rows):
    path = tmp_path / "input.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def test_load_data_converts_numbers_and_dates(tmp_path):
    result = load_data(write_csv(tmp_path, [valid_row(数量="10", 单价="4000")]))

    assert result.columns.tolist() == REQUIRED_COLUMNS
    assert pd.api.types.is_numeric_dtype(result["数量"])
    assert pd.api.types.is_numeric_dtype(result["单价"])
    assert pd.api.types.is_numeric_dtype(result["总成本"])
    assert pd.api.types.is_datetime64_any_dtype(result["采购日期"])


def test_load_data_reports_all_missing_columns(tmp_path):
    path = tmp_path / "missing.csv"
    pd.DataFrame({"项目": ["示例工程"]}).to_csv(path, index=False)

    with pytest.raises(ValueError, match="缺少列") as error:
        load_data(path)

    assert "数量" in str(error.value)
    assert "总成本" in str(error.value)


def test_load_data_rejects_empty_csv(tmp_path):
    path = tmp_path / "empty.csv"
    pd.DataFrame(columns=REQUIRED_COLUMNS).to_csv(path, index=False)

    with pytest.raises(ValueError, match="没有数据"):
        load_data(path)


@pytest.mark.parametrize("column", ["数量", "单价", "总成本"])
def test_load_data_rejects_invalid_numbers(tmp_path, column):
    with pytest.raises(ValueError):
        load_data(write_csv(tmp_path, [valid_row(**{column: "未知"})]))


def test_load_data_rejects_invalid_dates(tmp_path):
    with pytest.raises(ValueError):
        load_data(write_csv(tmp_path, [valid_row(采购日期="不是日期")]))


def sample_data():
    return pd.DataFrame(
        [
            valid_row(楼栋="1#楼", 材料="钢筋", 数量=10, 总成本=100),
            valid_row(楼栋="2#楼", 材料="水泥", 数量=20, 单位="吨", 总成本=300,
                      采购日期="2026-02-05"),
            valid_row(楼栋="1#楼", 材料="钢筋", 数量=15, 总成本=250,
                      采购日期="2026-02-10"),
        ]
    ).assign(采购日期=lambda frame: pd.to_datetime(frame["采购日期"]))


def test_summary_functions_group_and_sort_without_changing_source():
    data = sample_data()
    original_columns = data.columns.tolist()

    assert summarize_material_costs(data).to_dict("records") == [
        {"材料": "钢筋", "总成本": 350},
        {"材料": "水泥", "总成本": 300},
    ]
    assert summarize_building_costs(data).to_dict("records") == [
        {"楼栋": "1#楼", "总成本": 350},
        {"楼栋": "2#楼", "总成本": 300},
    ]
    assert summarize_monthly_costs(data).to_dict("records") == [
        {"月份": "2026-01", "总成本": 100},
        {"月份": "2026-02", "总成本": 550},
    ]
    assert data.columns.tolist() == original_columns


def test_top_material_usage_trend_returns_material_unit_and_monthly_quantity():
    material, unit, trend = get_top_material_usage_trend(sample_data())

    assert material == "钢筋"
    assert unit == "吨"
    assert trend.to_dict("records") == [
        {"月份": "2026-01", "数量": 10},
        {"月份": "2026-02", "数量": 15},
    ]


def test_top_material_usage_trend_rejects_mixed_units():
    data = sample_data()
    data.loc[2, "单位"] = "千克"

    with pytest.raises(ValueError, match="多个单位"):
        get_top_material_usage_trend(data)


def test_cost_share_keeps_top_five_and_preserves_total():
    data = pd.DataFrame(
        {"材料": list("ABCDEFG"), "总成本": [70, 60, 50, 40, 30, 20, 10]}
    )
    result = summarize_cost_share(data)

    assert result["材料"].tolist() == ["A", "B", "C", "D", "E", "其他"]
    assert result.iloc[-1]["总成本"] == 30
    assert result["总成本"].sum() == data["总成本"].sum()


def test_key_metrics_has_complete_stable_contract():
    metrics = calculate_key_metrics(sample_data())

    assert set(metrics) == {
        "date_range", "total_cost", "top_material", "top_material_cost",
        "top_building", "top_building_cost", "peak_cost_month",
        "peak_month_cost", "usage_peak_month", "usage_peak_quantity",
        "usage_unit", "top_five_share_percent",
    }
    assert metrics["date_range"] == "2026-01-05 至 2026-02-10"
    assert metrics["total_cost"] == 650.0
    assert metrics["top_material"] == "钢筋"
    assert metrics["peak_cost_month"] == "2026-02"
    assert metrics["top_five_share_percent"] == 100.0
