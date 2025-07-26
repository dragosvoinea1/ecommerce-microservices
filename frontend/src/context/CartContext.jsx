import { createContext, useState } from 'react';

export const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [items, setItems] = useState([]); // Aici vom stoca produsele din coș

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

   const clearCart = () => {
    setItems([]);
  };


  return (
    <CartContext.Provider value={{ items, addToCart, clearCart }}>
      {children}
    </CartContext.Provider>
  );
};