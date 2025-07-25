import { Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import '../styles/Navbar.css'; // <-- Importă fișierul CSS

export default function Navbar() {
  const { token, logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Magazinul Meu</Link>
      </div>
      <div className="navbar-links">
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