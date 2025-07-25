import '../styles/Navbar.css'; // <-- Importă fișierul CSS
import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { CartContext } from '../context/CartContext'; // <-- Am importat contextul coșului

export default function Navbar() {
  const { token, logout } = useContext(AuthContext);
  const { items } = useContext(CartContext); // <-- Preluăm produsele din coș

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Magazinul Meu</Link>
      </div>
      <div className="navbar-links">
        {/* --- NOU: Afișăm numărul de iteme din coș --- */}
        <Link to="/cart">Coș ({items.length})</Link>

        {token ? (
          <>
            {/* Aici vom adăuga link-ul către 'Comenzile Mele' */}
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}