"""工程成本图表生成。"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


FONT_CANDIDATES = (
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Arial Unicode MS",
)


def configure_chinese_font():
    """选择当前电脑上第一个可用的常见中文字体。"""
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}

    for font_name in FONT_CANDIDATES:
        if font_name in available_fonts:
            plt.rcParams["font.sans-serif"] = [font_name]
            plt.rcParams["axes.unicode_minus"] = False
            return font_name

    warnings.warn(
        "未找到常用中文字体，图表中的中文可能无法正常显示。",
        stacklevel=2,
    )
    return None


def plot_material_cost_ranking(summary, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_chinese_font()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(summary["材料"], summary["总成本"])
    ax.bar_label(
        bars,
        labels=[f"{value:,.0f}" for value in summary["总成本"]],
        padding=3,
    )
    ax.invert_yaxis()
    ax.set_title("材料总成本排名")
    ax.set_xlabel("总成本(元)")
    ax.set_ylabel("材料")
    ax.margins(x=0.15)

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_building_cost_comparison(summary, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_chinese_font()

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(summary["楼栋"], summary["总成本"])
    ax.bar_label(
        bars,
        labels=[f"{value:,.0f}" for value in summary["总成本"]],
        padding=3,
    )
    ax.set_title("楼栋总成本对比")
    ax.set_xlabel("楼栋")
    ax.set_ylabel("总成本(元)")
    ax.margins(y=0.15)

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_monthly_cost_trend(summary, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_chinese_font()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(summary["月份"], summary["总成本"], marker="o", linewidth=2)
    ax.set_title("月度总成本趋势")
    ax.set_xlabel("月份")
    ax.set_ylabel("总成本（元）")
    ax.grid(axis="y", alpha=0.25)
    ax.margins(y=0.15)

    for month, value in zip(summary["月份"], summary["总成本"]):
        ax.annotate(
            f"{value:,.0f}",
            (month, value),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
        )

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_top_material_usage_trend(material, unit, summary, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_chinese_font()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        summary["月份"],
        summary["数量"],
        marker="o",
        linewidth=2,
        color="#F28E2B",
    )
    ax.set_title(f"{material}月度用量趋势")
    ax.set_xlabel("月份")
    ax.set_ylabel(f"数量({unit})")
    ax.grid(axis="y", alpha=0.25)
    ax.margins(y=0.15)

    for month, value in zip(summary["月份"], summary["数量"]):
        ax.annotate(
            f"{value:,.2f}",
            (month, value),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
        )

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path


def plot_cost_share(summary, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_chinese_font()

    colors = ["#4C78A8", "#F28E2B", "#59A14F", "#E15759", "#76B7B2", "#BAB0AC"]
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.pie(
        summary["总成本"],
        labels=summary["材料"],
        autopct="%1.1f%%",
        startangle=90,
        colors=colors[: len(summary)],
    )
    ax.set_title("材料成本占比（前五类与其他）")
    ax.axis("equal")

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return output_path
