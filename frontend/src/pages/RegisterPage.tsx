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
                            <div className="relative z-10">
                                <h1 className="text-4xl font-bold mb-6">Unlock the Power of Your Data</h1>
                                <p className="text-lg text-indigo-100 mb-8">
                                    Join thousands of analysts who use ExcelDrill AI to transform raw spreadsheets into actionable insights in seconds.
                                </p>

                                <div className="space-y-4">
                                    <div className="flex items-center space-x-3">
                                        <div className="bg-indigo-500 p-2 rounded-full">
                                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                        </div>
                                        <span className="text-indigo-50">Automated Statistical Analysis</span>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <div className="bg-indigo-500 p-2 rounded-full">
                                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                                        </div>
                                        <span className="text-indigo-50">Interactive Visualizations</span>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <div className="bg-indigo-500 p-2 rounded-full">
                                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                                        </div>
                                        <span className="text-indigo-50">Export to Word & PowerPoint</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Right Side - Login Form */}
                        <div className="flex-1 flex items-center justify-center p-4 sm:px-6 lg:px-8 bg-white">
                            <div className="max-w-md w-full space-y-8">
                                <div className="text-center">
                                    <h2 className="text-3xl font-extrabold text-gray-900">Create your account</h2>
                                    <p className="mt-2 text-sm text-gray-600">
                                        Start your 7-day free trial. No credit card required.
                                    </p>
                                </div>

                                <div className="mt-8 space-y-6">
                                    <div className="bg-gray-50 p-6 rounded-lg border border-gray-100">
                                        <div className="flex justify-center w-full mb-4">
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
                                        <p className="text-xs text-center text-gray-500">
                                            Secure login powered by Google
                                        </p>
                                    </div>

                                    {error && (
                                        <div className="bg-red-50 border-l-4 border-red-400 p-4">
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
                                        By creating an account, you agree to our <Link to="/terms" className="underline hover:text-gray-600">Terms of Service</Link> and <Link to="/privacy" className="underline hover:text-gray-600">Privacy Policy</Link>.
                                    </div>

                                    <div className="text-center">
                                        <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
                                            Already have an account? Sign in
                                        </Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };
