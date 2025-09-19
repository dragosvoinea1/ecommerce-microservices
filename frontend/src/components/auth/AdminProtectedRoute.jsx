import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

export default function AdminProtectedRoute({ children }) {
  const { user } = useContext(AuthContext);

  // Dacă utilizatorul nu este logat sau nu are rolul 'admin',
  // îl redirecționăm către pagina principală.
  if (!user || user.role !== 'admin') {
    return <Navigate to="/" />;
  }

  // Dacă este admin, afișăm conținutul paginii protejate.
  return children;
}