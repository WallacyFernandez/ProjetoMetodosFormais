"use client";

import React from "react";
import styled from "styled-components";

interface ProgressStepsProps {
  currentStep: number;
  totalSteps: number;
}

const ProgressContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 32px;
`;

const ProgressStep = styled.div<{ $active: boolean }>`
  width: 40px;
  height: 4px;
  background-color: ${(props) =>
    props.$active
      ? props.theme.colors.primaryGreen
      : props.theme.colors.platinum};
  border-radius: 2px;
  transition: background-color 0.2s ease-in-out;
`;

const ProgressSteps = ({ currentStep, totalSteps }: ProgressStepsProps) => {
  return (
    <ProgressContainer>
      {Array.from({ length: totalSteps }, (_, index) => (
        <ProgressStep key={index} $active={index === currentStep - 1} />
      ))}
    </ProgressContainer>
  );
};

export default ProgressSteps;

