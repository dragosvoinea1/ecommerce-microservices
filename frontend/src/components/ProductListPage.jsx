import { useState, useEffect, useContext } from 'react';
import { CartContext } from '../context/CartContext';

export default function ProductListPage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null); // Starea pentru categoria selectată
  const { addToCart } = useContext(CartContext);

  // 1. Încarcă lista de categorii o singură dată
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://localhost:8000/products/categories');
        if (!response.ok) throw new Error('Nu am putut prelua categoriile.');
        const data = await response.json();
        setCategories(data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchCategories();
  }, []);

  // 2. Încarcă TOATE produsele o singură dată
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    };
    fetchProducts();
  }, []);

  // 3. Filtrează produsele pe baza categoriei selectate (direct în frontend)
  const filteredProducts = selectedCategory
    ? products.filter(p => p.category.id === selectedCategory)
    : products;

  return (
    <div>
      <h2>Produse Disponibile:</h2>
      
      {/* 4. Afișează butoanele de filtrare pe categorii */}
      <div>
        <button onClick={() => setSelectedCategory(null)}>Toate Categoriile</button>
        {categories.map(category => (
          <button key={category.id} onClick={() => setSelectedCategory(category.id)}>
            {category.name}
          </button>
        ))}
      </div>
      <hr/>

      {/* 5. Afișează produsele filtrate */}
      {filteredProducts.length > 0 ? (
        <ul className="product-list">
          {filteredProducts.map((product) => (
            <li key={product.id}>
              {product.name} - {product.price} RON (Categorie: {product.category.name})
              <button onClick={() => addToCart(product)} style={{ marginLeft: '10px' }}>
                Adaugă în Coș
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>Nu sunt produse în această categorie sau se încarcă...</p>
      )}
    </div>
  );
}