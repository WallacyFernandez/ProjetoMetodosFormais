'use client';

import React from 'react';
import Image from 'next/image';
import styled from 'styled-components';

interface LogoProps {
  variant?: 'white' | 'blue';
  width?: number;
  height?: number;
}

const LogoContainer = styled.div<{ width: number; height: number }>`
  width: ${props => props.width}px;
  height: ${props => props.height}px;
  position: relative;
`;

const LogoWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const LogoTag = styled.div`
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px dashed ${props => props.theme.colors.primaryGreen};
  border-radius: ${props => props.theme.borderRadius.sm};
  padding: 4px 8px;
  font-size: ${props => props.theme.fontSizes.sm};
  color: ${props => props.theme.colors.darkText};
  margin-top: 4px;
`;

const Logo = ({ variant = 'blue', width = 120, height = 40 }: LogoProps) => {
  const logoSrc = variant === 'white' ? '/logoWhite.svg' : '/logoBlue.svg';
  
  return (
    <LogoWrapper>
      <LogoContainer width={width} height={height}>
        <Image 
          src={logoSrc} 
          alt="CashLab Logo" 
          fill 
          style={{ objectFit: 'contain' }}
          priority
        />
      </LogoContainer>
    </LogoWrapper>
  );
};

export default Logo; 