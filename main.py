"""工程数据可视化项目命令行入口。"""

import argparse
from pathlib import Path
import sys

import pandas as pd

from charts import (
    plot_building_cost_comparison,
    plot_cost_share,
    plot_material_cost_ranking,
    plot_monthly_cost_trend,
    plot_top_material_usage_trend,
)
from data_analysis import (
    calculate_key_metrics,
    get_top_material_usage_trend,
    load_data,
    summarize_building_costs,
    summarize_cost_share,
    summarize_material_costs,
    summarize_monthly_costs,
)
from report import generate_report


def run_pipeline(input_path, output_dir):
    output_dir = Path(output_dir)
    charts_dir = output_dir / "charts"
    report_path = output_dir / "analysis_report.md"

    data = load_data(input_path)

    material_summary = summarize_material_costs(data)
    building_summary = summarize_building_costs(data)
    monthly_summary = summarize_monthly_costs(data)
    material, unit, usage_summary = get_top_material_usage_trend(data)
    share_summary = summarize_cost_share(data)
    metrics = calculate_key_metrics(data)

    chart_paths = {
        "material_cost_ranking": plot_material_cost_ranking(
            material_summary,
            charts_dir / "material_cost_ranking.png",
        ),
        "building_cost_comparison": plot_building_cost_comparison(
            building_summary,
            charts_dir / "building_cost_comparison.png",
        ),
        "monthly_cost_trend": plot_monthly_cost_trend(
            monthly_summary,
            charts_dir / "monthly_cost_trend.png",
        ),
        "top_material_usage_trend": plot_top_material_usage_trend(
            material,
            unit,
            usage_summary,
            charts_dir / "top_material_usage_trend.png",
        ),
        "cost_share": plot_cost_share(
            share_summary,
            charts_dir / "cost_share.png",
        ),
    }

    report = generate_report(metrics, chart_paths, report_path)

    return {
        "charts": chart_paths,
        "report": report,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="生成工程材料成本图表和 Markdown 报告"
    )
    parser.add_argument("--input", help="输入 CSV 路径")
    parser.add_argument("--output-dir", help="输出目录")
    return parser.parse_args(argv)

def resolve_paths(args):
    project_dir = Path(__file__).resolve().parent

    if args.input:
        input_path = Path(args.input).resolve()
    else:
        input_path = project_dir / "data" / "engineering_costs.csv"

    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
    else:
        output_dir = project_dir / "output"

    charts_dir = output_dir / "charts"
    report_path = output_dir / "analysis_report.md"

    return input_path, charts_dir, report_path


def main(argv=None):
    args = parse_args(argv)
    input_path, charts_dir, report_path = resolve_paths(args)

    try:
        outputs = run_pipeline(input_path, report_path.parent)
    except (
        OSError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        ValueError,
    ) as error:
        print(f"处理失败：{error}", file=sys.stderr)
        return 1

    print(f"已生成 {len(outputs['charts'])} 张图表：{charts_dir}")
    print(f"已生成分析报告：{outputs['report']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
