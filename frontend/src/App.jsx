import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductListPage from './components/ProductListPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage'; // <-- Importă pagina nouă
import Navbar from './components/Navbar'; // <-- Importă Navbar
import './styles/App.css';

function App() {
  return (
    <BrowserRouter>
      <Navbar /> {/* <-- Folosește componenta Navbar */}
      <hr />
      <main> {/* Am adăugat un tag <main> pentru conținutul paginii */}
        <Routes>
          <Route path="/" element={<ProductListPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} /> {/* <-- Adaugă ruta nouă */}
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;