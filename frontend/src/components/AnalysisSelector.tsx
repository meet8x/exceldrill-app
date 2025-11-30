import React, { useState } from 'react';
import { AnalysisConfig } from '../api/types';
import { BarChart2, GitMerge, Network } from 'lucide-react';

interface AnalysisSelectorProps {
    columns: string[];
    onAnalyze: (config: AnalysisConfig) => void;
    isAnalyzing: boolean;
}

export const AnalysisSelector: React.FC<AnalysisSelectorProps> = ({ columns, onAnalyze, isAnalyzing }) => {
    const [analysisType, setAnalysisType] = useState<'univariate' | 'bivariate' | 'multivariate'>('univariate');
    const [selectedCols, setSelectedCols] = useState<string[]>([]);

    const handleColToggle = (col: string) => {
        if (analysisType === 'univariate') {
            setSelectedCols([col]);
        } else if (analysisType === 'bivariate') {
            if (selectedCols.includes(col)) {
                setSelectedCols(selectedCols.filter(c => c !== col));
            } else if (selectedCols.length < 2) {
                setSelectedCols([...selectedCols, col]);
            }
        } else {
            // Multivariate
            if (selectedCols.includes(col)) {
                setSelectedCols(selectedCols.filter(c => c !== col));
            } else {
                setSelectedCols([...selectedCols, col]);
            }
        }
    };

    const isValid = () => {
        if (analysisType === 'univariate') return selectedCols.length === 1;
        if (analysisType === 'bivariate') return selectedCols.length === 2;
        if (analysisType === 'multivariate') return selectedCols.length >= 2;
        return false;
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Advanced Analysis</h3>

            {/* Type Selection */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                <button
                    onClick={() => { setAnalysisType('univariate'); setSelectedCols([]); }}
                    className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all ${analysisType === 'univariate'
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                            : 'border-gray-200 hover:border-gray-300 text-gray-600'
                        }`}
                >
                    <BarChart2 className="w-6 h-6 mb-2" />
                    <span className="font-medium">Univariate</span>
                    <span className="text-xs mt-1 opacity-75">Single Variable</span>
                </button>
                <button
                    onClick={() => { setAnalysisType('bivariate'); setSelectedCols([]); }}
                    className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all ${analysisType === 'bivariate'
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                            : 'border-gray-200 hover:border-gray-300 text-gray-600'
                        }`}
                >
                    <GitMerge className="w-6 h-6 mb-2" />
                    <span className="font-medium">Bivariate</span>
                    <span className="text-xs mt-1 opacity-75">Two Variables</span>
                </button>
                <button
                    onClick={() => { setAnalysisType('multivariate'); setSelectedCols([]); }}
                    className={`flex flex-col items-center p-4 rounded-lg border-2 transition-all ${analysisType === 'multivariate'
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                            : 'border-gray-200 hover:border-gray-300 text-gray-600'
                        }`}
                >
                    <Network className="w-6 h-6 mb-2" />
                    <span className="font-medium">Multivariate</span>
                    <span className="text-xs mt-1 opacity-75">Multiple Variables</span>
                </button>
            </div>

            {/* Column Selection */}
            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Columns {analysisType === 'bivariate' ? '(Select 2)' : analysisType === 'univariate' ? '(Select 1)' : '(Select 2+)'}
                </label>
                <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto p-2 border border-gray-200 rounded-lg">
                    {columns.map(col => (
                        <button
                            key={col}
                            onClick={() => handleColToggle(col)}
                            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${selectedCols.includes(col)
                                    ? 'bg-indigo-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            {col}
                        </button>
                    ))}
                </div>
            </div>

            <button
                onClick={() => onAnalyze({ type: analysisType, columns: selectedCols })}
                disabled={!isValid() || isAnalyzing}
                className="w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold shadow-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
                {isAnalyzing ? 'Running Analysis...' : 'Run Analysis'}
            </button>
        </div>
    );
};
