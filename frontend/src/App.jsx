import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ProductListPage from './components/ProductListPage'; // Vom crea acest fișier imediat
import LoginPage from './components/LoginPage';
import './App.css';


function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Produse</Link> | <Link to="/login">Login</Link>
      </nav>
      <hr />
      <Routes>
        <Route path="/" element={<ProductListPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;