import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../../styles/AuthForm.css';

export default function ResetPasswordPage() {
  const { token } = useParams(); // Preluăm token-ul din URL
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Parolele nu se potrivesc.');
      return;
    }
    setError('');
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'A apărut o eroare.');
      }

      setMessage(data.message + ' Vei fi redirecționat la login...');
      setTimeout(() => navigate('/login'), 3000); // Redirecționare după 3 secunde
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Setează o Parolă Nouă</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="password">Parola Nouă:</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirm-password">Confirmă Parola:</label>
            <input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="auth-button">Schimbă Parola</button>

          {message && <p style={{ color: 'lightgreen', marginTop: '15px' }}>{message}</p>}
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
}