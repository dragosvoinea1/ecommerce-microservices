import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ReviewsSection from '../reviews/ReviewSection'; // Importăm secțiunea de recenzii
import '../../styles/ProductDetailPage.css'; // Vom crea acest fișier de stil

export default function ProductDetailPage() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:8000/products/${productId}`);
        if (!response.ok) {
          throw new Error('Produsul nu a fost găsit.');
        }
        const data = await response.json();
        setProduct(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  if (loading) return <p>Se încarcă detaliile produsului...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!product) return <p>Nu am găsit detalii pentru acest produs.</p>;

  const hasDiscount = product.discount_percentage && product.discount_percentage > 0;
  const discountedPrice = hasDiscount
    ? product.price * (1 - product.discount_percentage / 100)
    : product.price;

  return (
    <div className="product-detail-container">
      <div className="product-info">
        <img src={product.image_url || 'https://via.placeholder.com/400'} alt={product.name} className="product-detail-image" />
        <div className="product-detail-text">
          <h1>{product.name}</h1>
           <div className="product-detail-price">
            {hasDiscount ? (
              <>
                <span className="original-price-detail">{product.price.toFixed(2)} RON</span>
                <span className="discounted-price-detail">{discountedPrice.toFixed(2)} RON</span>
              </>
            ) : (
              <span>{product.price.toFixed(2)} RON</span>
            )}
          </div>
          <p className="product-detail-description">{product.description}</p>
          {/* Aici poți adăuga controalele pentru "Adaugă în coș" dacă dorești */}
        </div>
      </div>
      <hr style={{ borderColor: '#444', margin: '2rem 0' }}/>
      
      {/* Aici integrăm secțiunea de recenzii */}
      <ReviewsSection productId={productId} />
    </div>
  );
}