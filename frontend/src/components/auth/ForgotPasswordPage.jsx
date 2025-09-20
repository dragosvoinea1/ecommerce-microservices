import { useState } from 'react';
import '../../styles/AuthForm.css'; // Reutilizăm stilurile existente

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await fetch('http://localhost:8000/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // 👇 Trimitem un obiect JSON, nu un string 👇
        body: JSON.stringify({ email: email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'A apărut o eroare.');
      }

      setMessage(data.message);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Resetează Parola</h2>
        <p style={{ color: '#b0b0b0', marginBottom: '20px' }}>
          Introdu adresa de email și îți vom trimite un link pentru a-ți reseta parola.
        </p>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="auth-button">Trimite Link</button>
          
          {/* Afișăm mesajul de succes sau de eroare */}
          {message && <p style={{ color: 'lightgreen', marginTop: '15px' }}>{message}</p>}
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
}