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

function App() {
  return (
    <BrowserRouter>
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