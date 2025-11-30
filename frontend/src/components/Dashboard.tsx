import React, { useState, useEffect } from 'react';
import { Statistics, AnalysisConfig, AnalysisResult } from '../api/types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, ScatterChart, Scatter, ZAxis } from 'recharts';
import { Lightbulb, BarChart2, Activity, ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';
import { AnalysisSelector } from './AnalysisSelector';
import { ExportPanel } from './ExportPanel';
import { runAdvancedAnalysis, getChartData } from '../api/client';

interface DashboardProps {
    stats: Statistics;
    insights: string[];
    columns: string[];
}

export const Dashboard: React.FC<DashboardProps> = ({ stats, insights, columns }) => {
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    // Legacy state for simple charts (kept for backward compatibility if needed, or we can remove)
    const [chartData, setChartData] = useState<any[]>([]);
    const [xCol, setXCol] = useState(columns[0] || '');
    const [yCol, setYCol] = useState(columns[1] || '');
    const [chartType, setChartType] = useState('bar');

    const handleAdvancedAnalysis = async (config: AnalysisConfig) => {
        setIsAnalyzing(true);
        try {
            const result = await runAdvancedAnalysis(config);
            setAnalysisResult(result);
        } catch (error) {
            console.error("Analysis failed", error);
        } finally {
            setIsAnalyzing(false);
        }
    };

    const renderAnalysisResult = () => {
        if (!analysisResult) return null;

        if (analysisResult.type === 'numeric') {
            // Univariate Numeric (Histogram)
            const histData = analysisResult.histogram?.bins.slice(0, -1).map((bin, i) => ({
                range: `${bin.toFixed(2)} - ${analysisResult.histogram?.bins[i + 1].toFixed(2)}`,
                count: analysisResult.histogram?.counts[i]
            }));

            return (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mt-6">
                    <h4 className="text-lg font-semibold mb-4">Distribution Analysis</h4>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={histData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="range" angle={-45} textAnchor="end" height={70} />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="count" fill="#4f46e5" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                        {Object.entries(analysisResult.stats).map(([key, val]: [string, any]) => (
                            <div key={key} className="p-3 bg-gray-50 rounded-lg">
                                <span className="text-xs text-gray-500 uppercase">{key}</span>
                                <p className="text-lg font-semibold text-gray-900">{typeof val === 'number' ? val.toFixed(2) : val}</p>
                            </div>
                        ))}
                    </div>
                </div>
            );
        } else if (analysisResult.type === 'numeric_numeric') {
            // Bivariate Numeric (Scatter + Correlation)
            return (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mt-6">
                    <div className="flex justify-between items-start mb-6">
                        <h4 className="text-lg font-semibold">Correlation Analysis</h4>
                        <div className={`px-4 py-2 rounded-lg ${analysisResult.significance === 'Significant' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                            <p className="text-sm font-medium">Correlation: {analysisResult.correlation?.toFixed(3)}</p>
                            <p className="text-xs opacity-75">p-value: {analysisResult.p_value?.toExponential(3)} ({analysisResult.significance})</p>
                        </div>
                    </div>
                    <div className="h-96">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart>
                                <CartesianGrid />
                                <XAxis type="number" dataKey={Object.keys(analysisResult.scatter_data![0])[0]} name="X" />
                                <YAxis type="number" dataKey={Object.keys(analysisResult.scatter_data![0])[1]} name="Y" />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                <Scatter data={analysisResult.scatter_data} fill="#8884d8" />
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            );
        } else if (analysisResult.correlation_matrix) {
            // Multivariate (Correlation Matrix)
            const matrix = analysisResult.correlation_matrix;
            const cols = Object.keys(matrix);

            return (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mt-6 overflow-x-auto">
                    <h4 className="text-lg font-semibold mb-4">Correlation Matrix</h4>
                    <table className="min-w-full text-sm text-left text-gray-500">
                        <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                            <tr>
                                <th className="px-6 py-3"></th>
                                {cols.map(c => <th key={c} className="px-6 py-3">{c}</th>)}
                            </tr>
                        </thead>
                        <tbody>
                            {cols.map(row => (
                                <tr key={row} className="bg-white border-b">
                                    <th className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap bg-gray-50">{row}</th>
                                    {cols.map(col => {
                                        const val = matrix[row][col];
                                        const p = analysisResult.p_values?.[row][col] || 0;
                                        const isSig = p < 0.05 && row !== col;
                                        const bg = val === null ? 'bg-gray-100' : val > 0.5 ? 'bg-indigo-100' : val < -0.5 ? 'bg-red-100' : 'bg-white';

                                        return (
                                            <td key={col} className={`px-6 py-4 ${bg}`}>
                                                <div className="flex flex-col items-center">
                                                    <span className="font-medium">{val?.toFixed(2) ?? '-'}</span>
                                                    {isSig && <span className="text-[10px] text-green-600 font-bold">* p&lt;0.05</span>}
                                                </div>
                                            </td>
                                        );
                                    })}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            );
        }

        return <div className="p-4 bg-yellow-50 text-yellow-700 rounded-lg mt-6">Analysis type visualization not implemented yet.</div>;
    };

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column: Stats & Insights */}
                <div className="lg:col-span-2 space-y-8">
                    {/* Quick Stats Cards */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-blue-100 rounded-lg">
                                    <Activity className="w-6 h-6 text-blue-600" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Total Rows</p>
                                    <p className="text-2xl font-bold text-gray-900">{stats.summary[Object.keys(stats.summary)[0]]?.count || 0}</p>
                                </div>
                            </div>
                        </div>
                        {/* Add more summary cards if needed */}
                    </div>

                    {/* Advanced Analysis Selector */}
                    <AnalysisSelector columns={columns} onAnalyze={handleAdvancedAnalysis} isAnalyzing={isAnalyzing} />

                    {/* Dynamic Analysis Result */}
                    {renderAnalysisResult()}

                    {/* Export Panel */}
                    <ExportPanel />

                </div>

                {/* Right Column: AI Insights */}
                <div className="space-y-6">
                    <div className="bg-gradient-to-br from-indigo-900 to-purple-900 rounded-2xl p-6 text-white shadow-xl">
                        <div className="flex items-center gap-3 mb-6">
                            <Lightbulb className="w-6 h-6 text-yellow-400" />
                            <h3 className="text-xl font-bold">AI Insights</h3>
                        </div>
                        <div className="space-y-4">
                            {insights.map((insight, index) => (
                                <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                                    <p className="text-sm leading-relaxed opacity-90">{insight}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
