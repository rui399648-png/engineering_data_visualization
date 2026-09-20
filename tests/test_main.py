from argparse import Namespace

import pandas as pd

from main import main, resolve_paths, run_pipeline


def make_input(tmp_path):
    path = tmp_path / "input.csv"
    pd.DataFrame(
        {
            "项目": ["示例工程", "示例工程"],
            "楼栋": ["1#楼", "2#楼"],
            "材料": ["钢筋", "水泥"],
            "数量": [10, 20],
            "单位": ["吨", "吨"],
            "单价": [4000, 500],
            "采购日期": ["2026-01-05", "2026-02-05"],
            "供应商": ["甲", "乙"],
            "总成本": [40000, 10000],
        }
    ).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def test_resolve_paths_uses_custom_absolute_paths(tmp_path):
    input_path = tmp_path / "input.csv"
    output_dir = tmp_path / "result"

    resolved_input, charts_dir, report_path = resolve_paths(
        Namespace(input=str(input_path), output_dir=str(output_dir))
    )

    assert resolved_input == input_path.resolve()
    assert charts_dir == output_dir.resolve() / "charts"
    assert report_path == output_dir.resolve() / "analysis_report.md"


def test_run_pipeline_creates_five_charts_and_report(tmp_path):
    outputs = run_pipeline(make_input(tmp_path), tmp_path / "output")

    assert len(outputs["charts"]) == 5
    assert all(path.exists() and path.stat().st_size > 0 for path in outputs["charts"].values())
    assert outputs["report"].exists()
    assert outputs["report"].read_text(encoding="utf-8").count("![") == 5


def test_main_returns_failure_for_missing_input(tmp_path, capsys):
    result = main([
        "--input", str(tmp_path / "missing.csv"),
        "--output-dir", str(tmp_path / "output"),
    ])

    assert result == 1
    assert "处理失败" in capsys.readouterr().err
