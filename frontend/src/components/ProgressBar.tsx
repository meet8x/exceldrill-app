import React from 'react';

interface ProgressBarProps {
    progress: number; // 0-100
    status?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ progress, status }) => {
    return (
        <div className="w-full max-w-md mx-auto mt-4">
            <div className="relative pt-1">
                <div className="flex mb-2 items-center justify-between">
                    <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-blue-600 bg-blue-200">
                            {status || 'Generating Report'}
                        </span>
                    </div>
                    <div className="text-right">
                        <span className="text-xs font-semibold inline-block text-blue-600">
                            {progress}%
                        </span>
                    </div>
                </div>
                <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-blue-200">
                    <div
                        style={{ width: `${progress}%` }}
                        className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-300 ease-out"
                    ></div>
                </div>
                {status && (
                    <p className="text-xs text-gray-600 text-center">{status}</p>
                )}
            </div>
        </div>
    );
};
