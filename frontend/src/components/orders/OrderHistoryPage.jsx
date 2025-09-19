import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';

export default function OrderHistoryPage() {
  const [orders, setOrders] = useState([]);
  const { token } = useContext(AuthContext);

  const fetchOrders = async () => {
    try {
      const response = await fetch('http://localhost:8000/orders', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error('Nu am putut prelua comenzile.');
      const data = await response.json();
      setOrders(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (token) {
      fetchOrders();
    }
  }, [token]);

  // --- NOU: Funcția pentru a șterge o comandă ---
  const handleDelete = async (orderId) => {
    if (!window.confirm("Ești sigur că vrei să ștergi această comandă?")) {
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:8000/orders/${orderId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Eroare la ștergerea comenzii.');
      }

      // Actualizăm lista de comenzi din UI fără a reîncărca pagina
      setOrders(prevOrders => prevOrders.filter(order => order.id !== orderId));
      alert('Comanda a fost ștearsă cu succes.');

    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  return (
    <div>
      <h2>Istoricul Comenzilor</h2>
      {orders.length === 0 ? (
        <p>Nu ai plasat nicio comandă.</p>
      ) : (
        orders.map(order => (
          <div key={order.id} style={{ border: '1px solid grey', padding: '10px', margin: '10px' }}>
            <h4>Comanda ID: {order.id} - Total: {order.total_amount.toFixed(2)} RON</h4>
            <ul>
              {order.items.map(item => (
                <li key={item.id}>
                  Produs ID: {item.product_id} - Cantitate: {item.quantity}
                </li>
              ))}
            </ul>
            {/* --- NOU: Butonul de ștergere --- */}
            <button onClick={() => handleDelete(order.id)} style={{backgroundColor: '#dc3545'}}>
              Șterge Comanda
            </button>
          </div>
        ))
      )}
    </div>
  );
}