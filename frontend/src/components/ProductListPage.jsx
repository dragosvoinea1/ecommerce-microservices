import { useState, useEffect } from 'react';

export default function ProductListPage() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };
    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Produse Disponibile:</h2>
      {Array.isArray(products) && products.length > 0 ? (
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              {product.name} - {product.price} RON
            </li>
          ))}
        </ul>
      ) : (
        <p>Nu sunt produse disponibile sau se încarcă...</p>
      )}
    </div>
  );
}