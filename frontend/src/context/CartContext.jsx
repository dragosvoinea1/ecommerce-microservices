import { createContext, useState, useEffect } from 'react';

export const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [items, setItems] = useState(() => {
    try {
      const storedItems = localStorage.getItem('cartItems');
      return storedItems ? JSON.parse(storedItems) : [];
    } catch (error) {
      console.error("Eroare la citirea coșului din localStorage", error);
      return [];
    }
  });


  useEffect(() => {
    try {
      localStorage.setItem('cartItems', JSON.stringify(items));
    } catch (error) {
      console.error("Eroare la salvarea coșului în localStorage", error);
    }
  }, [items]); 

  const addToCart = (product, quantity = 1) => { // <-- Am adăugat parametrul 'quantity'
    setItems((prevItems) => {
      // Verificăm dacă produsul este deja în coș
      const existingItem = prevItems.find((item) => item.id === product.id);

      const priceToAdd = product.discount_percentage && product.discount_percentage > 0
        ? product.price * (1 - product.discount_percentage / 100)
        : product.price;

      if (existingItem) {
        // Dacă există, adunăm noua cantitate la cea existentă
        return prevItems.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity } // <-- Folosim noua cantitate
            : item
        );
      } else {
        // Dacă nu există, îl adăugăm cu cantitatea specificată
        return [...prevItems, { ...product, quantity, price: priceToAdd }];
      }
    });
  };
   
  const removeFromCart = (productId) => {
    setItems((prevItems) => {
      return prevItems.filter(item => item.id !== productId);
    });
  };

   const clearCart = () => {
    setItems([]);
  };


  return (
    <CartContext.Provider value={{ items, addToCart, clearCart, removeFromCart }}>
      {children}
    </CartContext.Provider>
  );
};