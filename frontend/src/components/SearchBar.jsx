import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SearchBar.css';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const navigate = useNavigate();

  // Efectul care se ocupă de debouncing și de apelul API
  useEffect(() => {
    // Dacă nu e niciun text în bară, golește sugestiile
    if (query.trim() === '') {
      setSuggestions([]);
      return;
    }

    // Setează un timer. Apelul API se face doar dacă nu se mai tastează nimic timp de 300ms.
    const debounceTimer = setTimeout(() => {
      fetch(`http://localhost:8000/search?q=${query}`)
        .then(res => res.json())
        .then(data => setSuggestions(data))
        .catch(err => console.error("Error fetching suggestions:", err));
    }, 300);

    // Curăță timer-ul la fiecare literă nouă tastată
    return () => clearTimeout(debounceTimer);
  }, [query]); // Acest efect rulează de fiecare dată când `query` se schimbă

  const handleSubmit = (searchQuery) => {
    if (searchQuery.trim()) {
      navigate(`/search?q=${searchQuery}`);
      setQuery('');
      setSuggestions([]);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={(e) => { e.preventDefault(); handleSubmit(query); }} className="search-bar">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Caută produse..."
          className="search-input"
          autoComplete="off"
        />
        <button type="submit" className="search-button">
          Caută
        </button>
      </form>

      {/* Afișăm lista de sugestii doar dacă există */}
      {suggestions.length > 0 && (
        <ul className="suggestions-list">
          {suggestions.map(product => (
            <li 
              key={product.id} 
              className="suggestion-item"
              onClick={() => handleSubmit(product.name)}
            >
              {product.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}