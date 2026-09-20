from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import pandas as pd
import pytest

import charts
from charts import (
    configure_chinese_font,
    plot_building_cost_comparison,
    plot_cost_share,
    plot_material_cost_ranking,
    plot_monthly_cost_trend,
    plot_top_material_usage_trend,
)


def assert_nonempty_png(path):
    assert path.exists()
    assert path.suffix == ".png"
    assert path.stat().st_size > 0


def test_configure_chinese_font_uses_first_available_candidate(monkeypatch):
    fonts = [SimpleNamespace(name="SimHei"), SimpleNamespace(name="Microsoft YaHei")]
    monkeypatch.setattr(charts.font_manager.fontManager, "ttflist", fonts)

    assert configure_chinese_font() == "Microsoft YaHei"
    assert matplotlib.rcParams["font.sans-serif"][0] == "Microsoft YaHei"


@pytest.mark.parametrize(
    ("plotter", "summary"),
    [
        (plot_material_cost_ranking,
         pd.DataFrame({"材料": ["钢筋", "水泥"], "总成本": [120000, 80000]})),
        (plot_building_cost_comparison,
         pd.DataFrame({"楼栋": ["1#楼", "2#楼"], "总成本": [120000, 80000]})),
        (plot_monthly_cost_trend,
         pd.DataFrame({"月份": ["2026-01", "2026-02"], "总成本": [80000, 120000]})),
        (plot_cost_share,
         pd.DataFrame({"材料": ["钢筋", "其他"], "总成本": [120000, 80000]})),
    ],
)
def test_standard_chart_functions_write_nonempty_png(tmp_path, plotter, summary):
    output_path = tmp_path / "nested" / f"{plotter.__name__}.png"

    assert plotter(summary, output_path) == output_path
    assert_nonempty_png(output_path)


def test_usage_chart_writes_nonempty_png(tmp_path):
    summary = pd.DataFrame({"月份": ["2026-01", "2026-02"], "数量": [10, 15]})
    output_path = tmp_path / "charts" / "usage.png"

    result = plot_top_material_usage_trend("钢筋", "吨", summary, output_path)

    assert result == output_path
    assert_nonempty_png(output_path)
