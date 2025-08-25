import { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
// Creăm contextul
export const AuthContext = createContext(null);

// Creăm "Provider-ul", componenta care va oferi starea celorlalte componente
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);

  // Verificăm la încărcarea paginii dacă există un token salvat în browser
  useEffect(() => {
    const storedToken = localStorage.getItem('accessToken');
    if (storedToken) {
      try {
        const decodedUser = jwtDecode(storedToken);
        setUser(decodedUser); // Salvăm datele decodate (email, rol)
        setToken(storedToken);
      } catch (error) {
        // Dacă token-ul e invalid, îl ștergem
        localStorage.removeItem('accessToken');
      }
    }
  }, []);

  // Funcția de login: salvează token-ul în state și în localStorage
  const login = (newToken) => {
    try {
      const decodedUser = jwtDecode(newToken);
      setUser(decodedUser); // Salvăm datele la login
      setToken(newToken);
      localStorage.setItem('accessToken', newToken);
    } catch (error) {
      console.error("Token invalid", error);
    }
  };

  // Funcția de logout: șterge token-ul
  const logout = () => {
    setToken(null);
    setUser(null); // Ștergem și datele utilizatorului
    localStorage.removeItem('accessToken');
  };
  // Oferim starea și funcțiile copiilor
  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};