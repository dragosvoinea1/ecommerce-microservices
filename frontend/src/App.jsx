import ProductListPage from './components/product/ProductListPage';
import CategoriesPage from './components/product/CategoriesPage';
import ProductsByCategoryPage from './components/product/ProductsByCategoryPage';
import ProductDetailPage from './components/product/ProductDetailPage';
import SearchResultsPage from './components/product/SearchResultsPage';

import LoginPage from './components/auth/LoginPage';
import RegisterPage from './components/auth/RegisterPage';
import ConfirmationPage from './components/auth/ConfirmationPage';
import AdminProtectedRoute from './components/auth/AdminProtectedRoute';

import CartPage from './components/cart/CartPage';
import OrderHistoryPage from './components/orders/OrderHistoryPage';

import AdminDashboardPage from './components/admin/AdminDashboardPage';
import ManageCategoriesPage from './components/admin/ManageCategoriesPage';
import ManageProductsPage from './components/admin/ManageProductsPage';
import EditProductPage from './components/admin/EditProductPage';

import Navbar from './components/layout/Navbar';

import PaymentSuccessPage from './components/payment/PaymentSuccessPage';
import PaymentCancelPage from './components/payment/PaymentCancelPage';

import ForgotPasswordPage from './components/auth/ForgotPasswordPage';
import ResetPasswordPage from './components/auth/ResetPasswordPage';

import ProtectedRoute from './components/auth/ProtectedRoute';
import UserProfilePage from './components/auth/UserProfilePage';

import WishlistPage from './components/wishlist/WishlistPage';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './styles/App.css';

import { useEffect, useContext, useState, useRef } from 'react';
import { AuthContext } from './context/AuthContext';

function App() {
  const { user } = useContext(AuthContext);
  const [notification, setNotification] = useState(null);
  const ws = useRef(null); // <-- 2. Inițializează un ref pentru WebSocket

  useEffect(() => {
    // Dacă nu există utilizator logat, ne asigurăm că orice conexiune veche este închisă
    if (!user?.sub) {
      if (ws.current) {
        ws.current.close();
        ws.current = null;
      }
      return;
    }

    // Dacă există deja o conexiune activă, nu facem nimic
    if (ws.current) {
      return;
    }

    // Creăm o singură dată conexiunea
    ws.current = new WebSocket(`ws://localhost:8000/ws/${user.sub}`);

    ws.current.onopen = () => {
      console.log("WebSocket connected"); // Vei vedea asta în consolă
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotification(data.message);
      setTimeout(() => setNotification(null), 5000);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
      // Resetează ref-ul pentru a permite reconectarea la următorul login/refresh
      ws.current = null;
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    // Funcția de curățare se va asigura că la demontarea completă a aplicației, conexiunea se închide
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [user]);

  return (
    <BrowserRouter>
      {notification && (
        <div style={{
          position: 'fixed', top: '80px', right: '20px',
          padding: '15px', backgroundColor: '#646cff', color: 'white',
          borderRadius: '8px', zIndex: 1001, boxShadow: '0 4px 8px rgba(0,0,0,0.3)'
        }}>
          🔔 {notification}
        </div>
      )}
      <Navbar />
      <hr />
      <main>
        <Routes>
          <Route path="/" element={<ProductListPage />} />
          <Route path="/products/:productId" element={<ProductDetailPage />} />
          <Route path="/categories" element={<CategoriesPage />} /> {/* Rută nouă */}
          <Route path="/categories/:categoryId" element={<ProductsByCategoryPage />} /> {/* Rută dinamică nouă */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/my-orders" element={<OrderHistoryPage />} /> {/* <-- Adaugă această linie */}

          <Route
            path="/profile"
            element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>}
          />

          <Route
            path="/admin"
            element={
              <AdminProtectedRoute>
                <AdminDashboardPage />
              </AdminProtectedRoute>
            }
          />
          <Route
            path="/admin/categories"
            element={
              <AdminProtectedRoute>
                <ManageCategoriesPage />
              </AdminProtectedRoute>
            }
          />
          <Route
            path="/admin/products"
            element={<AdminProtectedRoute><ManageProductsPage /></AdminProtectedRoute>}
          />
          <Route
            path="/admin/products/edit/:productId"
            element={<AdminProtectedRoute><EditProductPage /></AdminProtectedRoute>}
          />
          <Route path="/search" element={<SearchResultsPage />} /> {/* <-- Ruta nouă */}
          <Route path="/confirm/:token" element={<ConfirmationPage />} /> {/* <-- Ruta nouă */}

          <Route path="/payment-success" element={<PaymentSuccessPage />} />
          <Route path="/payment-cancel" element={<PaymentCancelPage />} />

            <Route
            path="/wishlist" // <-- RUTĂ NOUĂ
            element={<ProtectedRoute><WishlistPage /></ProtectedRoute>}
          />

        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;