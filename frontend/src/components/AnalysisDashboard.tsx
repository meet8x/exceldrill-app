import { useState } from 'react';
import { FileUpload } from './FileUpload';
import { uploadFile, analyzeData, getInsights, downloadReport } from '../api/client';
import { BarChart3, FileText, Presentation, FileSpreadsheet, CheckCircle2, Loader2, Lock, Globe } from 'lucide-react';
import { DataPreview } from './DataPreview';
import { InsightsView } from './InsightsView';
import { DataPreview as DataPreviewType } from '../api/types';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import Footer from './Footer';

export function AnalysisDashboard() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState<'upload' | 'processing' | 'ready'>('upload');
    const [previewData, setPreviewData] = useState<DataPreviewType | null>(null);
    const [insights, setInsights] = useState<string[]>([]);

    const { isPaid, logout, user } = useAuth();
    const navigate = useNavigate();

    const handleUpload = async (uploadedFile: File) => {
        setLoading(true);
        try {
            const response = await uploadFile(uploadedFile);
            setFile(uploadedFile);
            if (response.preview) {
                setPreviewData(response.preview);
            }
            setStep('processing');

            // Auto-trigger analysis to ensure backend is ready
            await analyzeData();
            const insightsData = await getInsights();
            if (insightsData && insightsData.insights) {
                setInsights(insightsData.insights);
            }

            setStep('ready');
        } catch (error) {
            console.error("Upload failed", error);
            alert("Upload failed. Please try again.");
            setStep('upload');
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = (format: 'word' | 'ppt' | 'excel' | 'html') => {
        if (!isPaid) {
            if (confirm("This feature is available for premium users only. Unlock Lifetime Access for ₹1999?")) {
                navigate('/payment');
            }
            return;
        }
        downloadReport(format);
    };

    return (
        <div className="min-h-screen bg-gray-50 pb-20 font-sans">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="bg-indigo-600 p-2 rounded-lg">
                            <BarChart3 className="w-6 h-6 text-white" />
                        </div>
                        <h1 className="text-xl font-bold text-gray-900">Exceldrill AI</h1>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-600">
                            {user?.email} ({isPaid ? 'Premium' : 'Free'})
                        </span>
                        {!isPaid && (
                            <button
                                onClick={() => navigate('/payment')}
                                className="text-sm bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                            >
                                Upgrade
                            </button>
                        )}
                        <button onClick={logout} className="text-sm text-gray-500 hover:text-gray-900">Logout</button>
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 py-12">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">
                        Automated Data Analysis & Reporting
                    </h2>
                    <p className="text-lg text-gray-600">
                        Upload your dataset and get comprehensive Word & PowerPoint reports instantly.
                    </p>
                </div>

                <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                    {step === 'upload' && (
                        <div className="animate-in fade-in zoom-in duration-500">
                            <FileUpload onUpload={handleUpload} isUploading={loading} />
                        </div>
                    )}

                    {step === 'processing' && (
                        <div className="flex flex-col items-center justify-center py-12 animate-in fade-in duration-500">
                            <Loader2 className="w-16 h-16 text-indigo-600 animate-spin mb-6" />
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Processing Data...</h3>
                            <p className="text-gray-500">Running univariate, bivariate, and multivariate analysis.</p>
                        </div>
                    )}

                    {step === 'ready' && (
                        <div className="text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-6">
                                <CheckCircle2 className="w-8 h-8 text-green-600" />
                            </div>
                            <h3 className="text-2xl font-bold text-gray-900 mb-2">Analysis Complete!</h3>
                            <p className="text-gray-600 mb-8">
                                Your reports are ready. Download them below.
                            </p>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto mb-12">
                                <button
                                    onClick={() => handleDownload('word')}
                                    className="relative flex flex-col items-center p-6 border-2 border-blue-100 bg-blue-50 rounded-xl hover:bg-blue-100 hover:border-blue-200 transition-all group"
                                >
                                    {!isPaid && <div className="absolute top-2 right-2"><Lock className="w-5 h-5 text-gray-400" /></div>}
                                    <div className="p-4 bg-white rounded-full shadow-sm mb-4 group-hover:scale-110 transition-transform">
                                        <FileText className="w-8 h-8 text-blue-600" />
                                    </div>
                                    <span className="text-lg font-semibold text-blue-900">Download Word Report</span>
                                    <span className="text-sm text-blue-600 mt-1">Detailed analysis & stats</span>
                                </button>

                                <button
                                    onClick={() => handleDownload('ppt')}
                                    className="relative flex flex-col items-center p-6 border-2 border-orange-100 bg-orange-50 rounded-xl hover:bg-orange-100 hover:border-orange-200 transition-all group"
                                >
                                    {!isPaid && <div className="absolute top-2 right-2"><Lock className="w-5 h-5 text-gray-400" /></div>}
                                    <div className="p-4 bg-white rounded-full shadow-sm mb-4 group-hover:scale-110 transition-transform">
                                        <Presentation className="w-8 h-8 text-orange-600" />
                                    </div>
                                    <span className="text-lg font-semibold text-orange-900">Download PowerPoint</span>
                                    <span className="text-sm text-orange-600 mt-1">Presentation ready slides</span>
                                </button>

                                <button
                                    onClick={() => handleDownload('excel')}
                                    className="relative flex flex-col items-center p-6 border-2 border-green-100 bg-green-50 rounded-xl hover:bg-green-100 hover:border-green-200 transition-all group"
                                >
                                    {!isPaid && <div className="absolute top-2 right-2"><Lock className="w-5 h-5 text-gray-400" /></div>}
                                    <div className="p-4 bg-white rounded-full shadow-sm mb-4 group-hover:scale-110 transition-transform">
                                        <FileSpreadsheet className="w-8 h-8 text-green-600" />
                                    </div>
                                    <span className="text-lg font-semibold text-green-900">Download Excel</span>
                                    <span className="text-sm text-green-600 mt-1">Multi-sheet workbook</span>
                                </button>

                                <button
                                    onClick={() => handleDownload('html')}
                                    className="relative flex flex-col items-center p-6 border-2 border-purple-100 bg-purple-50 rounded-xl hover:bg-purple-100 hover:border-purple-200 transition-all group"
                                >
                                    {!isPaid && <div className="absolute top-2 right-2"><Lock className="w-5 h-5 text-gray-400" /></div>}
                                    <div className="p-4 bg-white rounded-full shadow-sm mb-4 group-hover:scale-110 transition-transform">
                                        <Globe className="w-8 h-8 text-purple-600" />
                                    </div>
                                    <span className="text-lg font-semibold text-purple-900">Download Dashboard</span>
                                    <span className="text-sm text-purple-600 mt-1">Interactive HTML</span>
                                </button>
                            </div>

                            <div className="text-left">
                                <InsightsView insights={insights} />
                                <DataPreview data={previewData} />
                            </div>

                            <button
                                onClick={() => {
                                    setFile(null);
                                    setStep('upload');
                                    setPreviewData(null);
                                    setInsights([]);
                                }}
                                className="mt-12 text-gray-500 hover:text-gray-700 underline"
                            >
                                Analyze another file
                            </button>
                        </div>
                    )}
                </div>
            </main>
            <Footer />
        </div>
    );
}
