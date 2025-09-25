"use client";

import React, { useState, useEffect, useContext } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import {
  MdShoppingCart,
  MdInventory,
  MdTrendingUp,
  MdTrendingDown,
  MdAdd,
  MdRemove,
  MdShoppingBag,
  MdStore,
  MdLocalShipping,
  MdWarning,
  MdCheckCircle,
  MdCancel,
} from "react-icons/md";
import { toast } from "react-toastify";
import SideBar from '@/components/organisms/Sidebar';
import { IsSidebarOnContext } from '@/context/IsSidebarOnContext';

import {
  getProducts,
  getSuppliers,
  getSalesSummary,
  simulateSale,
  purchaseProduct,
  getStockStatusColor,
  getStockStatusText,
  getStockStatusIcon,
  formatCurrency,
  formatNumber,
} from "@/services/GameServices";
import {
  Product,
  Supplier,
  SalesSummary,
  ProductPurchase,
  SaleSimulation,
} from "@/types/game";

const Container = styled.div<{ $isCollapsed: boolean }>`
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 5rem;
  margin: auto;
`;

const MainContent = styled.div<{ $isCollapsed: boolean }>`
  background-color: ${({ theme }) => theme.colors.backgroundSecondary};
  margin-left: ${({ $isCollapsed }) => $isCollapsed ? '16rem' : '0rem'};
  transition: all .3s ease-in-out;
  padding: 2rem;
  min-height: 100vh;

  @media (max-width: 1000px) {
    margin-left: ${({ $isCollapsed }) => $isCollapsed ? '18rem' : '7rem'};
  }

  @media (max-width: 834px) {
    margin-left: ${({ $isCollapsed }) => $isCollapsed ? '17rem' : '3rem'};
  }

  @media (max-width: 768px) {
    margin-left: 0;
    padding: 1rem;
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const StatIcon = styled.div<{ color: string }>`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: ${(props) => props.color}20;
  color: ${(props) => props.color};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
`;

const StatContent = styled.div`
  flex: 1;
`;

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const TabsContainer = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid ${(props) => props.theme.colors.border};
`;

const Tab = styled.button<{ $active: boolean }>`
  padding: 0.75rem 1.5rem;
  border: none;
  background: none;
  color: ${(props) =>
    props.$active
      ? props.theme.colors.primaryGreen
      : props.theme.colors.textSecondary};
  border-bottom: 2px solid
    ${(props) => (props.$active ? props.theme.colors.primaryGreen : "transparent")};
  cursor: pointer;
  font-weight: ${(props) => (props.$active ? "600" : "400")};
  transition: all 0.2s ease;

  &:hover {
    color: ${(props) => props.theme.colors.primaryGreen};
  }
`;

const ProductsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
`;

const ProductCard = styled(motion.div)`
  background: ${(props) => props.theme.colors.backgroundSecondary};
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s ease;

  &:hover {
    border-color: ${(props) => props.theme.colors.primaryGreen};
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }
`;

const ProductHeader = styled.div`
  padding: 1rem;
  border-bottom: 1px solid ${(props) => props.theme.colors.border};
`;

const ProductName = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: ${(props) => props.theme.colors.textPrimary};
  margin-bottom: 0.5rem;
`;

const ProductCategory = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const CategoryBadge = styled.span<{ color: string }>`
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  background: ${(props) => props.color}20;
  color: ${(props) => props.color};
  font-size: 0.75rem;
  font-weight: 500;
`;

const ProductContent = styled.div`
  padding: 1rem;
`;

const PriceRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const Price = styled.div`
  font-size: 1.25rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
`;

const ProfitMargin = styled.div<{ $positive: boolean }>`
  font-size: 0.875rem;
  color: ${(props) => (props.$positive ? "#10B981" : "#EF4444")};
  font-weight: 500;
`;

const StockInfo = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const StockStatus = styled.div<{ status: string }>`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: ${(props) => getStockStatusColor(props.status)};
  font-weight: 500;
`;

