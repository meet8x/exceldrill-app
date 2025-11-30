import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
    return (
        <footer className="bg-gray-800 text-white mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* Company Info */}
                    <div>
                        <h3 className="text-lg font-semibold mb-4">Exceldrill AI</h3>
                        <p className="text-gray-300 text-sm mb-2">
                            Automated Data Analysis & Reporting Platform
                        </p>
                        <p className="text-gray-400 text-xs">
                            Billing Label: Exceldrill AI
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
                        <ul className="space-y-2 text-sm">
                            <li>
                                <Link to="/contact" className="text-gray-300 hover:text-white">
                                    Contact Us
                                </Link>
                            </li>
                            <li>
                                <Link to="/privacy" className="text-gray-300 hover:text-white">
                                    Privacy Policy
                                </Link>
                            </li>
                            <li>
                                <Link to="/terms" className="text-gray-300 hover:text-white">
                                    Terms of Service
                                </Link>
                            </li>
                            <li>
                                <Link to="/refund-policy" className="text-gray-300 hover:text-white">
                                    Refund & Cancellation Policy
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Contact Info */}
                    <div>
                        <h3 className="text-lg font-semibold mb-4">Contact</h3>
                        <p className="text-gray-300 text-sm">
                            3/38, Tirthnagar Society<br />
                            Near Kalupur Bank, Soal Road<br />
                            Ahmedabad - 380061<br />
                            Gujarat, India
                        </p>
                        <p className="text-gray-300 text-sm mt-3">
                            Email: support@exceldrill.ai
                        </p>
                    </div>
                </div>

                <div className="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
                    <p>&copy; {new Date().getFullYear()} Exceldrill AI. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
