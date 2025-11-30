import axios from 'axios';
import { AnalysisConfig, AnalysisResult } from './types';

const API_URL = 'http://localhost:8000/api';

export const client = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

client.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await client.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const cleanData = async (action: string, params: any = {}) => {
    const response = await client.post('/clean', { action, params });
    return response.data;
};

export const analyzeData = async () => {
    const response = await client.get('/analyze');
    return response.data;
};

export const verifyOtp = async (email: string, otp: string) => {
    const response = await client.post('/auth/verify-otp', { email, otp });
    return response.data;
};

export const googleLogin = async (credential: string) => {
    const response = await client.post('/auth/google', { credential });
    return response.data;
};

export const runAdvancedAnalysis = async (config: AnalysisConfig): Promise<AnalysisResult> => {
    let endpoint = '';
    let body = {};

    if (config.type === 'univariate') {
        endpoint = '/analyze/univariate';
        body = { column: config.columns[0] };
    } else if (config.type === 'bivariate') {
        endpoint = '/analyze/bivariate';
        body = { col1: config.columns[0], col2: config.columns[1] };
    } else if (config.type === 'multivariate') {
        endpoint = '/analyze/multivariate';
        body = { columns: config.columns };
    }

    const response = await client.post(endpoint, body);
    return response.data;
};

export const getChartData = async (x_col: string, y_col?: string, chart_type: string = 'bar') => {
    const response = await client.post('/chart-data', { x_col, y_col, chart_type });
    return response.data;
};

export const getInsights = async () => {
    const response = await client.get('/insights');
    return response.data;
};

export const downloadReport = async (format: 'word' | 'ppt' | 'excel' | 'html', onProgress?: (progress: number) => void) => {
    try {
        // 1. Start generation
        const startResponse = await client.post(`/report/start/${format}`);
        const jobId = startResponse.data.job_id;

        // 2. Poll for status
        const pollInterval = setInterval(async () => {
            try {
                const statusResponse = await client.get(`/report/status/${jobId}`);
                const { status, progress, error } = statusResponse.data;

                if (onProgress) {
                    onProgress(progress);
                }

                if (status === 'completed') {
                    clearInterval(pollInterval);
                    // 3. Download
                    const downloadResponse = await client.get(`/report/download/${jobId}`, {
                        responseType: 'blob',
                    });

                    const blob = new Blob([downloadResponse.data]);
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = format === 'word' ? 'report.docx' : format === 'ppt' ? 'report.pptx' : format === 'excel' ? 'report.xlsx' : 'report.html';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);
                } else if (status === 'failed') {
                    clearInterval(pollInterval);
                    alert(`Report generation failed: ${error}`);
                }
            } catch (err) {
                console.error("Polling error", err);
                clearInterval(pollInterval);
            }
        }, 1000);

    } catch (error: any) {
        console.error('Download failed:', error);
        if (error.response?.status === 401) {
            alert('Authentication failed. Please log in again.');
        } else if (error.response?.status === 403) {
            alert('Premium subscription required to download reports.');
        } else {
            alert('Failed to start report generation. Please try again.');
        }
    }
};
