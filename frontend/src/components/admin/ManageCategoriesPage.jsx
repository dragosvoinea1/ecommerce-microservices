import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import Modal from '../ui/Modal';
import { useConfirmationModal } from '../../hooks/useConfirmationModal';
import '../../styles/AdminStyles.css';

export default function CategoryManager() {
  const [categories, setCategories] = useState([]);
  const [newCategoryName, setNewCategoryName] = useState('');
  const [error, setError] = useState('');
  const { token } = useContext(AuthContext);
  const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();

  // Funcția pentru a încărca categoriile
  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/products/categories');
      if (!response.ok) throw new Error('Nu am putut prelua categoriile.');
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      setError(err.message);
    }
  };

  // Încărcăm categoriile la afișarea componentei
  useEffect(() => {
    fetchCategories();
  }, []);

  // Funcția pentru a trimite noua categorie la backend
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/products/categories', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`, // Trimitem token-ul de admin
        },
        body: JSON.stringify({ name: newCategoryName }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Eroare la crearea categoriei.');
      }
      
      setNewCategoryName(''); // Golește input-ul
      fetchCategories(); // Reîncarcă lista de categorii

    } catch (err) {
      setError(err.message);
    }
  };

   const handleDelete = async () => {
    if (!modalData) return;
    setError('');

    try {
      const response = await fetch(`http://localhost:8000/products/categories/${modalData.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Eroare la ștergerea categoriei.');
      }
      
      closeModal();
      fetchCategories(); // Reîncarcă lista de categorii

    } catch (err) {
      setError(err.message);
      // Închidem modalul chiar dacă apare o eroare, eroarea va fi afișată
      closeModal(); 
    }
  };

  return (
    // Aplicăm clasele CSS noi
    <div className="admin-container">
      <h2>Admin Console</h2>
      <div className="admin-section">
        <h3>Management Categorii</h3>

        <form onSubmit={handleSubmit} className="admin-form">
          <input 
            type="text"
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            placeholder="Nume categorie nouă"
            required
            className="admin-input" // <-- Clasa nouă
          />
          <button type="submit" className="admin-button">Adaugă Categorie</button> {/* <-- Clasa nouă */}
        </form>

        {error && <p className="admin-error">{error}</p>} {/* <-- Clasa nouă */}

        <hr />

        <h4>Categorii Existente:</h4>
        <ul className="admin-list"> {/* <-- Clasa nouă */}
          {categories.map(category => (
            <li key={category.id} className="admin-list-item"> {/* <-- Clasa nouă */}
              <span>{category.name}</span>
              <button 
                onClick={() => openModal(category)} 
                className="admin-button delete-btn" // <-- Clase noi
              >
                Șterge
              </button>
            </li>
          ))}
        </ul>
      </div>

      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <h3>Confirmare Ștergere</h3>
        <p>Ești sigur că vrei să ștergi categoria "{modalData?.name}"?</p>
        <p style={{color: '#ffdd00', fontSize: '0.8em'}}>
            Atenție: Acest lucru este posibil doar dacă nu există produse în această categorie.
        </p>
        <div className="modal-actions">
          <button onClick={handleDelete} className="admin-button confirm-btn">Confirmă</button>
          <button onClick={closeModal} className="admin-button cancel-btn">Anulează</button>
        </div>
      </Modal>
    </div>
  );
}