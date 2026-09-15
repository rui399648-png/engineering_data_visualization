from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "engineering_costs.csv"


def test_sample_data_is_complete_and_deterministic():
    data = pd.read_csv(DATA_PATH)

    assert data.shape == (180, 9)
    assert list(data.columns) == [
        "项目",
        "楼栋",
        "材料",
        "数量",
        "单位",
        "单价",
        "采购日期",
        "供应商",
        "总成本",
    ]
    assert data.isna().sum().sum() == 0
    assert data["楼栋"].nunique() == 3
    assert data["材料"].nunique() == 10
    assert pd.to_datetime(data["采购日期"]).dt.to_period("M").nunique() == 6
    expected_cost = (data["数量"] * data["单价"]).round(2)
    assert data["总成本"].round(2).equals(expected_cost)

