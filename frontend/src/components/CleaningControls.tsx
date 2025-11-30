import React, { useState } from 'react';
import { Eraser, Wand2, Trash2 } from 'lucide-react';

interface CleaningControlsProps {
    onClean: (action: string, params: any) => void;
    columns: string[];
}

export const CleaningControls: React.FC<CleaningControlsProps> = ({ onClean, columns }) => {
    const [selectedCol, setSelectedCol] = useState(columns[0] || '');
    const [imputeStrategy, setImputeStrategy] = useState('mean');
    const [fillValue, setFillValue] = useState('');

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <div className="flex items-center gap-2 mb-6">
                <Wand2 className="w-5 h-5 text-indigo-600" />
                <h3 className="text-lg font-semibold text-gray-900">Data Cleaning</h3>
            </div>

            <div className="space-y-6">
                {/* Basic Cleaning */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button
                        onClick={() => onClean('drop_nulls', {})}
                        className="flex items-center justify-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-700 transition-colors"
                    >
                        <Eraser className="w-4 h-4" />
                        Drop Missing Rows
                    </button>
                    <div className="flex gap-2">
                        <input
                            type="text"
                            placeholder="Value"
                            value={fillValue}
                            onChange={(e) => setFillValue(e.target.value)}
                            className="w-20 px-2 border border-gray-300 rounded-lg text-sm"
                        />
                        <button
                            onClick={() => onClean('fill_nulls', { value: fillValue })}
                            className="flex-1 flex items-center justify-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-700 transition-colors"
                        >
                            <Eraser className="w-4 h-4" />
                            Fill Missing
                        </button>
                    </div>
                </div>

                <div className="border-t border-gray-100 pt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Advanced Cleaning Target</label>
                    <select
                        value={selectedCol}
                        onChange={(e) => setSelectedCol(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md mb-4"
                    >
                        {columns.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Smart Imputation */}
                        <div className="p-3 border border-gray-200 rounded-lg">
                            <label className="block text-xs font-medium text-gray-500 mb-2">Smart Imputation</label>
                            <div className="flex gap-2">
                                <select
                                    value={imputeStrategy}
                                    onChange={(e) => setImputeStrategy(e.target.value)}
                                    className="flex-1 p-1 text-sm border border-gray-300 rounded"
                                >
                                    <option value="mean">Mean</option>
                                    <option value="median">Median</option>
                                </select>
                                <button
                                    onClick={() => onClean('smart_impute', { column: selectedCol, strategy: imputeStrategy })}
                                    className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded text-sm font-medium hover:bg-indigo-200"
                                >
                                    Apply
                                </button>
                            </div>
                        </div>

                        {/* Outlier Removal */}
                        <button
                            onClick={() => onClean('remove_outliers', { column: selectedCol, method: 'iqr' })}
                            className="flex items-center justify-center gap-2 p-3 border border-red-100 bg-red-50 rounded-lg hover:bg-red-100 text-red-700 transition-colors"
                        >
                            <Trash2 className="w-4 h-4" />
                            Remove Outliers (IQR)
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
