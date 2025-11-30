import React from 'react';
import { Link } from 'react-router-dom';

const RefundPolicy: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="bg-white shadow rounded-lg p-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-6">Refund & Cancellation Policy</h1>

                    <div className="prose prose-indigo max-w-none">
                        <p className="text-gray-600 mb-6">
                            Last updated: {new Date().toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })}
                        </p>

                        <h3>1. Refund Policy</h3>
                        <p>
                            At Exceldrill AI, we strive to provide the best service possible. However, we understand that circumstances may arise where you need a refund.
                        </p>

                        <h3>2. Eligibility for Refunds</h3>
                        <p>
                            You may be eligible for a refund under the following conditions:
                        </p>
                        <ul>
                            <li>Technical issues that prevent you from using the service</li>
                            <li>Duplicate payments made by error</li>
                            <li>Service not delivered as described</li>
                            <li>Request made within 7 days of purchase</li>
                        </ul>

                        <h3>3. Non-Refundable Situations</h3>
                        <p>
                            Refunds will not be provided in the following cases:
                        </p>
                        <ul>
                            <li>Change of mind after using the service</li>
                            <li>Failure to use the service within the subscription period</li>
                            <li>Violation of our Terms of Service</li>
                            <li>Requests made after 7 days of purchase</li>
                        </ul>

                        <h3>4. Refund Process</h3>
                        <p>
                            To request a refund:
                        </p>
                        <ol>
                            <li>Email us at support@exceldrill.app with your order details</li>
                            <li>Provide a reason for the refund request</li>
                            <li>Include your transaction ID and registered email</li>
                            <li>Our team will review your request within 3-5 business days</li>
                        </ol>

                        <h3>5. Refund Timeline</h3>
                        <p>
                            Once approved, refunds will be processed within 7-10 business days. The refund will be credited to the original payment method used during purchase.
                        </p>

                        <h3>6. Cancellation Policy</h3>
                        <p>
                            For lifetime access plans, cancellation is not applicable as it's a one-time payment. However, you can request account deletion at any time by contacting support@exceldrill.app.
                        </p>

                        <h3>7. Partial Refunds</h3>
                        <p>
                            In some cases, partial refunds may be granted at our discretion based on usage and circumstances.
                        </p>

                        <h3>8. Contact Us</h3>
                        <p>
                            For any refund or cancellation queries, please contact us at:
                        </p>
                        <p>
                            Email: support@exceldrill.app<br />
                            Response Time: Within 24-48 hours
                        </p>
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

export default RefundPolicy;
