"use client";

import React, { useState, useRef, useEffect } from "react";
import { styled } from "styled-components";
import { MdKeyboardArrowDown, MdKeyboardArrowUp } from "react-icons/md";
import type { Category } from "@/types/finance";

interface CategoryDropdownProps {
  categories: Category[];
  selectedCategory: string;
  transactionType: string;
  onChange: (categoryId: string) => void;
  required?: boolean;
  placeholder?: string;
}

const DropdownContainer = styled.div`
  position: relative;
  width: 100%;
`;

const DropdownButton = styled.button<{ $isOpen: boolean }>`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-align: left;
  min-height: 48px;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }

  &:hover {
    border-color: ${({ theme }) => theme.colors.primaryBlue};
  }
`;

const DropdownList = styled.div<{ $isOpen: boolean }>`
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
  display: ${({ $isOpen }) => ($isOpen ? "block" : "none")};
  margin-top: 2px;
`;

const DropdownItem = styled.button<{ $isSelected: boolean }>`
  width: 100%;
  padding: 0.75rem;
  border: none;
  background: ${({ $isSelected, theme }) =>
    $isSelected ? theme.colors.primaryBlue + "10" : "white"};
  color: ${({ $isSelected, theme }) =>
    $isSelected ? theme.colors.primaryBlue : theme.colors.textPrimary};
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};

  &:hover {
    background: ${({ theme }) => theme.colors.backgroundSecondary};
  }

  &:last-child {
    border-bottom: none;
  }
`;

const PlaceholderText = styled.span`
  color: ${({ theme }) => theme.colors.textSecondary};
`;

const SelectedText = styled.span`
  color: ${({ theme }) => theme.colors.textPrimary};
`;

export default function CategoryDropdown({
  categories,
  selectedCategory,
  transactionType,
  onChange,
  required = false,
  placeholder = "Selecione uma categoria",
}: CategoryDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const filteredCategories = categories.filter(
    (cat) =>
      cat.category_type === transactionType || cat.category_type === "BOTH",
  );

  const selectedCategoryData = categories.find(
    (cat) => cat.id === selectedCategory,
  );

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleItemClick = (categoryId: string, event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    onChange(categoryId);
    setIsOpen(false);
  };

  return (
    <DropdownContainer ref={dropdownRef}>
      <DropdownButton
        type="button"
        $isOpen={isOpen}
        onClick={() => setIsOpen(!isOpen)}
      >
        {selectedCategoryData ? (
          <SelectedText>{selectedCategoryData.name}</SelectedText>
        ) : (
          <PlaceholderText>{placeholder}</PlaceholderText>
        )}
        {isOpen ? (
          <MdKeyboardArrowUp size={20} />
        ) : (
          <MdKeyboardArrowDown size={20} />
        )}
      </DropdownButton>

      <DropdownList $isOpen={isOpen}>
        {filteredCategories.map((category) => (
          <DropdownItem
            key={category.id}
            $isSelected={selectedCategory === category.id}
            onClick={(e) => handleItemClick(category.id, e)}
          >
            {category.icon} {category.name}
          </DropdownItem>
        ))}
      </DropdownList>
    </DropdownContainer>
  );
}
