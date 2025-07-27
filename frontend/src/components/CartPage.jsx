// în frontend/src/components/CartPage.jsx
import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { CartContext } from '../context/CartContext';
import { AuthContext } from '../context/AuthContext';
import Modal from './Modal'; // <-- Importăm Modal
import { useConfirmationModal } from '../hooks/useConfirmationModal'; // <-- Importăm hook-ul

export default function CartPage() {
  const { items, clearCart, removeFromCart } = useContext(CartContext);
  const { token } = useContext(AuthContext); // Preluăm token-ul de autentificare
  const navigate = useNavigate();

  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handlePlaceOrder = async () => {
    if (!token) {
      alert('Trebuie să fii logat pentru a plasa o comandă.');
      navigate('/login');
      return;
    }

    // Pregătim datele pentru API
    const orderData = {
      items: items.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
      })),
    };

    try {
      const response = await fetch('http://localhost:8000/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Trimitem token-ul
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        throw new Error('Eroare la plasarea comenzii');
      }

      alert('Comanda a fost plasată cu succes!');
      clearCart(); // Golim coșul
      navigate('/my-orders'); // Redirecționăm la istoricul de comenzi

    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  const confirmRemove = () => {
    if (modalData) {
      removeFromCart(modalData.id); // Ștergem produsul folosind ID-ul salvat
    }
    closeModal();
  };

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
                {/* --- NOU: Butonul de ștergere --- */}
                <button
                  onClick={() => openModal(item)}
                  style={{ marginLeft: '10px', backgroundColor: '#dc3545' }}
                >
                  Șterge
                </button>
              </li>
              
            ))}
          </ul>
          <hr />
          <h3>Total: {total.toFixed(2)} RON</h3>
          <button onClick={handlePlaceOrder}>Plasează Comanda</button>
        </>
      )}
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <h3>Confirmare Ștergere</h3>
        <p>Ești sigur că vrei să ștergi produsul "{modalData?.name}" din coș?</p>
        <div className="modal-actions">
          <button onClick={confirmRemove} className="confirm-btn">Confirmă</button>
          <button onClick={closeModal} className="cancel-btn">Anulează</button>
        </div>
      </Modal>
    </div>
  );
}