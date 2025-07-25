import { createContext, useState, useEffect } from 'react';

// Creăm contextul
export const AuthContext = createContext(null);

// Creăm "Provider-ul", componenta care va oferi starea celorlalte componente
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);

  // Verificăm la încărcarea paginii dacă există un token salvat în browser
  useEffect(() => {
    const storedToken = localStorage.getItem('accessToken');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  // Funcția de login: salvează token-ul în state și în localStorage
  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem('accessToken', newToken);
  };

  // Funcția de logout: șterge token-ul
  const logout = () => {
    setToken(null);
    localStorage.removeItem('accessToken');
  };

  // Oferim starea și funcțiile copiilor
  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};