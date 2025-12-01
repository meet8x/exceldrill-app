import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../context/AuthContext';
import { client, googleLogin } from '../api/client';

export const LoginPage: React.FC = () => {
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleGoogleSuccess = async (credentialResponse: any) => {
        try {
            const response = await googleLogin(credentialResponse.credential);
            login(response.access_token);
            navigate('/dashboard');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Google login failed');
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
                    <h1 className="text-5xl font-extrabold mb-6 leading-tight">
                        Welcome Back <br />to ExcelDrill AI
                    </h1>
                    <p className="text-xl text-indigo-100 mb-10 max-w-lg leading-relaxed">
                        Continue analyzing your data and generating professional reports with ease.
                    </p>

                    <div className="grid grid-cols-2 gap-6">
                        <div className="bg-white bg-opacity-10 p-4 rounded-xl backdrop-blur-sm">
                            <div className="text-3xl font-bold mb-1">10k+</div>
                            <div className="text-indigo-200 text-sm">Reports Generated</div>
                        </div>
                        <div className="bg-white bg-opacity-10 p-4 rounded-xl backdrop-blur-sm">
                            <div className="text-3xl font-bold mb-1">99%</div>
                            <div className="text-indigo-200 text-sm">Customer Satisfaction</div>
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                            </svg>
                        </div>
                        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">Sign in to your account</h2>
                        <p className="mt-2 text-sm text-gray-600">
                            Access your dashboard and saved reports
                        </p>
                    </div>

                    <div className="mt-8 space-y-6">
                        <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 ring-1 ring-gray-900/5">
                            <div className="flex justify-center w-full mb-6">
                                <GoogleLogin
                                    onSuccess={handleGoogleSuccess}
                                    onError={() => setError('Google Sign-In failed')}
                                    useOneTap
                                    size="large"
                                    width="300"
                                    theme="filled_blue"
                                    shape="pill"
                                />
                            </div>

                            <div className="relative flex py-2 items-center">
                                <div className="flex-grow border-t border-gray-200"></div>
                                <span className="flex-shrink-0 mx-4 text-gray-400 text-xs uppercase tracking-wider">Secure Access</span>
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
                            By signing in, you agree to our <Link to="/terms" className="underline hover:text-gray-600 transition-colors">Terms of Service</Link> and <Link to="/privacy" className="underline hover:text-gray-600 transition-colors">Privacy Policy</Link>.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
