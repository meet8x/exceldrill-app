import { Link } from 'react-router-dom';
import { Mail, MapPin } from 'lucide-react';

const ContactUs: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="bg-white shadow rounded-lg p-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-6">Contact Us</h1>

                    <div className="prose prose-indigo max-w-none">
                        <p className="text-lg text-gray-600 mb-8">
                            We're here to help! If you have any questions, feedback, or need support, please don't hesitate to reach out.
                        </p>

                        <div className="space-y-6">
                            <div className="flex items-start gap-4">
                                <Mail className="w-6 h-6 text-indigo-600 mt-1" />
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900">Email</h3>
                                    <p className="text-gray-600">support@exceldrill.ai</p>
                                    <p className="text-sm text-gray-500">We typically respond within 24 hours</p>
                                </div>
                            </div>

                            <div className="flex items-start gap-4">
                                <MapPin className="w-6 h-6 text-indigo-600 mt-1" />
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900">Address</h3>
                                    <p className="text-gray-600">
                                        Exceldrill AI<br />
                                        3/38, Tirthnagar Society<br />
                                        Near Kalupur Bank, Soal Road<br />
                                        Ahmedabad - 380061<br />
                                        Gujarat, India
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 pt-8 border-t border-gray-200">
                            <h3 className="text-xl font-semibold text-gray-900 mb-4">Business Hours</h3>
                            <p className="text-gray-600">
                                Monday - Friday: 9:00 AM - 6:00 PM IST<br />
                                Saturday: 10:00 AM - 4:00 PM IST<br />
                                Sunday: Closed
                            </p>
                        </div>

                        <div className="mt-8 pt-8 border-t border-gray-200">
                            <h3 className="text-xl font-semibold text-gray-900 mb-4">Support</h3>
                            <p className="text-gray-600">
                                For technical support, billing inquiries, or general questions, please email us at{' '}
                                <a href="mailto:support@exceldrill.ai" className="text-indigo-600 hover:text-indigo-500">
                                    support@exceldrill.ai
                                </a>
                            </p>
                        </div>
                    </div>

                    <div className="mt-8">
                        <Link to="/" className="text-indigo-600 hover:text-indigo-500">
                            ← Back to Home
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ContactUs;
