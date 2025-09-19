import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/AuthForm.css'; // Importăm noul fișier CSS

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone_number: '',
    password: '',
    address: '',
    city: '',
    country: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'A apărut o eroare');
      }

      alert('Cont creat cu succes! Acum te poți loga.');
      navigate('/login');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-page"> {/* Container principal al paginii */}
      <div className="auth-card"> {/* Containerul formularului (card-ul) */}
        <h2>Înregistrare Cont Nou</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="full_name">Nume complet:</label>
            <input id="full_name" name="full_name" value={formData.full_name} onChange={handleChange} placeholder="Ex: Popescu Ion" required />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input id="email" name="email" type="email" value={formData.email} onChange={handleChange} placeholder="Ex: user@example.com" required />
          </div>
          
          <div className="form-group">
            <label htmlFor="phone_number">Număr de telefon:</label>
            <input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleChange} placeholder="Ex: 0712345678" required />
          </div>

          <div className="form-group">
            <label htmlFor="password">Parolă:</label>
            <input id="password" name="password" type="password" value={formData.password} onChange={handleChange} placeholder="Minim 8 caractere" required />
          </div>

          <div className="form-group">
            <label htmlFor="address">Adresă:</label>
            <input id="address" name="address" value={formData.address} onChange={handleChange} placeholder="Ex: Strada Florilor, Nr. 10" required />
          </div>

          <div className="form-group">
            <label htmlFor="city">Oraș:</label>
            <input id="city" name="city" value={formData.city} onChange={handleChange} placeholder="Ex: București" required />
          </div>

          <div className="form-group">
            <label htmlFor="country">Țară:</label>
            <input id="country" name="country" value={formData.country} onChange={handleChange} placeholder="Ex: România" required />
          </div>
          
          <button type="submit" className="register-button">Înregistrare</button>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
}