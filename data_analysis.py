"""工程成本数据加载、校验与统计。"""

import pandas as pd


REQUIRED_COLUMNS = {
    "项目",
    "楼栋",
    "材料",
    "数量",
    "单位",
    "单价",
    "采购日期",
    "供应商",
    "总成本",
}
NUMBER_COLUMNS = ["数量", "单价", "总成本"]


def load_data(file_path):
    data = pd.read_csv(file_path)
    missing_columns = sorted(REQUIRED_COLUMNS - set(data.columns))

    if missing_columns:
        raise ValueError(f"缺少列: {missing_columns}")
    if data.empty:
        raise ValueError("CSV 没有数据")

    for column in NUMBER_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="raise")

    data["采购日期"] = pd.to_datetime(data["采购日期"], errors="raise")
    return data


def summarize_material_costs(data):
    return (
        data.groupby("材料", as_index=False)["总成本"]
        .sum()
        .sort_values("总成本", ascending=False)
        .reset_index(drop=True)
    )


def summarize_building_costs(data):
    return (
        data.groupby("楼栋", as_index=False)["总成本"]
        .sum()
        .sort_values("总成本", ascending=False)
        .reset_index(drop=True)
    )


def summarize_monthly_costs(data):
    monthly_data = data.copy()
    monthly_data["月份"] = monthly_data["采购日期"].dt.to_period("M").astype(str)

    return (
        monthly_data.groupby("月份", as_index=False)["总成本"]
        .sum()
        .sort_values("月份")
        .reset_index(drop=True)
    )


def get_top_material_usage_trend(data):
    top_material = summarize_material_costs(data).iloc[0]["材料"]
    material_data = data.loc[data["材料"] == top_material].copy()
    units = material_data["单位"].dropna().unique()

    if len(units) != 1:
        raise ValueError(f"{top_material}存在多个单位，无法汇总用量")

    unit = str(units[0])
    material_data["月份"] = material_data["采购日期"].dt.to_period("M").astype(str)
    trend_data = (
        material_data.groupby("月份", as_index=False)["数量"]
        .sum()
        .sort_values("月份")
        .reset_index(drop=True)
    )
    return top_material, unit, trend_data


def summarize_cost_share(data):
    ranking = summarize_material_costs(data)
    top_five = ranking.head(5).copy()
    other_cost = ranking.iloc[5:]["总成本"].sum()

    if other_cost > 0:
        other = pd.DataFrame([{"材料": "其他", "总成本": other_cost}])
        return pd.concat([top_five, other], ignore_index=True)

    return top_five.reset_index(drop=True)


def calculate_key_metrics(data):
    material_summary = summarize_material_costs(data)
    building_summary = summarize_building_costs(data)
    monthly_summary = summarize_monthly_costs(data)

    top_material_row = material_summary.iloc[0]
    top_building_row = building_summary.iloc[0]
    total_cost = float(data["总成本"].sum())

    peak_month_row = monthly_summary.loc[monthly_summary["总成本"].idxmax()]
    _, usage_unit, usage_trend = get_top_material_usage_trend(data)
    usage_peak_row = usage_trend.loc[usage_trend["数量"].idxmax()]
    top_five_cost = float(material_summary.head(5)["总成本"].sum())

    return {
        "date_range": (
            f"{data['采购日期'].min():%Y-%m-%d} 至 "
            f"{data['采购日期'].max():%Y-%m-%d}"
        ),
        "total_cost": total_cost,
        "top_material": str(top_material_row["材料"]),
        "top_material_cost": float(top_material_row["总成本"]),
        "top_building": str(top_building_row["楼栋"]),
        "top_building_cost": float(top_building_row["总成本"]),
        "peak_cost_month": str(peak_month_row["月份"]),
        "peak_month_cost": float(peak_month_row["总成本"]),
        "usage_peak_month": str(usage_peak_row["月份"]),
        "usage_peak_quantity": float(usage_peak_row["数量"]),
        "usage_unit": usage_unit,
        "top_five_share_percent": round(top_five_cost / total_cost * 100, 2),
    }
