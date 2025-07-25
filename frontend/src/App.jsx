import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductListPage from './components/ProductListPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import CartPage from './components/CartPage';
import OrderHistoryPage from './components/OrderHistoryPage'; // Asigură-te că este importată
import Navbar from './components/Navbar';
import './styles/App.css';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <hr />
      <main>
        <Routes>
          <Route path="/" element={<ProductListPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/my-orders" element={<OrderHistoryPage />} /> {/* <-- Adaugă această linie */}
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;