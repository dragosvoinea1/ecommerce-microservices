import { createContext, useState } from 'react';

export const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [items, setItems] = useState([]); // Aici vom stoca produsele din coș

  const addToCart = (product) => {
    setItems((prevItems) => {
      // Verificăm dacă produsul este deja în coș
      const existingItem = prevItems.find((item) => item.id === product.id);

      if (existingItem) {
        // Dacă există, doar incrementăm cantitatea
        return prevItems.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      } else {
        // Dacă nu există, îl adăugăm cu cantitatea 1
        return [...prevItems, { ...product, quantity: 1 }];
      }
    });
  };

  return (
    <CartContext.Provider value={{ items, addToCart }}>
      {children}
    </CartContext.Provider>
  );
};