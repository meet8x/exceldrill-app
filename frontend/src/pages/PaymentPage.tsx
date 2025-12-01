import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { client } from '../api/client';
import { useNavigate } from 'react-router-dom';

declare global {
    interface Window {
        Razorpay: any;
    }
}



const PLANS = [
    {
        id: '24h',
        name: '24-Hour Pass',
        price: 99,
        description: 'Perfect for a quick analysis.',
        features: ['24 hours access', 'Unlimited downloads', 'Basic support']
    },
    {
        id: 'monthly',
        name: 'Monthly Access',
        price: 499,
        description: 'Best for ongoing projects.',
        features: ['30 days access', 'Unlimited downloads', 'Priority support', 'Advanced insights']
    },
    {
        id: 'lifetime',
        name: 'Lifetime Access',
        price: 1999,
        description: 'One-time payment, forever access.',
        features: ['Lifetime access', 'All future updates', 'Premium support', 'Advanced insights']
    }
];

export const PaymentPage: React.FC = () => {
    const { user, refreshUser } = useAuth();
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handlePayment = async (planId: string, price: number) => {
        setLoading(true);
        try {
            // 1. Create Order
            const orderResponse = await client.post('/payment/create-order', { plan_id: planId });
            const { id: order_id, amount, currency, key_id } = orderResponse.data;

            // 2. Open Razorpay Modal
            const options = {
                key: key_id,
                amount: amount,
                currency: currency,
                name: "Exceldrill AI",
                description: `Premium Subscription - ${planId}`,
                order_id: order_id,
                handler: async function (response: any) {
                    // 3. Verify Payment
                    try {
                        await client.post('/payment/verify-payment', {
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature,
                            plan_id: planId
                        });
                        alert("Payment Successful! You are now a Premium user.");
                        await refreshUser();
                        navigate('/dashboard');
                    } catch (error) {
                        alert("Payment verification failed.");
                    }
                },
                prefill: {
                    name: user?.email,
                    email: user?.email,
                    contact: ""
                },
                theme: {
                    color: "#3399cc"
                }
            };

            const rzp1 = new window.Razorpay(options);
            rzp1.on('payment.failed', function (response: any) {
                alert(response.error.description);
            });
            rzp1.open();

        } catch (error) {
            console.error("Payment initiation failed", error);
            alert("Failed to initiate payment.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto text-center">
                <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                    Choose Your Plan
                </h2>
                <p className="mt-4 text-xl text-gray-600">
                    Unlock the full potential of your data.
                </p>
            </div>

            <div className="mt-12 space-y-4 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 lg:max-w-4xl lg:mx-auto xl:max-w-none xl:mx-0 xl:grid-cols-3">
                {PLANS.map((plan) => (
                    <div key={plan.id} className="border border-gray-200 rounded-lg shadow-sm divide-y divide-gray-200 bg-white flex flex-col">
                        <div className="p-6">
                            <h2 className="text-lg leading-6 font-medium text-gray-900">{plan.name}</h2>
                            <p className="mt-4 text-sm text-gray-500">{plan.description}</p>
                            <p className="mt-8">
                                <span className="text-4xl font-extrabold text-gray-900">₹{plan.price}</span>
                                <span className="text-base font-medium text-gray-500">{plan.id === 'monthly' ? '/mo' : ''}</span>
                            </p>
                            <button
                                onClick={() => handlePayment(plan.id, plan.price)}
                                disabled={loading}
                                className="mt-8 block w-full bg-indigo-600 border border-transparent rounded-md py-2 text-sm font-semibold text-white text-center hover:bg-indigo-700 disabled:opacity-50"
                            >
                                {loading ? 'Processing...' : `Get ${plan.name}`}
                            </button>
                        </div>
                        <div className="pt-6 pb-8 px-6">
                            <h3 className="text-xs font-medium text-gray-900 tracking-wide uppercase">What's included</h3>
                            <ul className="mt-6 space-y-4">
                                {plan.features.map((feature) => (
                                    <li key={feature} className="flex space-x-3">
                                        <svg className="flex-shrink-0 h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        <span className="text-sm text-gray-500">{feature}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
