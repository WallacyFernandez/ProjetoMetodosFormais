'use client';

import React, { ButtonHTMLAttributes } from 'react';
import styled from 'styled-components';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  fullWidth?: boolean;
}

// Usando um type com $-prefix para as props de estilo
type StyledButtonProps = {
  $variant: 'primary' | 'secondary';
  $fullWidth: boolean;
};

const StyledButton = styled.button<StyledButtonProps>`
  padding: 12px 16px;
  border: none;
  border-radius: ${props => props.theme.borderRadius.lg};
  font-size: ${props => props.theme.fontSizes.md};
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  background-color: ${props => 
    props.$variant === 'secondary' 
      ? props.theme.colors.white 
      : props.theme.colors.primaryGreen};
  color: ${props => 
    props.$variant === 'secondary' 
      ? props.theme.colors.primaryGreen 
      : props.theme.colors.white};
  width: ${props => props.$fullWidth ? '100%' : 'auto'};
  
  &:hover {
    background-color: ${props => 
      props.$variant === 'secondary' 
        ? props.theme.colors.ghostWhite 
        : props.theme.colors.secondaryGreen};
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const Button = ({ 
  children, 
  variant = 'primary', 
  fullWidth = false, 
  ...props 
}: ButtonProps) => {
  // Separando as props de estilo das props do DOM
  return (
    <StyledButton 
      $variant={variant} 
      $fullWidth={fullWidth} 
      {...props}
    >
      {children}
    </StyledButton>
  );
};

export default Button; 