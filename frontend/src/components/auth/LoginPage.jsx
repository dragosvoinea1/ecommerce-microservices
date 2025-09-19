import { useState, useContext } from 'react'; // Importă useContext
import { useNavigate } from 'react-router-dom'; // Importă useNavigate
import { AuthContext } from '../../context/AuthContext'; // Importă contextul
import '../../styles/AuthForm.css';

export default function LoginPage() {
   const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();


  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Email sau parolă incorectă');
      }

      const data = await response.json();
      login(data.access_token); // <-- Cheamă funcția de login din context
      navigate('/'); // <-- Redirecționează la pagina principală
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Login</h2>
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
          <div className="form-group">
            <label htmlFor="password">Parolă:</label>
            <input 
              id="password"
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
          </div>
          <button type="submit" className="auth-button">Login</button>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
}