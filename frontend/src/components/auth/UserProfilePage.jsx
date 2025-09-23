import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import '../../styles/AuthForm.css'; // Reutilizăm stilurile

export default function UserProfilePage() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone_number: '',
    address: '',
    city: '',
    country: ''
  });
  const [message, setMessage] = useState('');
  const { token } = useContext(AuthContext);

  // Preluăm datele utilizatorului la încărcarea paginii
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:8000/users/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        setFormData(data);
      } catch (error) {
        console.error("Eroare la preluarea datelor:", error);
      }
    };
    if (token) {
      fetchUserData();
    }
  }, [token]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    
    // Trimitem doar câmpurile care pot fi modificate
    const { full_name, phone_number, address, city, country } = formData;
    const updateData = { full_name, phone_number, address, city, country };

    try {
      const response = await fetch('http://localhost:8000/users/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData)
      });

      if (!response.ok) throw new Error('Eroare la actualizarea profilului.');
      
      setMessage('Profilul a fost actualizat cu succes!');
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Profilul Meu</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          {/* Câmpul de email este doar pentru afișare */}
          <div className="form-group">
            <label>Email:</label>
            <input type="email" value={formData.email} disabled />
          </div>
          
          {/* Câmpuri editabile */}
          <div className="form-group">
            <label htmlFor="full_name">Nume complet:</label>
            <input id="full_name" name="full_name" value={formData.full_name} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label htmlFor="phone_number">Număr de telefon:</label>
            <input id="phone_number" name="phone_number" value={formData.phone_number} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label htmlFor="address">Adresă:</label>
            <input id="address" name="address" value={formData.address} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label htmlFor="city">Oraș:</label>
            <input id="city" name="city" value={formData.city} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label htmlFor="country">Țară:</label>
            <input id="country" name="country" value={formData.country} onChange={handleChange} />
          </div>
          
          <button type="submit" className="auth-button">Salvează Modificările</button>
          {message && <p style={{ color: 'lightgreen', marginTop: '15px' }}>{message}</p>}
        </form>
      </div>
    </div>
  );
}