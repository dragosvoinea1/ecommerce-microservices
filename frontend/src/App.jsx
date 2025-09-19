import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductListPage from './components/ProductListPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import CartPage from './components/CartPage';
import OrderHistoryPage from './components/OrderHistoryPage'; // Asigură-te că este importată
import Navbar from './components/Navbar';
import CategoriesPage from './components/CategoriesPage';
import ProductsByCategoryPage from './components/ProductsByCategoryPage';
import AdminDashboardPage from './components/AdminDashboardPage';
import AdminProtectedRoute from './components/AdminProtectedRoute';
import ManageCategoriesPage from './components/admin/ManageCategoriesPage';
import ManageProductsPage from './components/admin/ManageProductsPage';
import EditProductPage from './components/admin/EditProductPage';
import SearchResultsPage from './components/SearchResultsPage';
import ConfirmationPage from './components/ConfirmationPage';
import ProductDetailPage from './components/ProductDetailPage';
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
          <Route path="/cart" element={<CartPage />} />
          <Route path="/my-orders" element={<OrderHistoryPage />} /> {/* <-- Adaugă această linie */}
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
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;