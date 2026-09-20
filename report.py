"""工程成本 Markdown 报告生成。"""

from pathlib import Path


def generate_report(metrics, chart_paths, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    def chart_link(key):
        return f"charts/{chart_paths[key].name}"

    content = f"""# 工程材料成本分析报告

数据范围：{metrics['date_range']}

## 关键指标

- 总成本：**{metrics['total_cost']:,.2f} 元**
- 成本最高材料：**{metrics['top_material']}**（{metrics['top_material_cost']:,.2f} 元）
- 成本最高楼栋：**{metrics['top_building']}**（{metrics['top_building_cost']:,.2f} 元）
- 成本峰值月份：**{metrics['peak_cost_month']}**（{metrics['peak_month_cost']:,.2f} 元）

## 1. 材料总成本排名

![材料总成本排名]({chart_link('material_cost_ranking')})

事实：成本最高的材料是 **{metrics['top_material']}**，总成本为 **{metrics['top_material_cost']:,.2f} 元**。

## 2. 各楼栋总成本对比

![各楼栋总成本对比]({chart_link('building_cost_comparison')})

事实：成本最高的楼栋是 **{metrics['top_building']}**，总成本为 **{metrics['top_building_cost']:,.2f} 元**。

## 3. 月度总成本趋势

![月度总成本趋势]({chart_link('monthly_cost_trend')})

事实：月度总成本峰值出现在 **{metrics['peak_cost_month']}**，金额为 **{metrics['peak_month_cost']:,.2f} 元**。

## 4. 最高成本材料月度用量趋势

![最高成本材料月度用量趋势]({chart_link('top_material_usage_trend')})

事实：该材料用量峰值出现在 **{metrics['usage_peak_month']}**，数量为 **{metrics['usage_peak_quantity']:,.2f} {metrics['usage_unit']}**。

## 5. 材料成本占比

![材料成本占比]({chart_link('cost_share')})

事实：成本最高的前五类材料合计占总成本的 **{metrics['top_five_share_percent']:.2f}%**。

> 本报告使用公开学习用模拟数据，只陈述统计结果，不代表真实工程采购记录或业务建议。
"""

    output_path.write_text(content, encoding="utf-8")
    return output_path
