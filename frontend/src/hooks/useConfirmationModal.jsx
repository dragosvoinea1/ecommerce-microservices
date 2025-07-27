import { useState } from 'react';

export const useConfirmationModal = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null); // Vom stoca aici datele (ex: produsul selectat)

  const openModal = (data) => {
    setModalData(data);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setModalData(null);
  };

  return {
    isModalOpen,
    modalData,
    openModal,
    closeModal,
  };
};