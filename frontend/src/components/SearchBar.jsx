import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SearchBar.css'; // Vom crea acest fișier

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      // Navigăm la pagina de rezultate, pasând căutarea ca parametru URL
      navigate(`/search?q=${query}`);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSearch} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Caută produse..."
        className="search-input"
      />
      <button type="submit" className="search-button">
        Caută
      </button>
    </form>
  );
}