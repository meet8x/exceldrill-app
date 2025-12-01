import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { client, googleLogin } from '../api/client';
import { useAuth } from '../context/AuthContext';

export const RegisterPage: React.FC = () => {
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleGoogleSuccess = async (credentialResponse: any) => {
        try {
            const response = await googleLogin(credentialResponse.credential);
            login(response.access_token);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Google registration failed');
        }
    };

    return (
        <div className="min-h-screen flex bg-gray-50">
            {/* Left Side - Features/Branding */}
            <div className="hidden lg:flex lg:w-1/2 bg-indigo-600 text-white flex-col justify-center px-12 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 to-purple-700 opacity-90"></div>

                {/* Decorative circles */}
                <div className="absolute top-0 left-0 w-64 h-64 bg-white opacity-10 rounded-full -translate-x-1/2 -translate-y-1/2 filter blur-3xl"></div>
                <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500 opacity-20 rounded-full translate-x-1/3 translate-y-1/3 filter blur-3xl"></div>

                <div className="relative z-10">
                    <div className="mb-8">
                        <span className="bg-indigo-500 bg-opacity-30 text-indigo-100 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider border border-indigo-400 border-opacity-30">
                            AI-Powered Analytics
                        </span>
                    </div>
                    <h1 className="text-5xl font-extrabold mb-6 leading-tight">
                        Unlock the Power <br />of Your Data
                    </h1>
                    <p className="text-xl text-indigo-100 mb-10 max-w-lg leading-relaxed">
                        Join thousands of analysts who use ExcelDrill AI to transform raw spreadsheets into actionable insights in seconds.
                    </p>

                    <div className="space-y-6">
                        <div className="flex items-start space-x-4 group">
                            <div className="bg-indigo-500 bg-opacity-20 p-3 rounded-xl group-hover:bg-opacity-30 transition-all duration-300">
                                <svg className="w-6 h-6 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg">Instant Analysis</h3>
                                <p className="text-indigo-200 text-sm">Get automated statistical insights instantly.</p>
                            </div>
                        </div>
                        <div className="flex items-start space-x-4 group">
                            <div className="bg-indigo-500 bg-opacity-20 p-3 rounded-xl group-hover:bg-opacity-30 transition-all duration-300">
                                <svg className="w-6 h-6 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg">Interactive Charts</h3>
                                <p className="text-indigo-200 text-sm">Visualize your data with dynamic graphs.</p>
                            </div>
                        </div>
                        <div className="flex items-start space-x-4 group">
                            <div className="bg-indigo-500 bg-opacity-20 p-3 rounded-xl group-hover:bg-opacity-30 transition-all duration-300">
                                <svg className="w-6 h-6 text-indigo-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                            </div>
                            <div>
                                <h3 className="font-semibold text-lg">One-Click Export</h3>
                                <p className="text-indigo-200 text-sm">Download reports in Word & PowerPoint.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="flex-1 flex items-center justify-center p-4 sm:px-6 lg:px-8 bg-white relative">
                {/* Mobile background decoration */}
                <div className="lg:hidden absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-500 to-purple-600"></div>

                <div className="max-w-md w-full space-y-8">
                    <div className="text-center">
                        <div className="mx-auto h-12 w-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4">
                            <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                            </svg>
                        </div>
                        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">Create your account</h2>
                        <p className="mt-2 text-sm text-gray-600">
                            Start your 7-day free trial. No credit card required.
                        </p>
                    </div>

                    <div className="mt-8 space-y-6">
                        <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 ring-1 ring-gray-900/5">
                            <div className="flex justify-center w-full mb-6">
                                <GoogleLogin
                                    onSuccess={handleGoogleSuccess}
                                    onError={() => setError('Google Sign-In failed')}
                                    text="signup_with"
                                    size="large"
                                    width="300"
                                    theme="filled_blue"
                                    shape="pill"
                                />
                            </div>

                            <div className="relative flex py-2 items-center">
                                <div className="flex-grow border-t border-gray-200"></div>
                                <span className="flex-shrink-0 mx-4 text-gray-400 text-xs uppercase tracking-wider">Trusted by Analysts</span>
                                <div className="flex-grow border-t border-gray-200"></div>
                            </div>

                            <p className="text-xs text-center text-gray-500 mt-4">
                                Secure login powered by Google Identity Services.
                            </p>
                        </div>

                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-md animate-pulse">
                                <div className="flex">
                                    <div className="flex-shrink-0">
                                        <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                        </svg>
                                    </div>
                                    <div className="ml-3">
                                        <p className="text-sm text-red-700">{error}</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="text-center text-xs text-gray-400">
                            By creating an account, you agree to our <Link to="/terms" className="underline hover:text-gray-600 transition-colors">Terms of Service</Link> and <Link to="/privacy" className="underline hover:text-gray-600 transition-colors">Privacy Policy</Link>.
                        </div>

                        <div className="text-center">
                            <span className="text-gray-600 text-sm">Already have an account? </span>
                            <Link to="/login" className="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors">
                                Sign in
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
