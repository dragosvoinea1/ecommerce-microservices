import { useState, useEffect } from 'react';
import ProductCard from './ProductCard'; 

export default function ProductListPage() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);

  // Încarcă categoriile
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

  // Încarcă produsele
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

  // Filtrează produsele
  const filteredProducts = selectedCategory
    ? products.filter(p => p.category.id === selectedCategory)
    : products;

  return (
    <div>
      <h2>Produse Disponibile:</h2>
      
      <div>
        <button onClick={() => setSelectedCategory(null)}>Toate Categoriile</button>
        {categories.map(category => (
          <button key={category.id} onClick={() => setSelectedCategory(category.id)}>
            {category.name}
          </button>
        ))}
      </div>
      <hr/>

      {/* --- AICI ESTE MODIFICAREA PRINCIPALĂ --- */}
      {/* Am înlocuit <ul> cu <div className="product-grid"> */}
      {/* Și <li> cu componenta <ProductCard /> */}
      <div className="product-grid">
        {filteredProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}