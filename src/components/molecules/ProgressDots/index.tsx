'use client';

import React from 'react';
import styled from 'styled-components';

interface ProgressDotsProps {
  totalSteps: number;
  currentStep: number;
}

const DotsContainer = styled.div`
  display: flex;
  width: 100%;
  align-items: center;
  gap: 1rem;
  justify-content: center;
  margin: 1.5rem 0;
`;

const Dot = styled.div<{ $active: boolean; $completed: boolean }>`
  width: ${props => props.$active ? '30%' : '30%'};
  height: 8px;
  border-radius: ${props => props.$active ? '9px' : '9px'};
  background-color: ${props => {
    if (props.$active) return props.theme.colors.primaryGreen;
    if (props.$completed) return props.theme.colors.lightGreen;
    return props.theme.colors.platinum;
  }};
  margin: 0 4px;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: left center;
  opacity: ${props => props.$active ? 1 : 0.6};
`;

const ProgressDots = ({ totalSteps, currentStep }: ProgressDotsProps) => {
  return (
    <DotsContainer>
      {Array.from({ length: totalSteps }, (_, i) => (
        <Dot 
          key={i} 
          $active={i + 1 === currentStep} 
          $completed={i + 1 < currentStep}
        />
      ))}
    </DotsContainer>
  );
};

export default ProgressDots; 