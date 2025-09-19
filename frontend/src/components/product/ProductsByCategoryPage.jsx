import { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { CartContext } from '../../context/CartContext';
import Modal from '../ui/Modal'; // <-- 1. Importăm Modal
import { useConfirmationModal } from '../../hooks/useConfirmationModal'; // <-- 2. Importăm hook-ul

export default function ProductsByCategoryPage() {
  const [products, setProducts] = useState([]);
  const { categoryId } = useParams(); // Preluăm ID-ul din URL
  const { addToCart } = useContext(CartContext);

  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(`http://localhost:8000/products/category/${categoryId}`);
        if (!response.ok) throw new Error('Nu am putut prelua produsele.');
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };
    fetchProducts();
  }, [categoryId]); // Efectul se re-execută la schimbarea ID-ului din URL

  const confirmAddToCart = () => {
    if (modalData) {
      addToCart(modalData);
    }
    closeModal();
  };

  return (
    <div>
      <h2>Produse</h2> 
      <ul className="product-list">
        {products.map((product) => (
          <li key={product.id}>
            {product.name} - {product.price} RON
            {/* 5. Modificăm butonul să deschidă modalul în loc să adauge direct în coș */}
            <button onClick={() => openModal(product)} style={{ marginLeft: '10px' }}>
              Adaugă în Coș
            </button>
          </li>
        ))}
      </ul>

      {/* 6. Adăugăm componenta Modal în pagină */}
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <h3>Confirmare</h3>
        <p>Ești sigur că vrei să adaugi produsul "{modalData?.name}" în coș?</p>
        <div className="modal-actions">
          <button onClick={confirmAddToCart} className="confirm-btn">Confirmă</button>
          <button onClick={closeModal} className="cancel-btn">Anulează</button>
        </div>
      </Modal>
    </div>
  );
}