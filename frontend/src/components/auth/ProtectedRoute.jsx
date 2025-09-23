import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { token } = useContext(AuthContext);

  // Dacă nu există token, redirecționează la login
  if (!token) {
    return <Navigate to="/login" />;
  }

  // Altfel, afișează pagina protejată
  return children;
}