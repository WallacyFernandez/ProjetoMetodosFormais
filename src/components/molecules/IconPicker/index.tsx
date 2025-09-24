"use client";

import React, { useState, useMemo } from "react";
import { styled } from "styled-components";
import { MdSearch, MdClose } from "react-icons/md";

// Lista de ícones/emojis para categorias financeiras
const CATEGORY_ICONS = [
  // Receitas
  { emoji: "💰", name: "Dinheiro", category: "income" },
  { emoji: "💼", name: "Trabalho", category: "income" },
  { emoji: "📈", name: "Investimentos", category: "income" },
  { emoji: "💻", name: "Freelance", category: "income" },
  { emoji: "🛒", name: "Vendas", category: "income" },
  { emoji: "💸", name: "Outros Ganhos", category: "income" },

  // Despesas
  { emoji: "🍽️", name: "Alimentação", category: "expense" },
  { emoji: "🚗", name: "Transporte", category: "expense" },
  { emoji: "🏠", name: "Moradia", category: "expense" },
  { emoji: "🎉", name: "Lazer", category: "expense" },
  { emoji: "🏥", name: "Saúde", category: "expense" },
  { emoji: "📚", name: "Educação", category: "expense" },
  { emoji: "👕", name: "Vestuário", category: "expense" },
  { emoji: "💻", name: "Tecnologia", category: "expense" },
  { emoji: "🔧", name: "Serviços", category: "expense" },
  { emoji: "🏛️", name: "Impostos", category: "expense" },
  { emoji: "🐕", name: "Pets", category: "expense" },
  { emoji: "❤️", name: "Doações", category: "expense" },
  { emoji: "📋", name: "Outros Gastos", category: "expense" },

  // Ambos
  { emoji: "🎯", name: "Metas", category: "both" },
  { emoji: "📊", name: "Relatórios", category: "both" },
  { emoji: "⚡", name: "Urgente", category: "both" },
  { emoji: "⭐", name: "Favorito", category: "both" },
  { emoji: "🔥", name: "Popular", category: "both" },
  { emoji: "💡", name: "Ideia", category: "both" },
  { emoji: "🎨", name: "Criativo", category: "both" },
  { emoji: "🚀", name: "Novo", category: "both" },
];

interface IconPickerProps {
  selectedIcon?: string;
  onIconSelect: (icon: string) => void;
  categoryType?: "INCOME" | "EXPENSE" | "BOTH";
  onClose: () => void;
}

const PickerContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const PickerModal = styled.div`
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  overflow: hidden;
  animation: slideIn 0.2s ease-out;

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: scale(0.95) translateY(-10px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
`;

const PickerHeader = styled.div`
  padding: 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const PickerTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ theme }) => theme.colors.textPrimary};
  margin: 0;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.colors.textSecondary};
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;

  &:hover {
    background: ${({ theme }) => theme.colors.backgroundSecondary};
  }
`;

const SearchContainer = styled.div`
  padding: 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.primaryBlue};
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: ${({ theme }) => theme.colors.textSecondary};
  pointer-events: none;
`;

const IconsGrid = styled.div`
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 0.5rem;
`;

const IconButton = styled.button<{ $isSelected?: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 0.5rem;
  border: 1px solid
    ${({ $isSelected, theme }) =>
      $isSelected ? theme.colors.primaryBlue : theme.colors.border};
  border-radius: 8px;
  background: ${({ $isSelected, theme }) =>
    $isSelected ? theme.colors.primaryBlue + "10" : "white"};
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.5rem;

  &:hover {
    background: ${({ theme }) => theme.colors.backgroundSecondary};
    border-color: ${({ theme }) => theme.colors.primaryBlue};
  }

  &:active {
    transform: scale(0.95);
  }
`;

const IconName = styled.span`
  font-size: 0.7rem;
  color: ${({ theme }) => theme.colors.textSecondary};
  margin-top: 0.25rem;
  text-align: center;
  line-height: 1;
`;

const CategoryTabs = styled.div`
  display: flex;
  padding: 0 1rem;
  border-bottom: 1px solid ${({ theme }) => theme.colors.border};
`;

const CategoryTab = styled.button<{ $isActive?: boolean }>`
  flex: 1;
  padding: 0.75rem;
  border: none;
  background: none;
  color: ${({ $isActive, theme }) =>
    $isActive ? theme.colors.primaryBlue : theme.colors.textSecondary};
  font-size: 0.9rem;
  font-weight: ${({ $isActive }) => ($isActive ? "600" : "400")};
  cursor: pointer;
  border-bottom: 2px solid
    ${({ $isActive, theme }) =>
      $isActive ? theme.colors.primaryBlue : "transparent"};
  transition: all 0.2s ease;

  &:hover {
    color: ${({ theme }) => theme.colors.primaryBlue};
  }
`;

export default function IconPicker({
  selectedIcon,
  onIconSelect,
  categoryType = "BOTH",
  onClose,
}: IconPickerProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState<
    "all" | "income" | "expense" | "both"
  >("all");

  const filteredIcons = useMemo(() => {
    let filtered = CATEGORY_ICONS;

    // Filtrar por categoria
    if (activeCategory !== "all") {
      filtered = filtered.filter((icon) => icon.category === activeCategory);
    }

    // Filtrar por termo de busca
    if (searchTerm.trim()) {
      filtered = filtered.filter(
        (icon) =>
          icon.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          icon.emoji.includes(searchTerm),
      );
    }

    return filtered;
  }, [searchTerm, activeCategory]);

  const handleIconSelect = (icon: string) => {
    onIconSelect(icon);
    onClose();
  };

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <PickerContainer onClick={handleOverlayClick}>
      <PickerModal>
        <PickerHeader>
          <PickerTitle>Escolher Ícone</PickerTitle>
          <CloseButton onClick={onClose}>
            <MdClose size={20} />
          </CloseButton>
        </PickerHeader>

        <SearchContainer>
          <div style={{ position: "relative" }}>
            <SearchIcon>
              <MdSearch size={16} />
            </SearchIcon>
            <SearchInput
              type="text"
              placeholder="Buscar ícone..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: "2.5rem" }}
            />
          </div>
        </SearchContainer>

        <CategoryTabs>
          <CategoryTab
            $isActive={activeCategory === "all"}
            onClick={() => setActiveCategory("all")}
          >
            Todos
          </CategoryTab>
          <CategoryTab
            $isActive={activeCategory === "income"}
            onClick={() => setActiveCategory("income")}
          >
            Receitas
          </CategoryTab>
          <CategoryTab
            $isActive={activeCategory === "expense"}
            onClick={() => setActiveCategory("expense")}
          >
            Despesas
          </CategoryTab>
          <CategoryTab
            $isActive={activeCategory === "both"}
            onClick={() => setActiveCategory("both")}
          >
            Ambos
          </CategoryTab>
        </CategoryTabs>

        <IconsGrid>
          {filteredIcons.map((icon, index) => (
            <IconButton
              key={index}
              $isSelected={selectedIcon === icon.emoji}
              onClick={() => handleIconSelect(icon.emoji)}
              title={icon.name}
            >
              <span>{icon.emoji}</span>
              <IconName>{icon.name}</IconName>
            </IconButton>
          ))}
        </IconsGrid>

        {filteredIcons.length === 0 && (
          <div
            style={{
              padding: "2rem",
              textAlign: "center",
              color: "#666",
            }}
          >
            Nenhum ícone encontrado
          </div>
        )}
      </PickerModal>
    </PickerContainer>
  );
}
