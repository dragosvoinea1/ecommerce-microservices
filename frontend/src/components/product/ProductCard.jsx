import { useState, useContext } from 'react';
import { CartContext } from '../../context/CartContext';
import { useConfirmationModal } from '../../hooks/useConfirmationModal';
import Modal from '../ui/Modal';
import { Link } from 'react-router-dom';
import '../../styles/ProductCard.css';

export default function ProductCard({ product }) {
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useContext(CartContext);
  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  const confirmAddToCart = () => {
    if (modalData) {
      addToCart(modalData, quantity);
    }
    closeModal();
  };

  return (
    <div className="product-card">
      {/* 👇 Îmbracă partea de sus a cardului într-un Link 👇 */}
      <Link to={`/products/${product.id}`} className="product-card-link">
        <img src={product.image_url || 'https://via.placeholder.com/250'} alt={product.name} />
        <h3>{product.name}</h3>
        <p className="product-price">{product.price.toFixed(2)} RON</p>
      </Link>
      
      <div className="add-to-cart-controls">
        <input 
          type="number" 
          value={quantity}
          onChange={(e) => setQuantity(parseInt(e.target.value, 10))}
          min="1"
        />
        <button onClick={() => openModal(product)}>Adaugă în Coș</button>
      </div>

      <Modal isOpen={isModalOpen && modalData?.id === product.id} onClose={closeModal}>
        <h3>Confirmare</h3>
        <p>Ești sigur că vrei să adaugi {quantity} buc. de "{product.name}" în coș?</p>
        <div className="modal-actions">
          <button onClick={confirmAddToCart} className="confirm-btn">Confirmă</button>
          <button onClick={closeModal} className="cancel-btn">Anulează</button>
        </div>
      </Modal>
    </div>
  );
}