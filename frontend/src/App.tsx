import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ErrorBoundary } from './components/ErrorBoundary';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { PaymentPage } from './pages/PaymentPage';
import { VerifyEmailPage } from './pages/VerifyEmailPage';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import { AdminDashboard } from './pages/AdminDashboard';
import PrivacyPolicy from './components/PrivacyPolicy';
import TermsOfService from './components/TermsOfService';
import ContactUs from './components/ContactUs';
import RefundPolicy from './components/RefundPolicy';

const GOOGLE_CLIENT_ID = "90600034364-o8r416gis9gqplo3ldt0a4tbpdonbm4q.apps.googleusercontent.com";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
    const { isAuthenticated } = useAuth();
    const token = localStorage.getItem('token');
    if (!isAuthenticated && !token) {
        return <Navigate to="/login" />;
    }
    return children;
};

function App() {
    return (
        <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
            <AuthProvider>
                <ErrorBoundary>
                    <Router>
                        <Routes>
                            <Route path="/" element={<LandingPage />} />
                            <Route path="/login" element={<LoginPage />} />
                            <Route path="/register" element={<RegisterPage />} />
                            <Route path="/verify-email" element={<VerifyEmailPage />} />
                            <Route path="/privacy" element={<PrivacyPolicy />} />
                            <Route path="/terms" element={<TermsOfService />} />
                            <Route path="/contact" element={<ContactUs />} />
                            <Route path="/refund-policy" element={<RefundPolicy />} />
                            <Route path="/payment" element={
                                <ProtectedRoute>
                                    <PaymentPage />
                                </ProtectedRoute>
                            } />
                            <Route path="/admin" element={
                                <ProtectedRoute>
                                    <AdminDashboard />
                                </ProtectedRoute>
                            } />
                            <Route path="/dashboard" element={
                                <ProtectedRoute>
                                    <AnalysisDashboard />
                                </ProtectedRoute>
                            } />
                        </Routes>
                    </Router>
                </ErrorBoundary>
            </AuthProvider>
        </GoogleOAuthProvider>
    );
}

export default App;
