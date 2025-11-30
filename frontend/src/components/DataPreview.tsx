import React from 'react';
import { DataPreview as DataPreviewType } from '../api/types';

interface DataPreviewProps {
    data: DataPreviewType | null;
}

export const DataPreview: React.FC<DataPreviewProps> = ({ data }) => {
    if (!data) return null;

    return (
        <div className="w-full overflow-hidden rounded-xl shadow-sm border border-gray-200 bg-white mt-8">
            <div className="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <h3 className="font-semibold text-gray-800">Data Preview</h3>
                <span className="text-sm text-gray-500">{data.total_rows} rows • {data.columns.length} columns</span>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-600">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 border-b">
                        <tr>
                            {data.columns.map((col) => (
                                <th key={col} className="px-6 py-3 font-medium whitespace-nowrap">
                                    {col}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.data.map((row, idx) => (
                            <tr key={idx} className="bg-white border-b hover:bg-gray-50">
                                {data.columns.map((col) => (
                                    <td key={`${idx}-${col}`} className="px-6 py-4 whitespace-nowrap">
                                        {row[col] !== null ? String(row[col]) : <span className="text-gray-300 italic">null</span>}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
