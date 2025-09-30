import { useState, useContext } from 'react';
import { CartContext } from '../../context/CartContext';
import { AuthContext } from '../../context/AuthContext';
import { WishlistContext } from '../../context/WishlistContext'; 
import { useConfirmationModal } from '../../hooks/useConfirmationModal';
import Modal from '../ui/Modal';
import { Link } from 'react-router-dom';
import '../../styles/ProductCard.css';

export default function ProductCard({ product }) {
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useContext(CartContext);
  const { token } = useContext(AuthContext);
  const { addToWishlist, removeFromWishlist, isProductInWishlist } = useContext(WishlistContext);
  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  const confirmAddToCart = () => {
    if (modalData) {
      addToCart(modalData, quantity);
    }
    closeModal();
  };

  const inWishlist = isProductInWishlist(product.id);

  const handleWishlistToggle = () => {
    if (!token) {
      alert("Trebuie să fii autentificat pentru a folosi wishlist-ul.");
      return;
    }
    if (inWishlist) {
      removeFromWishlist(product.id);
    } else {
      addToWishlist(product.id);
    }
  };

  const hasDiscount = product.discount_percentage && product.discount_percentage > 0;
  const discountedPrice = hasDiscount 
    ? product.price * (1 - product.discount_percentage / 100) 
    : product.price;

  return (
    <div className="product-card">
      <Link to={`/products/${product.id}`} className="product-card-link">

        <img src={product.image_url || 'https://via.placeholder.com/250'} alt={product.name} />
        <h3>{product.name}</h3>
        <div className="product-price-container">
          {hasDiscount ? (
            <>
              <span className="original-price">{product.price.toFixed(2)} RON</span>
              <span className="discounted-price">{discountedPrice.toFixed(2)} RON</span>
            </>
          ) : (
            <span className="product-price">{product.price.toFixed(2)} RON</span>
          )}
        </div>
      </Link>
              {token && (
          <button 
            onClick={handleWishlistToggle} 
            className={`wishlist-btn ${inWishlist ? 'active' : ''}`}
            title={inWishlist ? 'Șterge din wishlist' : 'Adaugă în wishlist'}
          >
            {inWishlist ? '❤️' : '♡'}
          </button>
        )}

      {/* Controalele pentru adăugarea în coș */}
      <div className="add-to-cart-controls">
        <input 
          type="number" 
          value={quantity}
          onChange={(e) => setQuantity(parseInt(e.target.value, 10))}
          min="1"
        />
        <button onClick={() => openModal(product)}>Adaugă în Coș</button>
      </div>

      {/* Modalul de confirmare pentru adăugarea în coș */}
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