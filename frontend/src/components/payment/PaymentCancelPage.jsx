import { Link } from 'react-router-dom';

export default function PaymentCancelPage() {
  return (
    <div style={{ textAlign: 'center', padding: '40px' }}>
      <h2>❌ Plata a fost anulată.</h2>
      <p>Plata nu a fost finalizată. Produsele tale sunt încă în coșul de cumpărături.</p>
      <Link to="/cart" style={{ color: '#88aaff' }}>
        Mergi înapoi la coș
      </Link>
    </div>
  );
}