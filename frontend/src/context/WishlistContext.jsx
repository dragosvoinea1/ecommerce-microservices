import { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { AuthContext } from './AuthContext';

export const WishlistContext = createContext(null);

export const WishlistProvider = ({ children }) => {
  const [wishlistItems, setWishlistItems] = useState([]);
  const { token } = useContext(AuthContext);

  const fetchWishlist = useCallback(async () => {
    if (!token) {
      setWishlistItems([]); // Golește wishlist-ul la logout
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/wishlist', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setWishlistItems(data);
      }
    } catch (error) {
      console.error("Eroare la preluarea wishlist-ului:", error);
    }
  }, [token]);

  useEffect(() => {
    fetchWishlist();
  }, [token, fetchWishlist]);

  const addToWishlist = async (productId) => {
    try {
      const response = await fetch('http://localhost:8000/wishlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ product_id: productId }),
      });
      if (response.ok) {
        await fetchWishlist(); // Reîncarcă lista după adăugare
      }
    } catch (error) {
      console.error("Eroare la adăugarea în wishlist:", error);
    }
  };

  const removeFromWishlist = async (productId) => {
    try {
      const response = await fetch(`http://localhost:8000/wishlist/${productId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        await fetchWishlist(); // Reîncarcă lista după ștergere
      }
    } catch (error) {
      console.error("Eroare la ștergerea din wishlist:", error);
    }
  };

  // Funcție ajutătoare pentru a verifica dacă un produs este deja în wishlist
  const isProductInWishlist = (productId) => {
    return wishlistItems.some(item => item.product_id === productId);
  };

  return (
    <WishlistContext.Provider value={{ wishlistItems, addToWishlist, removeFromWishlist, isProductInWishlist }}>
      {children}
    </WishlistContext.Provider>
  );
};