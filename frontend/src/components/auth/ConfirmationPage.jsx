import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function ConfirmationPage() {
  const { token } = useParams();
  const [message, setMessage] = useState('Se activează contul...');
  const [error, setError] = useState(false);

  useEffect(() => {
    let isMounted = true; // Flag pentru a preveni actualizări după ce componenta e demontată

    const confirmAccount = async () => {
      try {
        const response = await fetch(`http://localhost:8000/confirm/${token}`);
        
        if (!isMounted) return; // Nu face nimic dacă componenta nu mai e activă

        if (!response.ok) {
          // Verificăm dacă eroarea este cea așteptată (token deja folosit)
          const errorData = await response.json();
          if (errorData.detail === 'Token invalid.') {
            setMessage('Contul tău este deja activat sau link-ul a fost folosit.');
            setError(false); // Considerăm acest caz un semi-succes
          } else {
            throw new Error(errorData.detail || 'A apărut o eroare.');
          }
        } else {
          setMessage('Contul tău a fost activat cu succes!');
          setError(false);
        }
      } catch (err) {
        if (isMounted) {
          setMessage(err.message);
          setError(true);
        }
      }
    };

    confirmAccount();

    return () => {
      isMounted = false; // Setăm flag-ul pe false la curățare
    };
  }, [token]);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>Status Activare Cont</h2>
      <p style={{ color: error ? 'red' : 'lightgreen' }}>{message}</p>
      <Link to="/login" style={{ color: '#88aaff', textDecoration: 'none' }}>
        Mergi la pagina de Login
      </Link>
    </div>
  );
}