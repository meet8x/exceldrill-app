import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const TermsOfService: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto bg-white p-8 rounded-xl shadow-sm">
                <div className="mb-8">
                    <Link to="/" className="flex items-center text-indigo-600 hover:text-indigo-800 mb-4">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Home
                    </Link>
                    <h1 className="text-3xl font-bold text-gray-900">Terms of Service</h1>
                    <p className="text-gray-500 mt-2">Last updated: {new Date().toLocaleDateString()}</p>
                </div>

                <div className="prose prose-indigo max-w-none">
                    <h3>1. Acceptance of Terms</h3>
                    <p>
                        By accessing or using Exceldrill AI, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.
                    </p>

                    <h3>2. Description of Service</h3>
                    <p>
                        Exceldrill AI provides automated data analysis and reporting tools. We reserve the right to modify or discontinue the service at any time.
                    </p>

                    <h3>3. User Responsibilities</h3>
                    <p>You are responsible for:</p>
                    <ul>
                        <li>Maintaining the confidentiality of your account credentials.</li>
                        <li>Ensuring you have the right to upload and analyze the data you submit.</li>
                        <li>Using the service in compliance with all applicable laws.</li>
                    </ul>

                    <h3>4. Payment and Refunds</h3>
                    <p>
                        Premium features are available for a one-time fee of ₹1999. Refunds are processed on a case-by-case basis within 7 days of purchase if the service does not work as described.
                    </p>

                    <h3>5. Limitation of Liability</h3>
                    <p>
                        Exceldrill AI is provided "as is" without warranties of any kind. We are not liable for any indirect, incidental, or consequential damages arising from your use of the service.
                    </p>

                    <h3>6. Contact Us</h3>
                    <p>
                        For any questions regarding these terms, please contact us at support@datainsight.ai.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default TermsOfService;
