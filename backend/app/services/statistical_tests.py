from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

class StatisticalTestsService:
    """Service for advanced statistical tests"""
    
    def run_anova(self, df: pd.DataFrame, categorical_col: str, numeric_col: str) -> Dict[str, Any]:
        """Perform one-way ANOVA test"""
        try:
            # Group data by categorical variable
            groups = [group[numeric_col].dropna() for name, group in df.groupby(categorical_col)]
            
            # Need at least 2 groups
            if len(groups) < 2:
                return {"error": "Need at least 2 groups for ANOVA"}
            
            # Perform ANOVA
            f_stat, p_value = scipy_stats.f_oneway(*groups)
            
            return {
                "test": "One-Way ANOVA",
                "categorical_variable": categorical_col,
                "numeric_variable": numeric_col,
                "f_statistic": float(f_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "interpretation": self._interpret_anova(p_value, categorical_col, numeric_col),
                "group_count": len(groups),
                "group_means": {name: float(group[numeric_col].mean()) for name, group in df.groupby(categorical_col)}
            }
        except Exception as e:
            return {"error": str(e)}
    
    def run_t_test(self, df: pd.DataFrame, group_col: str, numeric_col: str, test_type: str = "independent") -> Dict[str, Any]:
        """Perform T-test (independent or paired)"""
        try:
            groups = df.groupby(group_col)[numeric_col].apply(list)
            
            if len(groups) != 2:
                return {"error": "T-test requires exactly 2 groups"}
            
            group1, group2 = list(groups.values())
            
            if test_type == "independent":
                t_stat, p_value = scipy_stats.ttest_ind(group1, group2)
                test_name = "Independent T-Test"
            else:
                t_stat, p_value = scipy_stats.ttest_rel(group1, group2)
                test_name = "Paired T-Test"
            
            return {
                "test": test_name,
                "group_variable": group_col,
                "numeric_variable": numeric_col,
                "t_statistic": float(t_stat),
                "p_value": float(p_value),
                "significant": p_value < 0.05,
                "interpretation": self._interpret_t_test(p_value, list(groups.keys()), numeric_col),
                "group_means": {name: float(np.mean(vals)) for name, vals in groups.items()}
            }
        except Exception as e:
            return {"error": str(e)}
    
    def run_normality_test(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """Perform Shapiro-Wilk normality test"""
        try:
            data = df[column].dropna()
            
            if len(data) < 3:
                return {"error": "Need at least 3 samples for normality test"}
            
            # Use Shapiro-Wilk for small samples (<5000), Kolmogorov-Smirnov for large
            if len(data) < 5000:
                stat, p_value = scipy_stats.shapiro(data)
                test_name = "Shapiro-Wilk Test"
            else:
                stat, p_value = scipy_stats.kstest(data, 'norm')
                test_name = "Kolmogorov-Smirnov Test"
            
            return {
                "test": test_name,
                "column": column,
                "statistic": float(stat),
                "p_value": float(p_value),
                "is_normal": p_value > 0.05,
                "interpretation": self._interpret_normality(p_value, column),
                "sample_size": len(data),
                "skewness": float(data.skew()),
                "kurtosis": float(data.kurtosis())
            }
        except Exception as e:
            return {"error": str(e)}
    
    def run_chi_square_test(self, df: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
        """Perform Chi-Square test for independence"""
        try:
            contingency_table = pd.crosstab(df[col1], df[col2])
            
            chi2, p_value, dof, expected = scipy_stats.chi2_contingency(contingency_table)
            
            return {
                "test": "Chi-Square Test of Independence",
                "variable1": col1,
                "variable2": col2,
                "chi2_statistic": float(chi2),
                "p_value": float(p_value),
                "degrees_of_freedom": int(dof),
                "significant": p_value < 0.05,
                "interpretation": self._interpret_chi_square(p_value, col1, col2),
                "contingency_table": contingency_table.to_dict()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _interpret_anova(self, p_value: float, cat_col: str, num_col: str) -> str:
        """Interpret ANOVA results"""
        if p_value < 0.001:
            return f"Very strong evidence that {num_col} differs significantly across {cat_col} groups (p < 0.001)"
        elif p_value < 0.01:
            return f"Strong evidence that {num_col} differs significantly across {cat_col} groups (p < 0.01)"
        elif p_value < 0.05:
            return f"Significant difference in {num_col} across {cat_col} groups (p < 0.05)"
        else:
            return f"No significant difference in {num_col} across {cat_col} groups (p = {p_value:.3f})"
    
    def _interpret_t_test(self, p_value: float, groups: List[str], num_col: str) -> str:
        """Interpret T-test results"""
        if p_value < 0.05:
            return f"Significant difference in {num_col} between {groups[0]} and {groups[1]} (p = {p_value:.3f})"
        else:
            return f"No significant difference in {num_col} between {groups[0]} and {groups[1]} (p = {p_value:.3f})"
    
    def _interpret_normality(self, p_value: float, column: str) -> str:
        """Interpret normality test results"""
        if p_value > 0.05:
            return f"{column} appears to follow a normal distribution (p = {p_value:.3f})"
        else:
            return f"{column} does not follow a normal distribution (p = {p_value:.3f})"
    
    def _interpret_chi_square(self, p_value: float, col1: str, col2: str) -> str:
        """Interpret Chi-Square test results"""
        if p_value < 0.05:
            return f"Significant association between {col1} and {col2} (p = {p_value:.3f})"
        else:
            return f"No significant association between {col1} and {col2} (p = {p_value:.3f})"
