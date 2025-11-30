import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const PrivacyPolicy: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto bg-white p-8 rounded-xl shadow-sm">
                <div className="mb-8">
                    <Link to="/" className="flex items-center text-indigo-600 hover:text-indigo-800 mb-4">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Home
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900">Privacy Policy</h1>
                    <p className="text-gray-500 mt-2">Last updated: {new Date().toLocaleDateString()}</p>
                </div>

                <div className="prose prose-indigo max-w-none">
                    <h3>1. Introduction</h3>
                    <p>
                        Welcome to Exceldrill AI ("we," "our," or "us"). We are committed to protecting your privacy and ensuring the security of your data.
                        This Privacy Policy explains how we collect, use, and safeguard your information when you use our data analysis platform.
                    </p>

                    <h3>2. Information We Collect</h3>
                    <p>We collect the following types of information:</p>
                    <ul>
                        <li><strong>Account Information:</strong> Name, email address, and password when you register.</li>
                        <li><strong>User Content:</strong> Data files (CSV, Excel) you upload for analysis.</li>
                        <li><strong>Usage Data:</strong> Information about how you interact with our platform.</li>
                    </ul>

                    <h3>3. How We Use Your Information</h3>
                    <p>We use your information to:</p>
                    <ul>
                        <li>Provide and improve our data analysis services.</li>
                        <li>Process payments and manage your subscription.</li>
                        <li>Send you important updates and reports.</li>
                        <li>Ensure the security of our platform.</li>
                    </ul>

                    <h3>4. Data Security</h3>
                    <p>
                        We implement industry-standard security measures to protect your data. Your uploaded files are processed securely and are not shared with third parties
                        except as necessary to provide our services (e.g., cloud storage providers).
                    </p>

                    <h3>5. Contact Us</h3>
                    <p>
                        If you have any questions about this Privacy Policy, please contact us at support@exceldrill.app.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default PrivacyPolicy;
