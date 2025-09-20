import { useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import { CartContext } from '../../context/CartContext';

export default function PaymentSuccessPage() {
  const { clearCart } = useContext(CartContext);

  // Golim coșul de cumpărături automat la afișarea paginii
  useEffect(() => {
    clearCart();
  }, []);

  return (
    <div style={{ textAlign: 'center', padding: '40px' }}>
      <h2>✅ Plata a fost efectuată cu succes!</h2>
      <p>Comanda ta a fost înregistrată și va fi procesată în curând.</p>
      <p>Mulțumim că ai cumpărat de la noi!</p>
      <Link to="/my-orders" style={{ color: '#88aaff' }}>
        Vezi istoricul comenzilor
      </Link>
    </div>
  );
}