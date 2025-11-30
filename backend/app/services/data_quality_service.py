from typing import Dict, Any, List
import pandas as pd
import numpy as np
from scipy import stats

class DataQualityService:
    """Service for automated data quality detection and reporting"""
    
    def analyze_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive data quality analysis"""
        issues = []
        recommendations = []
        
        # 1. High missing values
        missing_issues = self._detect_high_missing(df)
        issues.extend(missing_issues['issues'])
        recommendations.extend(missing_issues['recommendations'])
        
        # 2. Duplicate rows
        dup_issues = self._detect_duplicates(df)
        issues.extend(dup_issues['issues'])
        recommendations.extend(dup_issues['recommendations'])
        
        # 3. Constant/near-constant columns
        const_issues = self._detect_constant_columns(df)
        issues.extend(const_issues['issues'])
        recommendations.extend(const_issues['recommendations'])
        
        # 4. Outliers
        outlier_issues = self._detect_outliers(df)
        issues.extend(outlier_issues['issues'])
        recommendations.extend(outlier_issues['recommendations'])
        
        # 5. Skewed distributions
        skew_issues = self._detect_skewness(df)
        issues.extend(skew_issues['issues'])
        recommendations.extend(skew_issues['recommendations'])
        
        # Calculate overall quality score
        quality_score = self._calculate_quality_score(df, len(issues))
        
        return {
            "quality_score": quality_score,
            "total_issues": len(issues),
            "issues": issues,
            "recommendations": recommendations,
            "summary": self._generate_summary(df, issues)
        }
    
    def _detect_high_missing(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect columns with high missing values (>20%)"""
        issues = []
        recommendations = []
        
        for col in df.columns:
            missing_pct = (df[col].isnull().sum() / len(df)) * 100
            if missing_pct > 20:
                issues.append({
                    "type": "high_missing",
                    "severity": "high" if missing_pct > 50 else "medium",
                    "column": col,
                    "value": f"{missing_pct:.1f}%",
                    "description": f"Column '{col}' has {missing_pct:.1f}% missing values"
                })
                
                if missing_pct > 50:
                    recommendations.append(f"Consider removing column '{col}' (>{missing_pct:.0f}% missing)")
                else:
                    recommendations.append(f"Impute missing values in '{col}' using mean/median/mode")
        
        return {"issues": issues, "recommendations": recommendations}
    
    def _detect_duplicates(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect duplicate rows"""
        issues = []
        recommendations = []
        
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            dup_pct = (dup_count / len(df)) * 100
            issues.append({
                "type": "duplicates",
                "severity": "high" if dup_pct > 5 else "medium",
                "column": "All",
                "value": f"{dup_count} rows ({dup_pct:.1f}%)",
                "description": f"Found {dup_count} duplicate rows ({dup_pct:.1f}% of data)"
            })
            recommendations.append(f"Remove {dup_count} duplicate rows to ensure data integrity")
        
        return {"issues": issues, "recommendations": recommendations}
    
    def _detect_constant_columns(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect constant or near-constant columns"""
        issues = []
        recommendations = []
        
        for col in df.columns:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio < 0.01:  # Less than 1% unique values
                issues.append({
                    "type": "constant_column",
                    "severity": "low",
                    "column": col,
                    "value": f"{df[col].nunique()} unique values",
                    "description": f"Column '{col}' has very low variance ({df[col].nunique()} unique values)"
                })
                recommendations.append(f"Consider removing '{col}' - provides little information")
        
        return {"issues": issues, "recommendations": recommendations}
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect outliers using IQR method"""
        issues = []
        recommendations = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))][col]
            outlier_count = len(outliers)
            
            if outlier_count > 0:
                outlier_pct = (outlier_count / len(df)) * 100
                if outlier_pct > 5:  # Only report if >5% are outliers
                    issues.append({
                        "type": "outliers",
                        "severity": "medium",
                        "column": col,
                        "value": f"{outlier_count} outliers ({outlier_pct:.1f}%)",
                        "description": f"Column '{col}' has {outlier_count} outliers ({outlier_pct:.1f}%)"
                    })
                    recommendations.append(f"Investigate outliers in '{col}' - may indicate data errors or special cases")
        
        return {"issues": issues, "recommendations": recommendations}
    
    def _detect_skewness(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect highly skewed distributions"""
        issues = []
        recommendations = []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            skewness = df[col].skew()
            if abs(skewness) > 2:  # Highly skewed
                issues.append({
                    "type": "skewed_distribution",
                    "severity": "low",
                    "column": col,
                    "value": f"Skewness: {skewness:.2f}",
                    "description": f"Column '{col}' is highly skewed (skewness: {skewness:.2f})"
                })
                recommendations.append(f"Consider log transformation for '{col}' to reduce skewness")
        
        return {"issues": issues, "recommendations": recommendations}
    
    def _calculate_quality_score(self, df: pd.DataFrame, issue_count: int) -> float:
        """Calculate overall data quality score (0-100)"""
        # Start with 100 and deduct points for issues
        score = 100.0
        
        # Deduct for missing values
        missing_pct = (df.isnull().sum().sum() / df.size) * 100
        score -= min(missing_pct, 30)  # Max 30 points deduction
        
        # Deduct for issues (5 points per issue, max 40)
        score -= min(issue_count * 5, 40)
        
        return max(score, 0)
    
    def _generate_summary(self, df: pd.DataFrame, issues: List[Dict]) -> Dict[str, Any]:
        """Generate quality summary statistics"""
        return {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "total_cells": df.size,
            "missing_cells": df.isnull().sum().sum(),
            "missing_percentage": (df.isnull().sum().sum() / df.size * 100),
            "duplicate_rows": df.duplicated().sum(),
            "high_severity_issues": len([i for i in issues if i['severity'] == 'high']),
            "medium_severity_issues": len([i for i in issues if i['severity'] == 'medium']),
            "low_severity_issues": len([i for i in issues if i['severity'] == 'low'])
        }
