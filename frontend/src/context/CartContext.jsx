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

  const addToCart = (product) => {
    setItems((prevItems) => {
      const existingItem = prevItems.find((item) => item.id === product.id);

      if (existingItem) {
        return prevItems.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        return [...prevItems, { ...product, quantity: 1 }];
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