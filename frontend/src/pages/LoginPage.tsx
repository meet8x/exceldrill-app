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
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Welcome to ExcelDrill AI</h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        Sign in to access your dashboard
                    </p>
                </div>

                <div className="mt-8 space-y-6">
                    {/* Google Sign-In Button */}
                    <div className="flex justify-center w-full">
                        <div className="w-full flex justify-center">
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
                    </div>

                    {error && <div className="text-red-500 text-sm text-center bg-red-50 p-2 rounded">{error}</div>}

                    <div className="text-center text-xs text-gray-400 mt-4">
                        By signing in, you agree to our <Link to="/terms" className="underline hover:text-gray-600">Terms of Service</Link> and <Link to="/privacy" className="underline hover:text-gray-600">Privacy Policy</Link>.
                    </div>
                </div>
            </div>
        </div>
    );
};
