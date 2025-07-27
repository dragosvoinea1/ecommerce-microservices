import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);

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

  return (
    <div>
      <h2>Categorii de Produse</h2>
      <ul className="product-list">
        {categories.map(category => (
          <li key={category.id}>
            <Link to={`/categories/${category.id}`}>{category.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}