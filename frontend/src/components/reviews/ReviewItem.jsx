// O funcție simplă pentru a afișa steluțe în loc de cifre
const StarRating = ({ rating }) => {
  return (
    <div className="star-rating">
      {[...Array(5)].map((star, index) => {
        const ratingValue = index + 1;
        return (
          <span key={ratingValue} className={ratingValue <= rating ? "star-filled" : "star-empty"}>
            ★
          </span>
        );
      })}
    </div>
  );
};

export default function ReviewItem({ review, onDelete, currentUserEmail }) {
  const isOwner = currentUserEmail === review.user_email;

  return (
    <li className="review-item">
      {/* Container pentru conținutul principal al recenziei */}
      <div className="review-content">
        <div className="review-header">
          <strong className="review-author">{review.user_email.split('@')[0]}</strong>
          <StarRating rating={review.rating} />
        </div>
        <p className="review-comment">{review.comment}</p>
        <small className="review-date">
          {new Date(review.created_at).toLocaleDateString('ro-RO')}
        </small>
      </div>

      {/* Container separat pentru acțiuni (butonul de ștergere) */}
      {isOwner && (
        <div className="review-actions">
          <button onClick={() => onDelete(review.id)} className="delete-review-btn" title="Șterge recenzia">
            🗑️
          </button>
        </div>
      )}
    </li>
  );
}