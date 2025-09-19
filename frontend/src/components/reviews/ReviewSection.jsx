import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import ReviewItem from './ReviewItem'; // Calea este corectă, relativă la folderul curent
import StarRatingInput from './StarRatingInput';
import Modal from '../ui/Modal'; 
import { useConfirmationModal } from '../../hooks/useConfirmationModal';
import '../../styles/Reviews.css';


export default function ReviewsSection({ productId }) {
  const [reviews, setReviews] = useState([]);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [error, setError] = useState('');
  const { token, user } = useContext(AuthContext);

  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  const fetchReviews = async () => {
    try {
      const response = await fetch(`http://localhost:8000/reviews/product/${productId}`);
      if (!response.ok) throw new Error('Nu am putut prelua recenziile.');
      const data = await response.json();
      setReviews(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (productId) {
      fetchReviews();
    }
  }, [productId]);

  // --- LOGICA PENTRU ADĂUGARE RECENZIE ---
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    if (!token) {
      setError('Trebuie să fii autentificat pentru a lăsa o recenzie.');
      return;
    }
    openModal({ type: 'add', data: { product_id: productId, rating, comment } });
  };

  const confirmAddReview = async () => {
    const reviewData = modalData.data;
    try {
      const response = await fetch('http://localhost:8000/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(reviewData),
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'A apărut o eroare.');
      }
      setComment('');
      setRating(5);
      fetchReviews();
    } catch (err) {
      setError(err.message);
    } finally {
      closeModal();
    }
  };

  // --- LOGICA PENTRU ȘTERGERE RECENZIE ---
  const handleDelete = (reviewId) => {
    openModal({ type: 'delete', data: { reviewId } });
  };

  const confirmDeleteReview = async () => {
    const { reviewId } = modalData.data;
    try {
      const response = await fetch(`http://localhost:8000/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error('Eroare la ștergere.');
      fetchReviews();
    } catch (err) {
      alert(err.message);
    } finally {
      closeModal();
    }
  };

  const handleConfirm = () => {
    if (modalData?.type === 'add') {
      confirmAddReview();
    } else if (modalData?.type === 'delete') {
      confirmDeleteReview();
    }
  };


  return (
    <div className="reviews-container">
      <h3>Recenzii Produs</h3>
      {token && (
        <form onSubmit={handleSubmit} className="review-form">
            <h4>Adaugă recenzia ta</h4>
            <div className="form-group">
                <label>Nota:</label>
                <StarRatingInput rating={rating} setRating={setRating} />
            </div>
            <div className="form-group">
                <label>Comentariu:</label>
                <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Spune-ți părerea despre produs..."
                />
            </div>
            {error && <p className="error-message">{error}</p>}
            <button type="submit" className="auth-button">Trimite</button>
        </form>
      )}

      <ul className="reviews-list">
        {reviews.length > 0 ? (
          reviews.map(review => (
            <ReviewItem
              key={review.id}
              review={review}
              onDelete={handleDelete}
              currentUserEmail={user?.sub}
            />
          ))
        ) : (
          <p>Acest produs nu are nicio recenzie. Fii primul care adaugă una!</p>
        )}
      </ul>

      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <h3>Confirmare</h3>
        <p>
          {modalData?.type === 'add' 
            ? 'Ești sigur că vrei să adaugi această recenzie?' 
            : 'Ești sigur că vrei să ștergi această recenzie?'}
        </p>
        <div className="modal-actions">
          <button onClick={handleConfirm} className="confirm-btn">Confirmă</button>
          <button onClick={closeModal} className="cancel-btn">Anulează</button>
        </div>
      </Modal>
    </div>
  );
}