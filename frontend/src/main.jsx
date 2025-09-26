import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { AuthProvider } from './context/AuthContext.jsx';
import { CartProvider } from './context/CartContext.jsx'; // <-- Importă noul provider
import { WishlistProvider } from './context/WishlistContext.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
   <React.StrictMode>
    <AuthProvider>
      <CartProvider>
        <WishlistProvider> {/* <-- ADAUGĂ AICI */}
          <App />
        </WishlistProvider>
      </CartProvider>
    </AuthProvider>
  </React.StrictMode>,
);