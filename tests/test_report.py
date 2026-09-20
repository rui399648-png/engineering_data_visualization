from pathlib import Path

from report import generate_report


def test_generate_report_writes_metrics_facts_and_relative_chart_links(tmp_path):
    metrics = {
        "date_range": "2026-01-05 至 2026-06-07",
        "total_cost": 1234567.89,
        "top_material": "钢筋",
        "top_material_cost": 300000.0,
        "top_building": "3#楼",
        "top_building_cost": 500000.0,
        "peak_cost_month": "2026-06",
        "peak_month_cost": 250000.0,
        "usage_peak_month": "2026-06",
        "usage_peak_quantity": 50.0,
        "usage_unit": "吨",
        "top_five_share_percent": 82.5,
    }
    chart_paths = {
        key: tmp_path / "charts" / filename
        for key, filename in {
            "material_cost_ranking": "material_cost_ranking.png",
            "building_cost_comparison": "building_cost_comparison.png",
            "monthly_cost_trend": "monthly_cost_trend.png",
            "top_material_usage_trend": "top_material_usage_trend.png",
            "cost_share": "cost_share.png",
        }.items()
    }
    output_path = tmp_path / "analysis_report.md"

    result = generate_report(metrics, chart_paths, output_path)
    content = output_path.read_text(encoding="utf-8")

    assert result == output_path
    assert "1,234,567.89" in content
    assert "成本最高的材料是 **钢筋**" in content
    assert "成本最高的楼栋是 **3#楼**" in content
    for path in chart_paths.values():
        assert f"charts/{path.name}" in content
