export interface DataPreview {
    columns: string[];
    data: any[];
    total_rows: number;
    dtypes: Record<string, string>;
}

export interface Statistics {
    summary: Record<string, any>;
    categorical: Record<string, any>;
    correlation: Record<string, any>;
}

export interface AnalysisConfig {
    type: 'univariate' | 'bivariate' | 'multivariate';
    columns: string[];
}

export interface AnalysisResult {
    type: string;
    stats?: any;
    histogram?: { counts: number[], bins: number[] };
    counts?: Record<string, number>;
    correlation?: number;
    p_value?: number;
    significance?: string;
    scatter_data?: any[];
    box_data?: Record<string, number[]>;
    correlation_matrix?: Record<string, Record<string, number>>;
    p_values?: Record<string, Record<string, number>>;
    error?: string;
    message?: string;
}

export interface InsightsResponse {
    insights: string[];
}
