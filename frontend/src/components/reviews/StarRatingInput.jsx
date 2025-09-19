import { useState } from 'react';

export default function StarRatingInput({ rating, setRating }) {
  // O stare nouă, locală, pentru a ține minte peste ce stea este mouse-ul
  const [hover, setHover] = useState(0);

  return (
    <div className="star-rating-input">
      {[...Array(5)].map((star, index) => {
        const ratingValue = index + 1;

        return (
          <button
            type="button" // Important pentru a nu trimite formularul la click
            key={ratingValue}
            className={ratingValue <= (hover || rating) ? "star-filled" : "star-empty"}
            onClick={() => setRating(ratingValue)}
            onMouseEnter={() => setHover(ratingValue)}
            onMouseLeave={() => setHover(0)}
          >
            <span className="star-char">★</span>
          </button>
        );
      })}
    </div>
  );
}