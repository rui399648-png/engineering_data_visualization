# Engineering Data Visualization

这是一个使用 Pandas 和 Matplotlib 学习工程数据统计与可视化的 Python 项目。完成后，程序会把工程材料成本 CSV 转换为 5 张 PNG 图表和一份 Markdown 分析报告。

## 当前状态

项目处于学习开发阶段。目前只准备了项目骨架和样例数据，核心统计、绘图、报告和命令行功能将按照测试驱动方式逐步实现。

## 数据声明

`data/engineering_costs.csv` 是公开学习用确定性模拟数据，不代表真实工程采购记录。

## 推荐环境

- Python 3.13（64 位）
- NumPy
- Pandas
- Matplotlib
- pytest

## 创建环境

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 当前测试

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_sample_data.py -v
```

## 学习顺序

```text
NumPy 基础
→ 加载和验证 CSV
→ 材料成本统计与横向柱状图
→ 楼栋成本统计与柱状图
→ 月度成本统计与折线图
→ 最高成本材料用量趋势
→ 成本占比饼图
→ Markdown 报告
→ CLI、完整测试和 GitHub 发布
```

## License

MIT

