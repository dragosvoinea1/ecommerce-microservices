import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { AuthProvider } from './context/AuthContext.jsx'; // <-- Importă provider-ul

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider> {/* <-- Îmbracă App în AuthProvider */}
      <App />
    </AuthProvider>
  </React.StrictMode>,
);