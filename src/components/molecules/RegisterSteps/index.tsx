'use client';

import React from 'react';
import styled from 'styled-components';
import Logo from '@/components/atoms/Logo';
import { FaRegUser, FaRegEnvelope } from 'react-icons/fa6';

interface StepProps {
  step: number;
  title: string;
  subtitle: string;
  active: boolean;
}

interface RegisterStepsProps {
  currentStep: number;
}

const StepsContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 2rem;
  gap: 2rem;
`;

const LogoContainer = styled.div`
  margin-bottom: 2.5rem;
  display: flex;
  align-items: center;
`;

const StepIcon = styled.div<{ $active: boolean }>`
  width: 50px;
  height: 50px;
  border: 2px solid ${props => props.$active ? props.theme.colors.input : 'transparent'};
  border-radius: ${props => props.theme.borderRadius.lg};
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  margin-top: 2px;
  position: relative;
  transition: all 0.3s ease;

  svg {
    width: 30px;
    height: 30px;
    color: ${props => props.$active ? props.theme.colors.darkIcon : props.theme.colors.mediumGrey};
    transition: all 0.3s ease;
  }
`;

const Step = styled.div<{ $active: boolean }>`
  display: flex;
  margin-bottom: 1.5rem;
  opacity: ${props => props.$active ? 1 : 0.6};
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);

  &:not(:last-child) ${StepIcon}::after {
    content: '';
    position: absolute;
    top: 110%;
    left: 50%;
    transform: translateX(-50%);
    width: 1px;
    height: 100%;
    background-color: ${props => props.theme.colors.input};
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  }
`;

const StepContent = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
`;

const StepTitle = styled.div`
  font-weight: 600;
  font-size: ${props => props.theme.fontSizes.lg};
  color: ${props => props.theme.colors.darkText};
  margin-bottom: 4px;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
`;

const StepSubtitle = styled.div`
  font-size: ${props => props.theme.fontSizes.md};
  color: ${props => props.theme.colors.mediumGrey};
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
`;

const LogoText = styled.p`
  font-size: ${props => props.theme.fontSizes.lg};
  color: ${props => props.theme.colors.darkText};
  margin-top: 8px;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const STEPS: StepProps[] = [
  {
    step: 1,
    title: "Suas informações",
    subtitle: "Digite as informações necessárias",
    active: false
  },
  {
    step: 2,
    title: "Email e senha",
    subtitle: "Digite seu email e senha",
    active: false
  }
];

const getStepIcon = (step: number) => {
  switch(step) {
    case 1:
      return <FaRegUser />;
    case 2:
      return <FaRegEnvelope />;
    default:
      return null;
  }
};

const RegisterSteps = ({ currentStep }: RegisterStepsProps) => {
  return (
    <StepsContainer>
      <LogoContainer>
          <Logo variant="blue" width={70} height={40} />
          <LogoText>CashLab</LogoText>
      </LogoContainer>
      {STEPS.map((step) => (
        <Step key={step.step} $active={currentStep === step.step}>
          <StepIcon $active={currentStep === step.step}>
            {getStepIcon(step.step)}
          </StepIcon>
          <StepContent>
            <StepTitle>{step.title}</StepTitle>
            <StepSubtitle>{step.subtitle}</StepSubtitle>
          </StepContent>
        </Step>
      ))}
    </StepsContainer>
  );
};

export default RegisterSteps; 