'use client';

import React, { InputHTMLAttributes } from 'react';
import styled from 'styled-components';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  width: 100%;
`;

const InputLabel = styled.label`
  font-size: ${props => props.theme.fontSizes.sm};
  font-weight: 500;
  margin-bottom: 8px;
  color: ${props => props.theme.colors.darkText};
`;

const StyledInput = styled.input`
  padding: 12px;
  border: 1px solid ${props => props.theme.colors.platinum};
  border-radius: ${props => props.theme.borderRadius.md};
  font-size: ${props => props.theme.fontSizes.md};
  width: 100%;
  outline: none;
  
  &:focus {
    border-color: ${props => props.theme.colors.primaryGreen};
    box-shadow: 0 0 0 2px ${props => props.theme.colors.paleGreen};
  }
`;

const Input = ({ label, ...props }: InputProps) => {
  return (
    <InputContainer>
      {label && <InputLabel>{label}</InputLabel>}
      <StyledInput {...props} />
    </InputContainer>
  );
};

export default Input; 