import { useContext } from 'react';
import { CartContext } from '../context/CartContext';

export default function CartPage() {
  const { items } = useContext(CartContext);

  // Calculăm totalul coșului
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div>
      <h2>Coșul tău de cumpărături</h2>
      {items.length === 0 ? (
        <p>Coșul este gol.</p>
      ) : (
        <>
          <ul>
            {items.map((item) => (
              <li key={item.id}>
                {item.name} - {item.quantity} buc. x {item.price} RON
              </li>
            ))}
          </ul>
          <hr />
          <h3>Total: {total.toFixed(2)} RON</h3>
          {/* Aici vom adăuga butonul de "Plasează Comanda" */}
        </>
      )}
    </div>
  );
}