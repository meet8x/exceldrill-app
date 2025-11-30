import React, { useState, useEffect } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

// Replace with your actual publishable key
const stripePromise = loadStripe('pk_test_TYooMQauvdEDq54NiTphI7jx');

const CheckoutForm = () => {
    const stripe = useStripe();
    const elements = useElements();
    const [error, setError] = useState<string | null>(null);
    const [processing, setProcessing] = useState(false);
    const { refreshUser } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!stripe || !elements) {
            return;
        }

        setProcessing(true);

        try {
            // 1. Create PaymentIntent
            const { data: { clientSecret } } = await axios.post('http://localhost:8000/api/payment/create-payment-intent', {
                amount: 900 // $9.00
            });

            // 2. Confirm Card Payment
            const result = await stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: elements.getElement(CardElement)!,
                },
            });

            if (result.error) {
                setError(result.error.message || 'Payment failed');
                setProcessing(false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // 3. Notify backend of success (In production, rely on Webhooks)
                    await axios.post('http://localhost:8000/api/payment/payment-success', {
                        paymentIntentId: result.paymentIntent.id
                    });

                    await refreshUser();
                    navigate('/');
                }
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'An error occurred');
            setProcessing(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-6 text-center">Unlock Full Access</h2>
            <p className="mb-4 text-center text-gray-600">Get unlimited report downloads for just <strong>$9.00</strong></p>
            <div className="mb-4 p-3 border rounded-md">
                <CardElement options={{
                    style: {
                        base: {
                            fontSize: '16px',
                            color: '#424770',
                            '::placeholder': {
                                color: '#aab7c4',
                            },
                        },
                        invalid: {
                            color: '#9e2146',
                        },
                    },
                }} />
            </div>
            {error && <div className="text-red-500 mb-4 text-sm">{error}</div>}
            <button
                type="submit"
                disabled={!stripe || processing}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
                {processing ? 'Processing...' : 'Pay $9.00'}
            </button>
        </form>
    );
};

const Payment = () => {
    return (
        <Elements stripe={stripePromise}>
            <div className="min-h-screen bg-gray-100 py-12">
                <CheckoutForm />
            </div>
        </Elements>
    );
};

export default Payment;