const StockQuantity = styled.div`
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const ActionsRow = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled(motion.button)<{
  $variant: "primary" | "secondary" | "success" | "warning";
}>`
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;

  ${(props) => {
    switch (props.$variant) {
      case "primary":
        return `
          background: ${props.theme.colors.primaryGreen};
          color: white;
          &:hover { background: ${props.theme.colors.secondaryGreen}; }
        `;
      case "secondary":
        return `
          background: ${props.theme.colors.backgroundTertiary};
          color: ${props.theme.colors.textPrimary};
          &:hover { background: ${props.theme.colors.ghostWhite}; }
        `;
      case "success":
        return `
          background: #10B981;
          color: white;
          &:hover { background: #059669; }
        `;
      case "warning":
        return `
          background: #F59E0B;
          color: white;
          &:hover { background: #D97706; }
        `;
    }
  }}
`;

const SupplierInfo = styled.div`
  padding: 1rem;
  background: ${(props) => props.theme.colors.backgroundTertiary};
  border-top: 1px solid ${(props) => props.theme.colors.border};
`;

const SupplierName = styled.div`
  font-size: 0.875rem;
  color: ${(props) => props.theme.colors.textSecondary};
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Modal = styled(motion.div)`
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

const ModalContent = styled(motion.div)`
  background: ${(props) => props.theme.colors.white};
  border-radius: 16px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const ModalTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${(props) => props.theme.colors.textPrimary};
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 1.5rem;
  color: ${(props) => props.theme.colors.textSecondary};
  cursor: pointer;
`;

const FormGroup = styled.div`
  margin-bottom: 1rem;
`;

const Label = styled.label`
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: ${(props) => props.theme.colors.textPrimary};
  margin-bottom: 0.5rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid ${(props) => props.theme.colors.border};
  border-radius: 8px;
  background: ${(props) => props.theme.colors.backgroundSecondary};
  color: ${(props) => props.theme.colors.textPrimary};
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: ${(props) => props.theme.colors.primaryGreen};
  }
`;

const ModalActions = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
`;

const Button = styled.button<{ $variant: "primary" | "secondary" }>`
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  ${(props) => {
    switch (props.$variant) {
      case "primary":
        return `
          background: ${props.theme.colors.primaryGreen};
          color: white;
          &:hover { background: ${props.theme.colors.secondaryGreen}; }
        `;
      case "secondary":
        return `
          background: ${props.theme.colors.backgroundTertiary};
          color: ${props.theme.colors.textPrimary};
          &:hover { background: ${props.theme.colors.ghostWhite}; }
        `;
    }
  }}
`;

