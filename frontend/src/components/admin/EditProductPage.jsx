import { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import '../../styles/AdminStyles.css';

const initialFormState = {
    name: '',
    description: '',
    price: '',
    stock: '',
    image_url: '',
    category_id: ''
};

export default function EditProductPage() {
    const { productId } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(initialFormState);
    const [categories, setCategories] = useState([]);
    const [feedback, setFeedback] = useState({ message: '', type: '' });
    const { token } = useContext(AuthContext);

    useEffect(() => {
        // Fetch categorii pentru dropdown
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

        // Fetch datele produsului curent
        const fetchProductData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/products/${productId}`);
                if (!response.ok) throw new Error('Nu am putut prelua datele produsului.');
                const data = await response.json();
                // Asigurăm că `category_id` este setat corect pentru formular
                setProduct({
                    name: data.name || '',
                    description: data.description || '',
                    price: data.price || '',
                    stock: data.stock || '',
                    image_url: data.image_url || '',
                    category_id: data.category.id || ''
                });
            } catch (error) {
                setFeedback({ message: error.message, type: 'error' });
            }
        };

        fetchCategories();
        fetchProductData();
    }, [productId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProduct(prevProduct => ({
            ...prevProduct,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const productData = {
            name: product.name,
            description: product.description,
            price: parseFloat(product.price),
            stock: parseInt(product.stock, 10),
            image_url: product.image_url,
            category_id: parseInt(product.category_id, 10)
        };

        try {
            const response = await fetch(`http://localhost:8000/products/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(productData),
            });
            if (!response.ok) throw new Error('Eroare la actualizarea produsului.');

            setFeedback({ message: 'Produs actualizat cu succes!', type: 'success' });
            setTimeout(() => navigate('/admin/products'), 1500); // Redirecționare după 1.5s
        } catch (error) {
            setFeedback({ message: error.message, type: 'error' });
        }
    };

    if (!product) return <p>Se încarcă...</p>;

    return (
        <div className="admin-container">
            <div className="admin-section">
                <h3>Editează Produs: {product.name}</h3>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="name">Nume Produs</label>
                        <input
                            id="name"
                            name="name"
                            value={product.name}
                            onChange={handleChange}
                            required
                            className="admin-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="description">Descriere</label>
                        <textarea
                            id="description"
                            name="description"
                            value={product.description}
                            onChange={handleChange}
                            required
                            className="admin-input"
                            style={{ height: '80px' }}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="price">Preț (RON)</label>
                        <input
                            id="price"
                            name="price"
                            type="number"
                            value={product.price}
                            onChange={handleChange}
                            required
                            className="admin-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="stock">Stoc (bucăți)</label>
                        <input
                            id="stock"
                            name="stock"
                            type="number"
                            value={product.stock}
                            onChange={handleChange}
                            required
                            className="admin-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="image_url">URL Imagine</label>
                        <input
                            id="image_url"
                            name="image_url"
                            value={product.image_url}
                            onChange={handleChange}
                            className="admin-input"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="category_id">Categorie</label>
                        <select
                            id="category_id"
                            name="category_id"
                            value={product.category_id}
                            onChange={handleChange}
                            required
                            className="admin-input"
                        >
                            {categories.map(category => (
                                <option key={category.id} value={category.id}>{category.name}</option>
                            ))}
                        </select>
                    </div>

                    <button type="submit" className="admin-button" style={{ marginTop: '10px' }}>Salvează Modificările</button>
                </form>

                {feedback.message && (
                    <p
                        className={feedback.type === 'error' ? 'admin-error' : ''}
                        style={{ color: feedback.type === 'success' ? 'lightgreen' : '', marginTop: '15px' }}
                    >
                        {feedback.message}
                    </p>
                )}
            </div>
        </div>
    );
}