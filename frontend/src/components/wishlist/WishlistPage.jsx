import { useState, useEffect, useContext } from 'react';
import { WishlistContext } from '../../context/WishlistContext';
import ProductCard from '../product/ProductCard';

export default function WishlistPage() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const { wishlistItems } = useContext(WishlistContext);

    useEffect(() => {
        const fetchProductDetails = async () => {
            if (wishlistItems.length === 0) {
                setProducts([]);
                setLoading(false);
                return;
            }
            
            setLoading(true);
            try {
                // Creăm o listă de promisiuni care aduc detaliile fiecărui produs
                const productPromises = wishlistItems.map(async (item) => {
                    const response = await fetch(`http://localhost:8000/products/${item.product_id}`);
                    
                    // --- AICI ESTE CORECTURA CHEIE ---
                    // Verificăm dacă request-ul a avut succes (status 2xx)
                    if (!response.ok) {
                        return null; // Returnăm null dacă produsul nu există
                    }
                    return response.json();
                });

                // Așteptăm ca toate request-urile să se termine
                const productDetails = await Promise.all(productPromises);

                // Filtrăm produsele care nu au fost găsite (cele care sunt null)
                // înainte de a actualiza starea componentei.
                setProducts(productDetails.filter(p => p !== null));
                
            } catch (error) {
                console.error("Eroare la preluarea detaliilor produselor:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchProductDetails();
    }, [wishlistItems]);

    if (loading) return <p>Se încarcă wishlist-ul...</p>;

    return (
        <div style={{ padding: '2rem' }}>
            <h2>Wishlist-ul Meu</h2>
            {products.length === 0 ? (
                <p>Nu ai niciun produs în wishlist. Poți adăuga produse apăsând pe iconița cu inimă.</p>
            ) : (
                <div className="product-grid">
                    {products.map(product => (
                        // Acum, 'product' este garantat a fi un obiect valid
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
}