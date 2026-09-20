# Engineering Data Visualization

一个使用 Pandas 与 Matplotlib 完成工程材料成本分析的 Python 学习项目。程序读取 CSV，自动生成 5 张图表和一份 Markdown 分析报告。

## 功能

- 校验必需字段，并转换数值与日期类型
- 统计材料、楼栋和月份的总成本
- 分析最高成本材料的月度用量
- 计算前五类材料的成本占比
- 生成柱状图、折线图和饼图
- 输出带关键指标和图表链接的 Markdown 报告
- 支持默认路径和自定义命令行参数

## 项目结构

```text
03_engineering_data_visualization/
├─ data/
│  └─ engineering_costs.csv       # 学习用模拟数据
├─ tests/                          # 自动化测试
├─ charts.py                       # 图表生成
├─ data_analysis.py                # 加载、校验与统计
├─ report.py                       # Markdown 报告生成
├─ main.py                         # 程序入口与流程编排
├─ requirements.txt
└─ README.md
```

程序的核心流程是：

```text
CSV → load_data → 汇总统计 → 绘制图表 → 计算指标 → 生成报告
```

## 环境准备

推荐使用 64 位 Python 3.13。

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 运行

使用项目自带的数据和默认输出目录：

```powershell
.\.venv\Scripts\python.exe main.py
```

指定输入文件和输出目录：

```powershell
.\.venv\Scripts\python.exe main.py --input data/engineering_costs.csv --output-dir output
```

成功运行后会生成：

```text
output/
├─ charts/
│  ├─ material_cost_ranking.png
│  ├─ building_cost_comparison.png
│  ├─ monthly_cost_trend.png
│  ├─ top_material_usage_trend.png
│  └─ cost_share.png
└─ analysis_report.md
```

## 测试

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

测试覆盖输入校验、统计结果、混合单位保护、5 个图表函数、报告内容和完整运行流程。

## 重要数据规则

- CSV 必须包含：项目、楼栋、材料、数量、单位、单价、采购日期、供应商、总成本。
- 数量、单价和总成本必须能转换为数字。
- 采购日期必须是有效日期。
- 同一种材料只有在单位一致时才能汇总用量；例如“吨”和“千克”不能直接相加。
- 中文字体会按“微软雅黑、黑体、Noto Sans CJK、Arial Unicode MS”的顺序自动选择。

## 学习要点

本项目练习了 DataFrame、`groupby`、`sum`、`sort_values`、日期处理、Matplotlib 面向对象绘图、`pathlib.Path`、命令行参数、异常处理和 pytest。

## 数据声明

`data/engineering_costs.csv` 是公开学习用的确定性模拟数据，不代表真实工程采购记录。

## License

MIT
