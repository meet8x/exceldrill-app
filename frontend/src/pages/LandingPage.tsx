import React from 'react';
import { Link } from 'react-router-dom';
import { BarChart3, FileText, Shield, Zap, CheckCircle, ArrowRight } from 'lucide-react';
import Footer from '../components/Footer';

export const LandingPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
            {/* Navigation */}
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex justify-between items-center">
                        <div className="flex items-center gap-3">
                            <div className="bg-indigo-600 p-2 rounded-lg">
                                <BarChart3 className="w-6 h-6 text-white" />
                            </div>
                            <h1 className="text-2xl font-bold text-gray-900">Exceldrill AI</h1>
                        </div>
                        <div className="flex items-center gap-4">
                            <Link to="/login" className="text-gray-600 hover:text-gray-900">
                                Login
                            </Link>
                            <Link
                                to="/register"
                                className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
                            >
                                Get Started
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="text-center">
                    <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6">
                        Automated Data Analysis
                        <span className="block text-indigo-600">Made Simple</span>
                    </h1>
                    <p className="text-xl text-gray-600 mb-4 max-w-3xl mx-auto">
                        Upload your dataset and get comprehensive Word & PowerPoint reports instantly.
                        No coding required. Powered by AI.
                    </p>
                    <p className="text-lg text-indigo-600 font-semibold mb-8 max-w-3xl mx-auto">
                        ✨ Get editable Word & PPT reports with graphs, analyzed Excel files, and ready-made interactive dashboards
                    </p>
                    <div className="flex justify-center gap-4">
                        <Link
                            to="/register"
                            className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition flex items-center gap-2"
                        >
                            Start Now
                            <ArrowRight className="w-5 h-5" />
                        </Link>
                        <Link
                            to="/login"
                            className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold border-2 border-indigo-600 hover:bg-indigo-50 transition"
                        >
                            Sign In
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
                    Why Choose Exceldrill AI?
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
                        <div className="bg-indigo-100 w-16 h-16 rounded-lg flex items-center justify-center mb-4">
                            <Zap className="w-8 h-8 text-indigo-600" />
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-3">Lightning Fast</h3>
                        <p className="text-gray-600">
                            Get comprehensive analysis reports in seconds. No waiting, no hassle.
                        </p>
                    </div>

                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
                        <div className="bg-purple-100 w-16 h-16 rounded-lg flex items-center justify-center mb-4">
                            <FileText className="w-8 h-8 text-purple-600" />
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-3">Professional Reports</h3>
                        <p className="text-gray-600">
                            Download editable Word, PowerPoint, Excel, and HTML reports instantly.
                        </p>
                    </div>

                    <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition">
                        <div className="bg-green-100 w-16 h-16 rounded-lg flex items-center justify-center mb-4">
                            <Shield className="w-8 h-8 text-green-600" />
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-3">Secure & Private</h3>
                        <p className="text-gray-600">
                            Your data is encrypted and secure. We never share your information.
                        </p>
                    </div>
                </div>
            </section>

            {/* Pricing Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
                    Choose Your Plan
                </h2>
                <p className="text-center text-gray-600 mb-12">Flexible options for every need</p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* 24-Hour Pass */}
                    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border-2 border-gray-200">
                        <div className="bg-gray-100 text-gray-800 text-center py-4">
                            <p className="text-sm font-semibold uppercase">24-Hour Pass</p>
                        </div>
                        <div className="p-8">
                            <p className="text-center text-gray-600 mb-6">Perfect for a quick analysis</p>
                            <div className="text-center mb-6">
                                <p className="text-5xl font-bold text-gray-900">₹99</p>
                                <p className="text-gray-600 mt-2">24 hours access</p>
                            </div>
                            <ul className="space-y-4 mb-8">
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">24 hours access</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Unlimited downloads</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Basic support</span>
                                </li>
                            </ul>
                            <Link
                                to="/register"
                                className="block w-full bg-gray-600 text-white text-center py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
                            >
                                Get 24-Hour Pass
                            </Link>
                        </div>
                    </div>

                    {/* Monthly Access */}
                    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border-2 border-gray-200">
                        <div className="bg-blue-600 text-white text-center py-4">
                            <p className="text-sm font-semibold uppercase">Monthly Access</p>
                        </div>
                        <div className="p-8">
                            <p className="text-center text-gray-600 mb-6">Best for ongoing projects</p>
                            <div className="text-center mb-6">
                                <p className="text-5xl font-bold text-gray-900">₹499</p>
                                <p className="text-gray-600 mt-2">per month</p>
                            </div>
                            <ul className="space-y-4 mb-8">
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">30 days access</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Unlimited downloads</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Priority support</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Advanced insights</span>
                                </li>
                            </ul>
                            <Link
                                to="/register"
                                className="block w-full bg-blue-600 text-white text-center py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
                            >
                                Get Monthly Access
                            </Link>
                        </div>
                    </div>

                    {/* Lifetime Access - Featured */}
                    <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border-4 border-indigo-600 transform md:scale-105">
                        <div className="bg-indigo-600 text-white text-center py-4">
                            <p className="text-sm font-semibold uppercase">Lifetime Access ⭐ Best Value</p>
                        </div>
                        <div className="p-8">
                            <p className="text-center text-gray-600 mb-6">Pay once, use forever</p>
                            <div className="text-center mb-6">
                                <p className="text-5xl font-bold text-gray-900">₹1,999</p>
                                <p className="text-gray-600 mt-2">One-time payment</p>
                                <p className="text-sm text-green-600 mt-1">✓ No monthly fees ever</p>
                            </div>
                            <ul className="space-y-4 mb-8">
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700"><strong>Editable Word Reports</strong></span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700"><strong>PowerPoint with charts</strong></span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700"><strong>Analyzed Excel files</strong></span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700"><strong>HTML Dashboards</strong></span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Unlimited downloads</span>
                                </li>
                                <li className="flex items-center gap-3">
                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                    <span className="text-gray-700">Priority support</span>
                                </li>
                            </ul>
                            <Link
                                to="/register"
                                className="block w-full bg-indigo-600 text-white text-center py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition mb-4"
                            >
                                Get Lifetime Access
                            </Link>
                            <p className="text-center text-sm text-gray-500">
                                Secure payment via Razorpay
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Quick Links Section */}
            <section className="bg-gray-50 py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
                        Important Information
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <Link
                            to="/contact"
                            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
                        >
                            <h3 className="font-semibold text-gray-900 mb-2">Contact Us</h3>
                            <p className="text-sm text-gray-600">Get in touch with our team</p>
                        </Link>
                        <Link
                            to="/privacy"
                            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
                        >
                            <h3 className="font-semibold text-gray-900 mb-2">Privacy Policy</h3>
                            <p className="text-sm text-gray-600">How we protect your data</p>
                        </Link>
                        <Link
                            to="/terms"
                            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
                        >
                            <h3 className="font-semibold text-gray-900 mb-2">Terms of Service</h3>
                            <p className="text-sm text-gray-600">Our terms and conditions</p>
                        </Link>
                        <Link
                            to="/refund-policy"
                            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition text-center"
                        >
                            <h3 className="font-semibold text-gray-900 mb-2">Refund Policy</h3>
                            <p className="text-sm text-gray-600">Our refund terms</p>
                        </Link>
                    </div>
                </div>
            </section>

            <Footer />
        </div>
    );
};
