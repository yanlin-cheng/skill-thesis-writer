#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计表格生成器
生成符合学术规范的统计结果表格（Markdown格式）
支持：描述性统计、相关分析、回归分析、方差分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from scipy import stats


@dataclass
class TableConfig:
    """表格配置"""
    title: str
    note: str = ""
    decimal_places: int = 2
    show_stars: bool = True
    

class StatTableGenerator:
    """统计表格生成器"""
    
    # 显著性标记
    SIG_MARKS = {
        0.001: "***",
        0.01: "**",
        0.05: "*"
    }
    
    def __init__(self, config: Optional[TableConfig] = None):
        self.config = config or TableConfig(title="统计结果")
    
    def descriptive_stats(self, data: pd.DataFrame, 
                         variables: Optional[List[str]] = None,
                         group_by: Optional[str] = None) -> str:
        """
        生成描述性统计表
        
        Args:
            data: 数据框
            variables: 变量列表，默认全部数值变量
            group_by: 分组变量
            
        Returns:
            str: Markdown格式表格
        """
        if variables is None:
            variables = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if group_by:
            return self._grouped_descriptive(data, variables, group_by)
        
        # 计算描述性统计
        desc = data[variables].describe().T
        desc['偏度'] = data[variables].skew()
        desc['峰度'] = data[variables].kurtosis()
        
        # 构建表格
        rows = []
        rows.append(f"表X {self.config.title}")
        rows.append("")
        rows.append("| 变量 | M | SD | 最小值 | 最大值 | 偏度 | 峰度 |")
        rows.append("|------|------|------|--------|--------|------|------|")
        
        for var in variables:
            if var in desc.index:
                row = desc.loc[var]
                rows.append(
                    f"| {var} | "
                    f"{row['mean']:.{self.config.decimal_places}f} | "
                    f"{row['std']:.{self.config.decimal_places}f} | "
                    f"{row['min']:.{self.config.decimal_places}f} | "
                    f"{row['max']:.{self.config.decimal_places}f} | "
                    f"{row['偏度']:.{self.config.decimal_places}f} | "
                    f"{row['峰度']:.{self.config.decimal_places}f} |"
                )
        
        if self.config.note:
            rows.append("")
            rows.append(f"注：{self.config.note}")
        
        return "\n".join(rows)
    
    def _grouped_descriptive(self, data: pd.DataFrame, 
                            variables: List[str], 
                            group_by: str) -> str:
        """分组描述性统计"""
        groups = data.groupby(group_by)
        
        rows = []
        rows.append(f"表X {self.config.title}")
        rows.append("")
        
        # 表头
        group_names = list(groups.groups.keys())
        header = "| 变量 | " + " | ".join([f"{g} (M±SD)" for g in group_names]) + " |"
        rows.append(header)
        rows.append("|" + "|".join(["------"] * (len(group_names) + 1)) + "|")
        
        # 数据行
        for var in variables:
            row_data = [var]
            for name, group in groups:
                m = group[var].mean()
                sd = group[var].std()
                row_data.append(f"{m:.{self.config.decimal_places}f}±{sd:.{self.config.decimal_places}f}")
            rows.append("| " + " | ".join(row_data) + " |")
        
        if self.config.note:
            rows.append("")
            rows.append(f"注：{self.config.note}")
        
        return "\n".join(rows)
    
    def correlation_matrix(self, data: pd.DataFrame, 
                          variables: Optional[List[str]] = None,
                          method: str = "pearson") -> str:
        """
        生成相关分析矩阵
        
        Args:
            data: 数据框
            variables: 变量列表
            method: 相关方法（pearson/spearman）
            
        Returns:
            str: Markdown格式表格
        """
        if variables is None:
            variables = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # 计算相关系数
        corr = data[variables].corr(method=method)
        
        # 计算p值
        def calculate_pvalues(df):
            cols = df.columns
            p_matrix = np.zeros((len(cols), len(cols)))
            for i, col1 in enumerate(cols):
                for j, col2 in enumerate(cols):
                    if i != j:
                        _, p = stats.pearsonr(df[col1].dropna(), df[col2].dropna())
                        p_matrix[i, j] = p
            return pd.DataFrame(p_matrix, columns=cols, index=cols)
        
        pvalues = calculate_pvalues(data[variables])
        
        # 构建表格
        rows = []
        method_name = "Pearson" if method == "pearson" else "Spearman"
        rows.append(f"表X {variables[0]}等变量的{method_name}相关矩阵")
        rows.append("")
        
        # 表头
        header = "| 变量 | " + " | ".join([f"{i+1}" for i in range(len(variables))]) + " |"
        rows.append(header)
        rows.append("|" + "|".join(["------"] * (len(variables) + 1)) + "|")
        
        # 数据行
        for i, var in enumerate(variables):
            row_data = [f"{i+1}. {var}"]
            for j in range(len(variables)):
                if i == j:
                    row_data.append("1")
                elif j > i:
                    r = corr.iloc[i, j]
                    p = pvalues.iloc[i, j]
                    mark = self._get_sig_mark(p)
                    row_data.append(f"{r:.{self.config.decimal_places}f}{mark}")
                else:
                    row_data.append("")
            rows.append("| " + " | ".join(row_data) + " |")
        
        rows.append("")
        rows.append("注：*p < .05, **p < .01, ***p < .001；对角线为1")
        
        return "\n".join(rows)
    
    def regression_table(self, models: List[Dict], 
                        model_names: Optional[List[str]] = None) -> str:
        """
        生成回归分析表
        
        Args:
            models: 模型结果列表，每个模型包含变量、系数、标准误、t值、p值
            model_names: 模型名称列表
            
        Returns:
            str: Markdown格式表格
        """
        if model_names is None:
            model_names = [f"M{i+1}" for i in range(len(models))]
        
        # 收集所有变量
        all_vars = set()
        for model in models:
            all_vars.update(model.keys())
        all_vars = sorted(all_vars - {'R2', 'Adj_R2', 'F', 'N'})
        
        # 构建表格
        rows = []
        rows.append(f"表X {self.config.title}")
        rows.append("")
        rows.append("| 变量 | " + " | ".join(model_names) + " |")
        rows.append("|" + "|".join(["------"] * (len(models) + 1)) + "|")
        
        # 变量行
        for var in all_vars:
            row_data = [var]
            for model in models:
                if var in model:
                    coef = model[var].get('coef', 0)
                    se = model[var].get('se', 0)
                    p = model[var].get('p', 1)
                    mark = self._get_sig_mark(p)
                    row_data.append(f"{coef:.{self.config.decimal_places}f}{mark}")
                else:
                    row_data.append("")
            rows.append("| " + " | ".join(row_data) + " |")
        
        # 统计量行
        rows.append("|" + "|".join(["------"] * (len(models) + 1)) + "|")
        
        # R²
        r2_row = ["R²"]
        for model in models:
            r2 = model.get('R2', 0)
            r2_row.append(f"{r2:.{self.config.decimal_places}f}")
        rows.append("| " + " | ".join(r2_row) + " |")
        
        # Adj R²
        adj_r2_row = ["调整R²"]
        for model in models:
            adj_r2 = model.get('Adj_R2', 0)
            adj_r2_row.append(f"{adj_r2:.{self.config.decimal_places}f}")
        rows.append("| " + " | ".join(adj_r2_row) + " |")
        
        # F值
        f_row = ["F"]
        for model in models:
            f = model.get('F', 0)
            f_row.append(f"{f:.{self.config.decimal_places}f}")
        rows.append("| " + " | ".join(f_row) + " |")
        
        # N
        n_row = ["N"]
        for model in models:
            n = model.get('N', 0)
            n_row.append(str(n))
        rows.append("| " + " | ".join(n_row) + " |")
        
        rows.append("")
        rows.append("注：*p < .05, **p < .01, ***p < .001；表中为非标准化回归系数")
        
        return "\n".join(rows)
    
    def anova_table(self, anova_results: Dict) -> str:
        """
        生成方差分析表
        
        Args:
            anova_results: ANOVA结果字典
            
        Returns:
            str: Markdown格式表格
        """
        rows = []
        rows.append(f"表X {self.config.title}")
        rows.append("")
        rows.append("| 变异来源 | 平方和 | 自由度 | 均方 | F | p | η² |")
        rows.append("|----------|--------|--------|------|------|------|------|")
        
        for source, values in anova_results.items():
            if source == 'Total':
                continue
            ss = values.get('SS', 0)
            df = values.get('df', 0)
            ms = values.get('MS', 0)
            f = values.get('F', 0)
            p = values.get('p', 1)
            eta = values.get('eta2', 0)
            mark = self._get_sig_mark(p)
            
            rows.append(
                f"| {source} | "
                f"{ss:.{self.config.decimal_places}f} | "
                f"{df} | "
                f"{ms:.{self.config.decimal_places}f} | "
                f"{f:.{self.config.decimal_places}f}{mark} | "
                f"{p:.{self.config.decimal_places}f} | "
                f"{eta:.{self.config.decimal_places}f} |"
            )
        
        rows.append("")
        rows.append("注：*p < .05, **p < .01, ***p < .001；η²为效应量")
        
        return "\n".join(rows)
    
    def _get_sig_mark(self, p: float) -> str:
        """获取显著性标记"""
        if not self.config.show_stars:
            return ""
        for threshold, mark in sorted(self.SIG_MARKS.items(), reverse=True):
            if p < threshold:
                return mark
        return ""
    
    def mediation_table(self, indirect_effects: Dict) -> str:
        """
        生成中介效应表
        
        Args:
            indirect_effects: 中介效应结果
            
        Returns:
            str: Markdown格式表格
        """
        rows = []
        rows.append(f"表X {self.config.title}")
        rows.append("")
        rows.append("| 效应路径 | 效应值 | 标准误 | 95% CI | 效应占比 |")
        rows.append("|----------|--------|--------|--------|----------|")
        
        for path, values in indirect_effects.items():
            effect = values.get('effect', 0)
            se = values.get('se', 0)
            ci_lower = values.get('ci_lower', 0)
            ci_upper = values.get('ci_upper', 0)
            ratio = values.get('ratio', 0)
            
            rows.append(
                f"| {path} | "
                f"{effect:.{self.config.decimal_places}f} | "
                f"{se:.{self.config.decimal_places}f} | "
                f"[{ci_lower:.{self.config.decimal_places}f}, {ci_upper:.{self.config.decimal_places}f}] | "
                f"{ratio:.{self.config.decimal_places}%} |"
            )
        
        rows.append("")
        rows.append("注：CI = 置信区间；Bootstrap = 5000；不包含0表示效应显著")
        
        return "\n".join(rows)


