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
                const productIds = wishlistItems.map(item => item.product_id);
                const productPromises = productIds.map(id =>
                    fetch(`http://localhost:8000/products/${id}`).then(res => res.json())
                );
                const productDetails = await Promise.all(productPromises);
                setProducts(productDetails);
            } catch (error) {
                console.error("Eroare la preluarea detaliilor produselor:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchProductDetails();
    }, [wishlistItems]); // Re-rulează efectul când lista de item-uri se schimbă

    if (loading) return <p>Se încarcă wishlist-ul...</p>;

    return (
        <div style={{ padding: '2rem' }}>
            <h2>Wishlist-ul Meu</h2>
            {products.length === 0 ? (
                <p>Nu ai niciun produs în wishlist. Poți adăuga produse apăsând pe iconița cu inimă.</p>
            ) : (
                <div className="product-grid">
                    {products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
}