import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import ProductCard from './ProductCard';

export default function SearchResultsPage() {
  const [results, setResults] = useState([]);
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q'); // Preluăm termenul de căutare din URL

  useEffect(() => {
    if (query) {
      const fetchResults = async () => {
        try {
          // Apelăm API Gateway-ul, care va redirecționa la search-service
          const response = await fetch(`http://localhost:8000/search?q=${query}`);
          const data = await response.json();
          setResults(data);
        } catch (error) {
          console.error("Error fetching search results:", error);
        }
      };
      fetchResults();
    }
  }, [query]); // Re-executăm la fiecare căutare nouă

  return (
    <div>
      <h2>Rezultate pentru: "{query}"</h2>
      <div className="product-grid">
        {results.length > 0 ? (
          results.map(product => (
            <ProductCard key={product.id} product={product} />
          ))
        ) : (
          <p>Nu s-au găsit produse care să corespundă căutării tale.</p>
        )}
      </div>
    </div>
  );
}