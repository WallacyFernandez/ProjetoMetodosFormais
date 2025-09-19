"use client";

import React, { useState } from "react";
import styled from "styled-components";
import Input from "@/components/atoms/Input";
import Button from "@/components/atoms/Button";
import TextLink from "@/components/atoms/TextLink";
import ProgressSteps from "@/components/atoms/ProgressSteps";
import Logo from "@/components/atoms/Logo";
import Link from "next/link";
import { useRouter } from "next/navigation";

const FormContainer = styled.div`
  width: 100%;
  max-width: 400px;
`;

const FormTitle = styled.h1`
  text-align: center;
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: ${(props) => props.theme.colors.darkText};
`;

const FormSubtitle = styled.p`
  text-align: center;
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.darkText};
  margin-bottom: 24px;
`;

const BackLinkContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 16px;
`;

const LogoContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
`;

const LogoText = styled.p`
  font-size: ${(props) => props.theme.fontSizes.lg};
  color: ${(props) => props.theme.colors.darkText};
  font-weight: 600;
  margin: 0;
`;

const ForgotPasswordEmail = () => {
  const [email, setEmail] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email?.trim()) {
      return;
    }

    // Aqui seria feita a chamada para o backend
    // Por enquanto, apenas simula o envio
    console.log("Email enviado:", email);

    // Redireciona para a próxima tela (código)
    router.push("/recuperar-senha/codigo");
  };

  return (
    <FormContainer>
      <LogoContainer>
        <Logo variant="blue" width={70} height={40} />
        <LogoText>CashLab</LogoText>
      </LogoContainer>
      <FormTitle>Esqueceu sua senha?</FormTitle>
      <FormSubtitle>Siga as instruções enviadas para o email</FormSubtitle>

      <form onSubmit={handleSubmit}>
        <Input
          label="Email"
          type="email"
          placeholder="Digite seu email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <Button type="submit" fullWidth>
          Continuar
        </Button>
      </form>

      <BackLinkContainer>
        <TextLink href="/" color="secondary">
          Voltar
        </TextLink>
      </BackLinkContainer>

      <ProgressSteps currentStep={1} totalSteps={3} />
    </FormContainer>
  );
};

export default ForgotPasswordEmail;
