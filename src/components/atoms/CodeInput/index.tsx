"use client";

import React, { forwardRef } from "react";
import styled from "styled-components";

interface CodeInputProps {
  value: string;
  onChange: (value: string) => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  autoFocus?: boolean;
}

const StyledCodeInput = styled.input`
  width: 60px;
  height: 60px;
  border: 1px solid ${(props) => props.theme.colors.platinum};
  border-radius: ${(props) => props.theme.borderRadius.md};
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  outline: none;

  &:focus {
    border-color: ${(props) => props.theme.colors.primaryGreen};
    box-shadow: 0 0 0 2px ${(props) => props.theme.colors.paleGreen};
  }
`;

const CodeInput = forwardRef<HTMLInputElement, CodeInputProps>(
  ({ value, onChange, onKeyDown, autoFocus, ...props }, ref) => {
    return (
      <StyledCodeInput
        ref={ref}
        type="text"
        maxLength={1}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={onKeyDown}
        autoFocus={autoFocus}
        {...props}
      />
    );
  },
);

CodeInput.displayName = "CodeInput";

export default CodeInput;

