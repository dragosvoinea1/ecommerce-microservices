import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import Modal from '../ui/Modal';
import { useConfirmationModal } from '../../hooks/useConfirmationModal';
import { Link } from 'react-router-dom';
import '../../styles/AdminStyles.css';

export default function ManageProductsPage() {
    // Stare pentru datele formularului
    const [product, setProduct] = useState({
        name: '',
        description: '',
        price: '',
        stock: '',
        image_url: '',
        category_id: '',
        discount_percentage: 0 // <-- VALOARE INIȚIALĂ
    });
    const [categories, setCategories] = useState([]); // Stare pentru a ține minte categoriile
    const [feedback, setFeedback] = useState({ message: '', type: '' });
    const [products, setProducts] = useState([]);
    const { token } = useContext(AuthContext);
    const { isModalOpen, modalData, openModal, closeModal } = useConfirmationModal();



    // Funcție pentru a reîncărca lista de produse
    const fetchProducts = async () => {
        try {
            const response = await fetch('http://localhost:8000/products');
            if (!response.ok) throw new Error('Nu am putut prelua produsele.');
            const data = await response.json();
            setProducts(data);
        } catch (error) {
            setFeedback({ message: error.message, type: 'error' });
        }
    };

    // Încărcăm categoriile la afișarea paginii pentru a le folosi în dropdown
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await fetch('http://localhost:8000/products/categories');
                if (!response.ok) throw new Error('Nu am putut prelua categoriile.');
                const data = await response.json();
                setCategories(data);
                if (data.length > 0) {
                    // Pre-selectăm prima categorie
                    setProduct(prev => ({ ...prev, category_id: data[0].id }));
                }
            } catch (error) {
                setFeedback({ message: error.message, type: 'error' });
            }
        };
        fetchCategories();
        fetchProducts();
    }, []);

    // Funcție generică pentru a actualiza starea formularului
    const handleChange = (e) => {
        const { name, value } = e.target;
        setProduct(prevProduct => ({
            ...prevProduct,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFeedback({ message: '', type: '' });

        // Conversie la tipurile corecte de date
        const productData = {
            ...product,
            price: parseFloat(product.price),
            stock: parseInt(product.stock, 10),
            category_id: parseInt(product.category_id, 10),
            discount_percentage: parseFloat(product.discount_percentage) // <-- CONVERSIE NOUĂ
        };

        try {
            const response = await fetch('http://localhost:8000/products/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(productData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Eroare la adăugarea produsului.');
            }

            setFeedback({ message: 'Produsul a fost adăugat cu succes!', type: 'success' });
            // Resetăm formularul
            setProduct({ name: '', description: '', price: '', stock: '', image_url: '', category_id: categories.length > 0 ? categories[0].id : '', discount_percentage: 0 });
            fetchProducts(); // Reîncărcăm lista de produse

        } catch (err) {
            setFeedback({ message: err.message, type: 'error' });
        }
    };

    const handleDeleteProduct = async () => {
        if (!modalData) return;
        setFeedback({ message: '', type: '' });

        try {
            const response = await fetch(`http://localhost:8000/products/${modalData.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Eroare la ștergerea produsului.');
            }

            setFeedback({ message: 'Produsul a fost șters cu succes!', type: 'success' });
            fetchProducts(); // Reîncarcă lista de produse
            closeModal();

        } catch (err) {
            setFeedback({ message: err.message, type: 'error' });
            closeModal();
        }
    };

    return (
        <div className="admin-container">
            <div className="admin-section">
                <h3>Adaugă Produs Nou</h3>
                <form onSubmit={handleSubmit}>
                    <input name="name" value={product.name} onChange={handleChange} placeholder="Nume produs" required className="admin-input" style={{ marginBottom: '10px' }} />
                    <textarea name="description" value={product.description} onChange={handleChange} placeholder="Descriere" required className="admin-input" style={{ marginBottom: '10px', height: '80px' }} />
                    <input name="price" type="number" value={product.price} onChange={handleChange} placeholder="Preț" required className="admin-input" style={{ marginBottom: '10px' }} />
                    <input name="stock" type="number" value={product.stock} onChange={handleChange} placeholder="Stoc" required className="admin-input" style={{ marginBottom: '10px' }} />
                    <input name="image_url" value={product.image_url} onChange={handleChange} placeholder="URL Imagine" className="admin-input" style={{ marginBottom: '10px' }} />
                    
                    {/* --- CÂMP NOU PENTRU DISCOUNT --- */}
                    <input 
                        name="discount_percentage" 
                        type="number" 
                        value={product.discount_percentage} 
                        onChange={handleChange} 
                        placeholder="Procentaj Discount (ex: 10)" 
                        className="admin-input" 
                        style={{ marginBottom: '10px' }} 
                        step="0.01"
                        min="0"
                        max="100"
                    />

                    <select name="category_id" value={product.category_id} onChange={handleChange} required className="admin-input" style={{ marginBottom: '20px' }}>
                        {categories.map(category => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>

                    <button type="submit" className="admin-button">Adaugă Produs</button>
                </form>
                {feedback.message && <p className={feedback.type === 'error' ? 'admin-error' : ''} style={{ color: feedback.type === 'success' ? 'lightgreen' : '' }}>{feedback.message}</p>}
            </div>
            <div className="admin-section">
                <h3>Produse Existente</h3>
                <ul className="admin-list">
                    {products.map(p => (
                        <li key={p.id} className="admin-list-item">
                            <span>{p.name} ({p.category.name}) - {p.stock} buc.</span>
                            <div>
                                <Link
                                    to={`/admin/products/edit/${p.id}`}
                                    className="admin-button"
                                    style={{ marginRight: '10px' }}
                                >
                                    Edit
                                </Link>
                                <button
                                    onClick={() => openModal(p)}
                                    className="admin-button delete-btn"
                                >
                                    Șterge
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
            <Modal isOpen={isModalOpen} onClose={closeModal}>
                <h3>Confirmare Ștergere</h3>
                <p>Ești sigur că vrei să ștergi produsul "{modalData?.name}"?</p>
                <div className="modal-actions">
                    <button onClick={handleDeleteProduct} className="admin-button confirm-btn">Confirmă</button>
                    <button onClick={closeModal} className="admin-button cancel-btn">Anulează</button>
                </div>
            </Modal>
        </div>
    );
}