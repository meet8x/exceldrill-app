import pandas as pd
import numpy as np
import io
from typing import Dict, Any, List

class DataProcessor:
    def __init__(self):
        self.df = None
        self.filename = None

    def load_data(self, file_content: bytes, filename: str):
        self.filename = filename
        if filename.endswith('.csv'):
            self.df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith(('.xls', '.xlsx')):
            self.df = pd.read_excel(io.BytesIO(file_content))
        else:
            raise ValueError("Unsupported file format")
        
        # Basic cleanup: convert object columns to string if needed, etc.
        return self.get_preview()

    def get_preview(self, rows: int = 50) -> Dict[str, Any]:
        if self.df is None:
            return {}
        
        # Replace NaN with None for JSON serialization
        preview_df = self.df.head(rows).replace({np.nan: None})
        return {
            "columns": list(self.df.columns),
            "data": preview_df.to_dict(orient='records'),
            "total_rows": len(self.df),
            "dtypes": self.df.dtypes.astype(str).to_dict()
        }

    def clean_data(self, action: str, params: Dict[str, Any] = None):
        if self.df is None:
            raise ValueError("No data loaded")
        
        if action == "drop_nulls":
            self.df = self.df.dropna()
        elif action == "fill_nulls":
            value = params.get("value", 0)
            self.df = self.df.fillna(value)
        elif action == "smart_impute":
            col = params.get("column")
            strategy = params.get("strategy", "mean") # mean, median
            if col and col in self.df.columns:
                if strategy == "mean":
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
                elif strategy == "median":
                    self.df[col] = self.df[col].fillna(self.df[col].median())
        elif action == "remove_outliers":
            col = params.get("column")
            method = params.get("method", "iqr")
            if col and col in self.df.columns:
                if method == "iqr":
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    self.df = self.df[~((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR)))]

        elif action == "rename_column":
            old_name = params.get("old_name")
            new_name = params.get("new_name")
            if old_name and new_name:
                self.df = self.df.rename(columns={old_name: new_name})
        elif action == "convert_type":
            col = params.get("column")
            dtype = params.get("dtype") # 'numeric', 'datetime'
            if col and dtype:
                if dtype == 'numeric':
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                elif dtype == 'datetime':
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        return self.get_preview()

    def get_statistics(self) -> Dict[str, Any]:
        if self.df is None:
            raise ValueError("No data loaded")
        
        # Numeric summary
        numeric_df = self.df.select_dtypes(include=[np.number])
        desc = numeric_df.describe().replace({np.nan: None}).to_dict()
        
        # Categorical summary
        cat_df = self.df.select_dtypes(include=['object', 'category'])
        cat_summary = {}
        for col in cat_df.columns:
            counts = cat_df[col].value_counts().head(10).to_dict()
            cat_summary[col] = counts

        # Correlations (numeric only)
        corr = {}
        if not numeric_df.empty:
            corr_matrix = numeric_df.corr()
            corr = corr_matrix.replace({np.nan: None}).to_dict()

        return {
            "summary": desc,
            "categorical": cat_summary,
            "correlation": corr
        }

    def get_univariate_analysis(self, column: str) -> Dict[str, Any]:
        if self.df is None or column not in self.df.columns:
            raise ValueError("Invalid column")
        
        data = self.df[column].dropna()
        if pd.api.types.is_numeric_dtype(data):
            # Convert stats to native Python types for JSON serialization
            stats = data.describe().to_dict()
            stats = {k: float(v) if isinstance(v, (np.floating, float)) else int(v) if isinstance(v, (np.integer, int)) else v for k, v in stats.items()}
            
            # Histogram data
            hist, bin_edges = np.histogram(data, bins='auto')
            return {
                "type": "numeric",
                "stats": stats,
                "histogram": {"counts": hist.tolist(), "bins": bin_edges.tolist()}
            }
        else:
            counts = data.value_counts().head(20).to_dict()
            return {
                "type": "categorical",
                "counts": counts
            }

    def get_bivariate_analysis(self, col1: str, col2: str) -> Dict[str, Any]:
        if self.df is None or col1 not in self.df.columns or col2 not in self.df.columns:
            raise ValueError("Invalid columns")
        
        data = self.df[[col1, col2]].dropna()
        
        # Numeric vs Numeric
        if pd.api.types.is_numeric_dtype(data[col1]) and pd.api.types.is_numeric_dtype(data[col2]):
            correlation = data[col1].corr(data[col2])
            from scipy import stats
            pearson_coef, p_value = stats.pearsonr(data[col1], data[col2])
            
            return {
                "type": "numeric_numeric",
                "correlation": float(correlation) if not pd.isna(correlation) else None,
                "p_value": float(p_value) if not pd.isna(p_value) else None,
                "significance": "Significant" if p_value < 0.05 else "Not Significant",
                "scatter_data": data.head(500).to_dict(orient='records')
            }
        # Categorical vs Numeric (Box Plot data)
        elif pd.api.types.is_numeric_dtype(data[col2]) and not pd.api.types.is_numeric_dtype(data[col1]):
             # Group by categorical col1 and get list of values for col2
             groups = data.groupby(col1)[col2].apply(list).to_dict()
             # Limit to top 10 categories to avoid clutter
             top_cats = data[col1].value_counts().head(10).index
             filtered_groups = {k: v for k, v in groups.items() if k in top_cats}
             return {
                 "type": "categorical_numeric",
                 "box_data": filtered_groups
             }
        else:
            return {"type": "other", "message": "Combination not fully supported for deep analysis yet"}

    def get_chi_square_test(self, col1: str, col2: str) -> Dict[str, Any]:
        """
        Calculate Chi-Square test for independence between two categorical variables.
        """
        if self.df is None or col1 not in self.df.columns or col2 not in self.df.columns:
            raise ValueError("Invalid columns")

        data = self.df[[col1, col2]].dropna()
        
        # Check if both are categorical (or object/low cardinality int)
        # We'll assume if this is called, the caller intends to treat them as categorical
        
        contingency_table = pd.crosstab(data[col1], data[col2])
        
        # Check for sufficient data
        if contingency_table.size == 0:
             return {"error": "Insufficient data"}

        from scipy.stats import chi2_contingency
        try:
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            return {
                "chi2": float(chi2),
                "p_value": float(p),
                "dof": int(dof),
                "significance": "Significant" if p < 0.05 else "Not Significant",
                "contingency_table": contingency_table.to_dict()
            }
        except Exception as e:
            return {"error": str(e)}

    def get_multivariate_analysis(self, columns: List[str]) -> Dict[str, Any]:
        if self.df is None:
             raise ValueError("No data")
        
        data = self.df[columns].dropna()
        numeric_df = data.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"error": "No numeric columns selected"}
            
        corr_matrix = numeric_df.corr()
        
        # Calculate p-values matrix
        from scipy import stats
        p_values = pd.DataFrame(np.zeros_like(corr_matrix), columns=corr_matrix.columns, index=corr_matrix.index)
        for r in corr_matrix.columns:
            for c in corr_matrix.columns:
                if r == c:
                    p_values.loc[r, c] = 0.0
                else:
                    # Handle constant columns or other issues that might cause pearsonr to fail or return NaN
                    try:
                        if numeric_df[r].nunique() <= 1 or numeric_df[c].nunique() <= 1:
                             p_values.loc[r, c] = 1.0 # Not significant if constant
                        else:
                            _, p = stats.pearsonr(numeric_df[r], numeric_df[c])
                            p_values.loc[r, c] = p
                    except:
                        p_values.loc[r, c] = 1.0

        return {
            "correlation_matrix": corr_matrix.replace({np.nan: None}).to_dict(),
            "p_values": p_values.replace({np.nan: None}).to_dict()
        }

    def get_chart_data(self, x_col: str, y_col: str = None, chart_type: str = "bar"):
        if self.df is None:
            raise ValueError("No data loaded")
        
        data = []
        if chart_type == "bar" or chart_type == "line":
            if y_col:
                if self.df[x_col].dtype == 'object' and self.df[y_col].dtype != 'object':
                     agg = self.df.groupby(x_col)[y_col].mean().reset_index()
                     data = agg.to_dict(orient='records')
                else:
                    data = self.df[[x_col, y_col]].dropna().head(1000).to_dict(orient='records')
            else:
                counts = self.df[x_col].value_counts().reset_index()
                counts.columns = [x_col, 'count']
                data = counts.head(20).to_dict(orient='records')
        
        elif chart_type == "scatter":
             if x_col and y_col:
                 data = self.df[[x_col, y_col]].dropna().head(1000).to_dict(orient='records')

        return data

    def is_identifier(self, col: str) -> bool:
        """
        Enhanced identifier detection:
        - Common ID keywords (id, email, phone, sr, no, name, etc.)
        - High cardinality (>90% unique values)
        - Sequential numbering pattern
        - Email/phone patterns
        """
        if self.df is None or col not in self.df.columns:
            return False
        
        data = self.df[col]
        
        # 1. Check column name for common identifier keywords
        lower_col = col.lower()
        id_keywords = ['id', 'email', 'phone', 'mobile', 'uuid', 'guid', 'code', 'token', 
                       'sr', 'sno', 's.no', 'sr.', 's.', 'no', 'number', 'index', 'key', 
                       'username', 'user_id', 'customer_id', 'name', 'firstname', 'lastname',
                       'fullname', 'employee', 'student', 'roll']
        if any(keyword in lower_col for keyword in id_keywords):
            return True
        
        # 2. Check for high cardinality (object/string types)
        if data.dtype == 'object':
            unique_ratio = data.nunique() / len(data)
            if unique_ratio > 0.9 and len(data) > 20:
                return True
            
            # Check for email pattern (simple check)
            sample = data.dropna().astype(str).head(10)
            if sample.str.contains('@').sum() > 5:  # If >50% look like emails
                return True
            
            # Check for phone pattern (simple check for digits)
            if sample.str.replace('[^0-9]', '', regex=True).str.len().mean() > 8:
                # Looks like phone numbers
                return True
        
        # 3. Check for sequential numbering (1, 2, 3, ...)
        if pd.api.types.is_numeric_dtype(data):
            if len(data) > 10:
                # Check if it's sequential
                sorted_data = data.dropna().sort_values().reset_index(drop=True)
                if len(sorted_data) > 0:
                    diffs = sorted_data.diff().dropna()
                    if (diffs == 1).sum() / len(diffs) > 0.8:  # 80% are increments of 1
                        return True
        
        return False
