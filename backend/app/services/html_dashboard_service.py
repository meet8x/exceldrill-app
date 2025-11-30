import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from typing import Dict, Any, List
import io
import json

class HtmlDashboardService:
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Data Analysis Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card { margin-bottom: 20px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 12px; }
        .card-header { background-color: #fff; border-bottom: 1px solid #eee; font-weight: 600; color: #333; border-radius: 12px 12px 0 0 !important; padding: 15px 20px; }
        .sidebar { position: fixed; top: 0; bottom: 0; left: 0; z-index: 100; padding: 48px 0 0; box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1); background-color: #fff; }
        .sidebar-sticky { position: relative; top: 0; height: calc(100vh - 48px); padding-top: .5rem; overflow-x: hidden; overflow-y: auto; }
        .nav-link { font-weight: 500; color: #333; padding: 10px 20px; }
        .nav-link:hover { color: #007bff; background-color: #f8f9fa; }
        .nav-link.active { color: #007bff; }
        .metric-card { text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .metric-value { font-size: 2rem; font-weight: bold; color: #007bff; }
        .metric-label { color: #6c757d; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        main { margin-left: 240px; padding: 30px; }
        @media (max-width: 768px) {
            .sidebar { display: none; }
            main { margin-left: 0; }
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block sidebar collapse">
                <div class="position-sticky sidebar-sticky">
                    <h5 class="px-3 pb-3 border-bottom">Analysis Report</h5>
                    <ul class="nav flex-column">
                        <li class="nav-item"><a class="nav-link" href="#overview">Overview</a></li>
                        <li class="nav-item"><a class="nav-link" href="#data-quality">Data Quality</a></li>
                        <li class="nav-item"><a class="nav-link" href="#univariate">Univariate Analysis</a></li>
                        <li class="nav-item"><a class="nav-link" href="#bivariate">Bivariate Analysis</a></li>
                        <li class="nav-item"><a class="nav-link" href="#correlations">Correlations</a></li>
                    </ul>
                </div>
            </nav>

            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                    <h1 class="h2">Interactive Data Analysis Dashboard</h1>
                    <div class="btn-toolbar mb-2 mb-md-0">
                        <button type="button" class="btn btn-sm btn-outline-secondary" onclick="window.print()">Export PDF</button>
                    </div>
                </div>

                <!-- Overview Section -->
                <section id="overview" class="mb-5">
                    <h3 class="mb-4">Dataset Overview</h3>
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="metric-card">
                                <div class="metric-value">{{ total_records }}</div>
                                <div class="metric-label">Total Records</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="metric-card">
                                <div class="metric-value">{{ total_columns }}</div>
                                <div class="metric-label">Total Columns</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="metric-card">
                                <div class="metric-value">{{ missing_cells }}</div>
                                <div class="metric-label">Missing Cells</div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="metric-card">
                                <div class="metric-value">{{ duplicate_rows }}</div>
                                <div class="metric-label">Duplicate Rows</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header">Key AI Insights</div>
                        <div class="card-body">
                            <ul class="list-group list-group-flush">
                                {% for insight in insights %}
                                <li class="list-group-item">{{ insight }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    </div>
                </section>

                <!-- Data Quality Section -->
                <section id="data-quality" class="mb-5">
                    <h3 class="mb-4">Data Quality Analysis</h3>
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive">
                                {{ quality_table }}
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Univariate Analysis -->
                <section id="univariate" class="mb-5">
                    <h3 class="mb-4">Univariate Analysis</h3>
                    <div class="row">
                        {% for plot in univariate_plots %}
                        <div class="col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-header">{{ plot.title }}</div>
                                <div class="card-body">
                                    {{ plot.div | safe }}
                                    <div class="mt-3 text-muted small">
                                        {{ plot.insight }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Bivariate Analysis -->
                <section id="bivariate" class="mb-5">
                    <h3 class="mb-4">Bivariate Analysis</h3>
                    <div class="row">
                        {% for plot in bivariate_plots %}
                        <div class="col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-header">{{ plot.title }}</div>
                                <div class="card-body">
                                    {{ plot.div | safe }}
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </section>

                <!-- Correlations -->
                <section id="correlations" class="mb-5">
                    <h3 class="mb-4">Correlation Matrix</h3>
                    <div class="card">
                        <div class="card-body">
                            {{ correlation_plot | safe }}
                        </div>
                    </div>
                </section>
            </main>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


    def _is_identifier(self, df: pd.DataFrame, col: str) -> bool:
        """Detect if a column is an identifier (ID, name, phone, address, etc.)"""
        lower_col = col.lower()
        
        # Check for common identifier keywords
        id_keywords = ['id', 'sr', 'serial', 'number', 'no', 'name', 'phone', 'mobile', 
                       'email', 'address', 'uuid', 'guid', 'code', 'token', 'key']
        if any(keyword in lower_col for keyword in id_keywords):
            return True
        
        # Check for high cardinality (unique ratio > 90%)
        if df[col].dtype == 'object':
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio > 0.9 and len(df) > 20:
                return True
        
        return False

    def generate_dashboard(self, df: pd.DataFrame, stats: Dict[str, Any], insights: List[str]) -> io.BytesIO:
        # 1. Prepare Overview Data
        total_records = len(df)
        total_columns = len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        # 2. Prepare Data Quality Table
        quality_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Missing (%)': (df.isnull().sum() / len(df) * 100).round(1),
            'Unique Values': df.nunique(),
            'Memory Usage (KB)': (df.memory_usage(deep=True)[1:] / 1024).round(1).values
        })
        quality_table_html = quality_df.to_html(classes='table table-striped table-hover', index=False)

        # Filter out identifier columns for analysis
        analysis_cols = [col for col in df.columns if not self._is_identifier(df, col)]
        df_analysis = df[analysis_cols]

        # 3. Generate Univariate Plots
        univariate_plots = []
        for col in df_analysis.columns[:10]:  # Limit to 10 for performance
            if pd.api.types.is_numeric_dtype(df_analysis[col]):
                fig = px.histogram(df_analysis, x=col, title=f"Distribution of {col}", template="plotly_white")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300, bargap=0.2)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                univariate_plots.append({'title': col, 'div': div, 'insight': f"Mean: {df_analysis[col].mean():.2f}, Std: {df_analysis[col].std():.2f}"})
            elif df_analysis[col].nunique() < 20:
                value_counts = df_analysis[col].value_counts().reset_index()
                value_counts.columns = ['category', 'count']
                fig = px.bar(value_counts, x='category', y='count', title=f"Count of {col}", template="plotly_white")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300, bargap=0.3)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                univariate_plots.append({'title': col, 'div': div, 'insight': f"Top category: {df_analysis[col].mode()[0]}"})

        # 4. Generate Bivariate Plots
        bivariate_plots = []
        numeric_cols = df_analysis.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df_analysis.select_dtypes(include=['object', 'category']).columns.tolist()
        categorical_cols = [c for c in categorical_cols if df_analysis[c].nunique() < 10]  # Only low-cardinality categoricals

        # 4a. Numeric-Numeric (Scatter plots with correlation)
        if len(numeric_cols) >= 2:
            corr = df_analysis[numeric_cols].corr().abs()
            pairs = (corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
                     .stack()
                     .sort_values(ascending=False)
                     .head(6))
            
            for (col1, col2), val in pairs.items():
                fig = px.scatter(df_analysis, x=col1, y=col2, title=f"{col1} vs {col2} (Corr: {val:.2f})", 
                               template="plotly_white", trendline="ols")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                bivariate_plots.append({'title': f"{col1} vs {col2} (Numeric)", 'div': div})

        # 4b. Categorical-Numeric (Box plots)
        for cat_col in categorical_cols[:5]:  # Limit to 5
            for num_col in numeric_cols[:3]:  # Limit to 3 numeric per categorical
                fig = px.box(df_analysis, x=cat_col, y=num_col, 
                           title=f"{num_col} by {cat_col}", template="plotly_white")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                bivariate_plots.append({'title': f"{num_col} by {cat_col} (Cat-Num)", 'div': div})

        # 4c. Categorical-Categorical (Stacked bar charts)
        if len(categorical_cols) >= 2:
            for i, cat1 in enumerate(categorical_cols[:3]):
                for cat2 in categorical_cols[i+1:i+2]:  # Pair with next one
                    crosstab = pd.crosstab(df_analysis[cat1], df_analysis[cat2])
                    crosstab_reset = crosstab.reset_index()
                    crosstab_melted = crosstab_reset.melt(id_vars=cat1, var_name=cat2, value_name='count')
                    
                    fig = px.bar(crosstab_melted, x=cat1, y='count', color=cat2,
                               title=f"{cat1} vs {cat2}", template="plotly_white", barmode='stack')
                    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300, bargap=0.2)
                    div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                    bivariate_plots.append({'title': f"{cat1} vs {cat2} (Cat-Cat)", 'div': div})

        # 5. Generate Correlation Heatmap
        if len(numeric_cols) > 1:
            corr_matrix = df_analysis[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Correlation Heatmap")
            fig.update_layout(height=600)
            correlation_plot = pio.to_html(fig, full_html=False, include_plotlyjs=False)
        else:
            correlation_plot = "<p>Not enough numeric columns for correlation analysis.</p>"

        # 6. Render Template using Jinja2
        try:
            from jinja2 import Template
            t = Template(self.template)
            html = t.render(
                total_records=total_records,
                total_columns=total_columns,
                missing_cells=missing_cells,
                duplicate_rows=duplicate_rows,
                insights=insights,
                quality_table=quality_table_html,
                univariate_plots=univariate_plots,
                bivariate_plots=bivariate_plots,
                correlation_plot=correlation_plot
            )
        except ImportError:
            print("Jinja2 not found, falling back to simple replacement (loops will fail)")
            html = self.template

        return io.BytesIO(html.encode('utf-8'))

        total_columns = len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        # 2. Prepare Data Quality Table
        quality_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Missing (%)': (df.isnull().sum() / len(df) * 100).round(1),
            'Unique Values': df.nunique(),
            'Memory Usage (KB)': (df.memory_usage(deep=True)[1:] / 1024).round(1).values
        })
        quality_table_html = quality_df.to_html(classes='table table-striped table-hover', index=False)

        # 3. Generate Univariate Plots
        univariate_plots = []
        for col in df.columns[:10]:  # Limit to 10 for performance
            if pd.api.types.is_numeric_dtype(df[col]):
                fig = px.histogram(df, x=col, title=f"Distribution of {col}", template="plotly_white")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                univariate_plots.append({'title': col, 'div': div, 'insight': f"Mean: {df[col].mean():.2f}, Std: {df[col].std():.2f}"})
            elif df[col].nunique() < 20:
                # Fix: properly reset index and rename columns for plotly
                value_counts = df[col].value_counts().reset_index()
                value_counts.columns = ['category', 'count']
                fig = px.bar(value_counts, x='category', y='count', title=f"Count of {col}", template="plotly_white")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                univariate_plots.append({'title': col, 'div': div, 'insight': f"Top category: {df[col].mode()[0]}"})

        # 4. Generate Bivariate Plots
        bivariate_plots = []
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr().abs()
            # Find top correlated pairs
            pairs = (corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
                     .stack()
                     .sort_values(ascending=False)
                     .head(6))
            
            for (col1, col2), val in pairs.items():
                fig = px.scatter(df, x=col1, y=col2, title=f"{col1} vs {col2} (Corr: {val:.2f})", template="plotly_white", trendline="ols")
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=300)
                div = pio.to_html(fig, full_html=False, include_plotlyjs=False)
                bivariate_plots.append({'title': f"{col1} vs {col2}", 'div': div})

        # 5. Generate Correlation Heatmap
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Correlation Heatmap")
            fig.update_layout(height=600)
            correlation_plot = pio.to_html(fig, full_html=False, include_plotlyjs=False)
        else:
            correlation_plot = "<p>Not enough numeric columns for correlation analysis.</p>"

        # 6. Render Template (Simple string replacement for now, Jinja2 would be better but keeping dependencies low)
        # Using simple replace for keys
        html = self.template
        html = html.replace('{{ total_records }}', str(total_records))
        html = html.replace('{{ total_columns }}', str(total_columns))
        html = html.replace('{{ missing_cells }}', str(missing_cells))
        html = html.replace('{{ duplicate_rows }}', str(duplicate_rows))
        
        # Insights loop (manual)
        insights_html = ""
        for insight in insights:
            insights_html += f'<li class="list-group-item">{insight}</li>'
        html = html.replace('{% for insight in insights %}\n                                <li class="list-group-item">{{ insight }}</li>\n                                {% endfor %}', insights_html)

        html = html.replace('{{ quality_table }}', quality_table_html)
        html = html.replace('{{ correlation_plot | safe }}', correlation_plot)

        # Univariate loop (manual)
        uni_html = ""
        for plot in univariate_plots:
            uni_html += f"""
                        <div class="col-md-6 mb-4">
                            <div class="card h-100">
                                <div class="card-header">{plot['title']}</div>
                                <div class="card-body">
                                    {plot['div']}
                                    <div class="mt-3 text-muted small">
                                        {plot['insight']}
                                    </div>
                                </div>
                            </div>
                        </div>"""
        # Regex replacement for the loop block would be safer, but let's try to match the block structure
        # Actually, since I defined the template string, I can just split it or use Jinja2 if available.
        # Let's try to use jinja2 if installed, otherwise fallback to replace.
        # Given the complexity of loops, I'll assume Jinja2 is available (standard in FastAPI/Flask envs).
        
        try:
            from jinja2 import Template
            t = Template(self.template)
            html = t.render(
                total_records=total_records,
                total_columns=total_columns,
                missing_cells=missing_cells,
                duplicate_rows=duplicate_rows,
                insights=insights,
                quality_table=quality_table_html,
                univariate_plots=univariate_plots,
                bivariate_plots=bivariate_plots,
                correlation_plot=correlation_plot
            )
        except ImportError:
            # Fallback or error
            print("Jinja2 not found, falling back to simple replacement (loops will fail)")
            pass

        return io.BytesIO(html.encode('utf-8'))
