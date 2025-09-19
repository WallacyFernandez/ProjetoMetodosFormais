"use client";

import React from "react";
import styled from "styled-components";
import Logo from "@/components/atoms/Logo";
import ForgotPasswordEmail from "@/components/molecules/ForgotPasswordEmail";
import ForgotPasswordCode from "@/components/molecules/ForgotPasswordCode";
import ForgotPasswordNewPassword from "@/components/molecules/ForgotPasswordNewPassword";

interface ForgotPasswordContainerProps {
  step: "email" | "code" | "newPassword";
}

const Container = styled.div`
  display: flex;
  width: 100%;
  height: 100vh;
`;

const LeftPanel = styled.div`
  flex: 1;
  background-color: ${(props) => props.theme.colors.primaryGreen};
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
`;

const RightPanel = styled.div`
  flex: 1;
  background-color: ${(props) => props.theme.colors.white};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
`;

const LogoContainer = styled.div`
  position: absolute;
  top: 30px;
  right: 30px;
`;

const WhiteLogoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 300px;
`;

const ForgotPasswordContainer = ({ step }: ForgotPasswordContainerProps) => {
  const renderStep = () => {
    switch (step) {
      case "email":
        return <ForgotPasswordEmail />;
      case "code":
        return <ForgotPasswordCode />;
      case "newPassword":
        return <ForgotPasswordNewPassword />;
      default:
        return <ForgotPasswordEmail />;
    }
  };

  return (
    <Container>
      <LeftPanel>
        <WhiteLogoContainer>
          <Logo variant="white" width={540} height={400} />
        </WhiteLogoContainer>
      </LeftPanel>

      <RightPanel>
        {renderStep()}
      </RightPanel>
    </Container>
  );
};

export default ForgotPasswordContainer;

