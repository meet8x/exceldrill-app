import React from 'react';
import { Lightbulb } from 'lucide-react';

interface InsightsViewProps {
    insights: string[];
}

export const InsightsView: React.FC<InsightsViewProps> = ({ insights }) => {
    if (!insights || insights.length === 0) return null;

    return (
        <div className="w-full rounded-xl shadow-sm border border-indigo-100 bg-indigo-50/50 mt-8 p-6">
            <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="w-6 h-6 text-indigo-600" />
                <h3 className="text-lg font-semibold text-indigo-900">AI-Generated Insights</h3>
            </div>
            <ul className="space-y-3">
                {insights.map((insight, idx) => (
                    <li key={idx} className="flex items-start gap-3 bg-white p-4 rounded-lg border border-indigo-100 shadow-sm">
                        <span className="flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-full bg-indigo-100 text-indigo-600 font-bold text-xs mt-0.5">
                            {idx + 1}
                        </span>
                        <p className="text-gray-700 leading-relaxed">{insight}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};
