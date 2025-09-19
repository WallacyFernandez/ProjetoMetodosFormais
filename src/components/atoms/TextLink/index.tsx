'use client';

import React from 'react';
import Link from 'next/link';
import styled from 'styled-components';

interface TextLinkProps {
  href: string;
  children: React.ReactNode;
  color?: 'primary' | 'secondary';
}

const StyledLink = styled(Link)<{ $color: 'primary' | 'secondary' }>`
  color: ${props => props.$color === 'primary' 
    ? props.theme.colors.primaryGreen 
    : props.theme.colors.darkText};
  text-decoration: none;
  font-size: ${props => props.theme.fontSizes.md};
  transition: color 0.2s ease-in-out;
  font-weight: 500;
  
  &:hover {
    color: ${props => props.theme.colors.secondaryGreen};
    text-decoration: underline;
  }
`;

const TextLink = ({ href, children, color = 'primary' }: TextLinkProps) => {
  return (
    <StyledLink href={href} $color={color}>
      {children}
    </StyledLink>
  );
};

export default TextLink; 