# 辅助函数：从statsmodels结果生成表格
def from_statsmodels(results, title: str = "回归分析结果") -> str:
    """从statsmodels结果生成表格"""
    import pandas as pd
    
    summary = results.summary()
    params = results.params
    pvalues = results.pvalues
    conf_int = results.conf_int()
    
    rows = []
    rows.append(f"表X {title}")
    rows.append("")
    rows.append("| 变量 | B | SE | t | p | 95% CI |")
    rows.append("|------|------|------|------|------|----------|")
    
    for var in params.index:
        b = params[var]
        se = results.bse[var]
        t = results.tvalues[var]
        p = pvalues[var]
        ci_low = conf_int.loc[var, 0]
        ci_high = conf_int.loc[var, 1]
        
        sig = ""
        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        
        rows.append(
            f"| {var} | {b:.3f}{sig} | {se:.3f} | {t:.3f} | {p:.3f} | [{ci_low:.3f}, {ci_high:.3f}] |"
        )
    
    rows.append("|------|------|------|------|------|----------|")
    rows.append(f"| R² | {results.rsquared:.3f} | 调整R² | {results.rsquared_adj:.3f} | F | {results.fvalue:.3f} |")
    rows.append("")
    rows.append("注：*p < .05, **p < .01, ***p < .001")
    
    return "\n".join(rows)


def main():
    """主函数：示例"""
    # 创建示例数据
    np.random.seed(42)
    n = 100
    data = pd.DataFrame({
        'X1': np.random.normal(3.5, 0.8, n),
        'X2': np.random.normal(2.9, 0.7, n),
        'X3': np.random.normal(3.2, 0.9, n),
        'Y': np.random.normal(3.0, 0.8, n),
        'Group': np.random.choice(['A', 'B'], n)
    })
    
    generator = StatTableGenerator(TableConfig(
        title="示例统计表格",
        note="示例数据，仅用于演示"
    ))
    
    print("=" * 60)
    print("描述性统计")
    print("=" * 60)
    print(generator.descriptive_stats(data, ['X1', 'X2', 'X3', 'Y']))
    
    print("\n" + "=" * 60)
    print("相关分析")
    print("=" * 60)
    print(generator.correlation_matrix(data, ['X1', 'X2', 'X3', 'Y']))
    
    print("\n" + "=" * 60)
    print("分组描述性统计")
    print("=" * 60)
    print(generator.descriptive_stats(data, ['X1', 'X2', 'Y'], group_by='Group'))


if __name__ == "__main__":
    main()