const LoadingSpinner = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  color: ${(props) => props.theme.colors.textSecondary};
`;

const ButtonSpinner = styled.div`
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingButton = styled(ActionButton)`
  position: relative;
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

export default function VendasPage() {
  const { isCollapsed } = useContext(IsSidebarOnContext);
  const [activeTab, setActiveTab] = useState<"products" | "sales">("products");
  const [products, setProducts] = useState<Product[]>([]);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [salesSummary, setSalesSummary] = useState<SalesSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [showPurchaseModal, setShowPurchaseModal] = useState(false);
  const [purchaseQuantity, setPurchaseQuantity] = useState(1);
  
  // Estados de loading específicos para cada produto
  const [productLoadingStates, setProductLoadingStates] = useState<Record<string, {
    purchasing: boolean;
  }>>({});

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [productsData, suppliersData, salesData] = await Promise.all([
        getProducts(),
        getSuppliers(),
        getSalesSummary(),
      ]);

      setProducts(productsData);
      setSuppliers(suppliersData);
      setSalesSummary(salesData);
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      toast.error("Erro ao carregar dados do jogo");
    } finally {
      setLoading(false);
    }
  };

  // Funções auxiliares para gerenciar estados de loading
  const setProductLoading = (productId: string, action: 'purchasing', isLoading: boolean) => {
    setProductLoadingStates(prev => ({
      ...prev,
      [productId]: {
        ...prev[productId],
        [action]: isLoading
      }
    }));
  };

  const getProductLoading = (productId: string, action: 'purchasing') => {
    return productLoadingStates[productId]?.[action] || false;
  };

  // Função para atualizar apenas um produto específico
  const updateProduct = (updatedProduct: Product) => {
    setProducts(prev => prev.map(p => p.id === updatedProduct.id ? updatedProduct : p));
  };

  const handlePurchase = async () => {
    if (!selectedProduct) return;

    try {
      setProductLoading(selectedProduct.id, 'purchasing', true);
      
      const purchaseData: ProductPurchase = {
        product_id: selectedProduct.id,
        quantity: purchaseQuantity,
        description: `Compra de ${purchaseQuantity} unidades de ${selectedProduct.name}`,
      };

      const result = await purchaseProduct(selectedProduct.id, purchaseData);
      
      // Atualizar apenas o produto específico
      updateProduct(result.product);
      
      toast.success("Compra realizada com sucesso!");
      setShowPurchaseModal(false);
      setPurchaseQuantity(1);
    } catch (error) {
      console.error("Erro ao comprar produto:", error);
      toast.error("Erro ao realizar compra");
    } finally {
      setProductLoading(selectedProduct.id, 'purchasing', false);
    }
  };

  const getSupplierById = (supplierId: string) => {
    return suppliers.find((s) => s.id === supplierId);
  };

  if (loading) {
    return (
      <Container $isCollapsed={isCollapsed}>
        <SideBar />
        <MainContent $isCollapsed={isCollapsed}>
          <LoadingSpinner>
            <MdStore size={24} />
            <span style={{ marginLeft: "0.5rem" }}>
              Carregando dados do supermercado...
            </span>
          </LoadingSpinner>
        </MainContent>
      </Container>
    );
  }

  return (
    <Container $isCollapsed={!isCollapsed}>
      <SideBar />
      <MainContent $isCollapsed={!isCollapsed}>
      <Header>
        <Title>
          <MdShoppingCart />
          Sistema de Vendas
        </Title>
      </Header>

      {/* Estatísticas */}
      <StatsGrid>
        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <StatIcon color="#10B981">
            <MdInventory />
          </StatIcon>
          <StatContent>
            <StatValue>{products.length}</StatValue>
            <StatLabel>Produtos Cadastrados</StatLabel>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <StatIcon color="#F59E0B">
            <MdWarning />
          </StatIcon>
          <StatContent>
            <StatValue>
              {products.filter((p) => p.is_low_stock).length}
            </StatValue>
            <StatLabel>Produtos com Estoque Baixo</StatLabel>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <StatIcon color="#EF4444">
            <MdCancel />
          </StatIcon>
          <StatContent>
            <StatValue>
              {products.filter((p) => p.is_out_of_stock).length}
            </StatValue>
            <StatLabel>Produtos Fora de Estoque</StatLabel>
          </StatContent>
        </StatCard>

        <StatCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <StatIcon color="#3B82F6">
            <MdTrendingUp />
          </StatIcon>
          <StatContent>
            <StatValue>
              {formatCurrency(salesSummary?.total_revenue || 0)}
            </StatValue>
            <StatLabel>Receita Total</StatLabel>
          </StatContent>
        </StatCard>
      </StatsGrid>

      {/* Abas */}
      <TabsContainer>
        <Tab
          $active={activeTab === "products"}
          onClick={() => setActiveTab("products")}
        >
          Produtos e Estoque
        </Tab>
        <Tab
          $active={activeTab === "sales"}
          onClick={() => setActiveTab("sales")}
        >
          Vendas e Relatórios
        </Tab>
      </TabsContainer>

      {/* Conteúdo das Abas */}
      <AnimatePresence mode="wait">
        {activeTab === "products" && (
          <motion.div
            key="products"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <ProductsGrid>
              {products.map((product, index) => (
                <ProductCard
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                >
                  <ProductHeader>
                    <ProductName>{product.name}</ProductName>
                    <ProductCategory>
                      <CategoryBadge color={product.category_color}>
                        {product.category_name}
                      </CategoryBadge>
                    </ProductCategory>
                  </ProductHeader>

                  <ProductContent>
                    <PriceRow>
                      <Price>{formatCurrency(product.current_price)}</Price>
                      <ProfitMargin $positive={product.profit_margin > 0}>
                        {product.profit_margin_formatted}
                      </ProfitMargin>
                    </PriceRow>

                    <StockInfo>
                      <StockStatus status={product.stock_status}>
                        {getStockStatusIcon(product.stock_status)}
                        {getStockStatusText(product.stock_status)}
                      </StockStatus>
                      <StockQuantity>
                        {formatNumber(product.current_stock)} /{" "}
                        {formatNumber(product.max_stock)}
                      </StockQuantity>
                    </StockInfo>

                    <ActionsRow>
                      <LoadingButton
                        $variant="primary"
                        disabled={getProductLoading(product.id, 'purchasing')}
                        onClick={() => {
                          setSelectedProduct(product);
                          setShowPurchaseModal(true);
                        }}
                        whileHover={{ scale: getProductLoading(product.id, 'purchasing') ? 1 : 1.05 }}
                        whileTap={{ scale: getProductLoading(product.id, 'purchasing') ? 1 : 0.95 }}
                      >
                        {getProductLoading(product.id, 'purchasing') ? (
                          <ButtonSpinner />
                        ) : (
                          <>
                            <MdAdd />
                            Comprar
                          </>
                        )}
                      </LoadingButton>
                    </ActionsRow>
                  </ProductContent>

                  <SupplierInfo>
                    <SupplierName>
                      <MdLocalShipping />
                      {getSupplierById(product.supplier)?.name ||
                        "Fornecedor não encontrado"}
                    </SupplierName>
                  </SupplierInfo>
                </ProductCard>
              ))}
            </ProductsGrid>
          </motion.div>
        )}

        {activeTab === "sales" && (
          <motion.div
            key="sales"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <div
              style={{ textAlign: "center", padding: "2rem", color: "#6B7280" }}
            >
              <MdTrendingUp size={48} style={{ marginBottom: "1rem" }} />
              <h3>Relatórios de Vendas</h3>
              <p>
                Em breve: gráficos de vendas, produtos mais vendidos e análises
                detalhadas
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Modal de Compra */}
      <AnimatePresence>
        {showPurchaseModal && selectedProduct && (
          <Modal
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowPurchaseModal(false)}
          >
            <ModalContent
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e: React.MouseEvent) => e.stopPropagation()}
            >
              <ModalHeader>
                <ModalTitle>Comprar {selectedProduct.name}</ModalTitle>
                <CloseButton onClick={() => setShowPurchaseModal(false)}>
                  ×
                </CloseButton>
              </ModalHeader>

              <FormGroup>
                <Label>Quantidade</Label>
                <Input
                  type="number"
                  min="1"
                  value={purchaseQuantity}
                  onChange={(e) =>
                    setPurchaseQuantity(parseInt(e.target.value) || 1)
                  }
                />
              </FormGroup>

              <div
                style={{
                  background: "#F3F4F6",
                  padding: "1rem",
                  borderRadius: "8px",
                  marginBottom: "1rem",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "0.5rem",
                  }}
                >
                  <span>Preço unitário:</span>
                  <span>{formatCurrency(selectedProduct.purchase_price)}</span>
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontWeight: "bold",
                  }}
                >
                  <span>Total:</span>
                  <span>
                    {formatCurrency(
                      selectedProduct.purchase_price * purchaseQuantity,
                    )}
                  </span>
                </div>
              </div>

              <ModalActions>
                <Button
                  $variant="secondary"
                  onClick={() => setShowPurchaseModal(false)}
                >
                  Cancelar
                </Button>
                <LoadingButton 
                  $variant="primary" 
                  disabled={selectedProduct ? getProductLoading(selectedProduct.id, 'purchasing') : false}
                  onClick={handlePurchase}
                >
                  {selectedProduct && getProductLoading(selectedProduct.id, 'purchasing') ? (
                    <ButtonSpinner />
                  ) : (
                    'Confirmar Compra'
                  )}
                </LoadingButton>
              </ModalActions>
            </ModalContent>
          </Modal>
        )}
      </AnimatePresence>

      </MainContent>
    </Container>
  );
}
