import React from 'react';
import { FileText, Presentation, FileSpreadsheet, Lock, Globe } from 'lucide-react';
import { downloadReport } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { ProgressBar } from './ProgressBar';

import { ColorSchemeSelector } from './ColorSchemeSelector';

export const ExportPanel: React.FC = () => {
    const { isPaid } = useAuth();
    const navigate = useNavigate();
    const [downloading, setDownloading] = React.useState(false);
    const [progress, setProgress] = React.useState(0);
    const [status, setStatus] = React.useState('');

    const handleDownload = async (format: 'word' | 'ppt' | 'excel' | 'html') => {
        setDownloading(true);
        setProgress(0);
        setStatus('Preparing report...');

        try {
            setStatus('Generating report...');
            await downloadReport(format, (p) => {
                setProgress(p);
                if (p < 20) setStatus('Analyzing data...');
                else if (p < 80) setStatus('Generating charts...');
                else if (p < 95) setStatus('Finalizing report...');
                else setStatus('Downloading...');
            });

            setProgress(100);
            setStatus('Download complete!');
            setTimeout(() => {
                setDownloading(false);
                setProgress(0);
                setStatus('');
            }, 1500);
        } catch (error) {
            setStatus('Download failed');
            setTimeout(() => {
                setDownloading(false);
                setProgress(0);
                setStatus('');
            }, 2000);
        }
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mt-6 flex flex-col gap-4">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-gray-800">Export Report</h3>
                    <p className="text-sm text-gray-500">Download comprehensive analysis reports.</p>
                </div>
                <div className="flex gap-4 items-center">
                    {isPaid && <ColorSchemeSelector />}
                    {!isPaid ? (
                        <button
                            onClick={() => navigate('/payment')}
                            className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg font-medium hover:from-purple-700 hover:to-indigo-700 transition-all shadow-md transform hover:scale-105"
                        >
                            Upgrade to Premium (₹1999)
                        </button>
                    ) : (
                        <>
                            <button
                                onClick={() => handleDownload('word')}
                                disabled={downloading}
                                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <FileText className="w-4 h-4" />
                                {downloading ? 'Downloading...' : 'Word Report'}
                            </button>
                            <button
                                onClick={() => handleDownload('ppt')}
                                disabled={downloading}
                                className="flex items-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg font-medium hover:bg-orange-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Presentation className="w-4 h-4" />
                                {downloading ? 'Downloading...' : 'PowerPoint'}
                            </button>
                            <button
                                onClick={() => handleDownload('excel')}
                                disabled={downloading}
                                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <FileSpreadsheet className="w-4 h-4" />
                                {downloading ? 'Downloading...' : 'Excel Report'}
                            </button>
                            <button
                                onClick={() => handleDownload('html')}
                                disabled={downloading}
                                className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Globe className="w-4 h-4" />
                                {downloading ? 'Downloading...' : 'Dashboard'}
                            </button>
                        </>
                    )}
                </div>
            </div>
            {downloading && <ProgressBar progress={progress} status={status} />}
        </div>
    );
};
