"use client";

import React, { useState } from "react";
import styled from "styled-components";
import Input from "@/components/atoms/Input";
import Button from "@/components/atoms/Button";
import ProgressSteps from "@/components/atoms/ProgressSteps";
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

const ForgotPasswordNewPassword = () => {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState<{
    password?: string;
    confirmPassword?: string;
  }>({});
  const router = useRouter();

  const validateForm = () => {
    const newErrors: { password?: string; confirmPassword?: string } = {};

    if (password.length < 8) {
      newErrors.password = "A senha deve ter no mínimo 8 caracteres";
    }

    if (password !== confirmPassword) {
      newErrors.confirmPassword = "As senhas não coincidem";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Aqui seria feita a chamada para o backend para alterar a senha
    console.log("Nova senha definida:", password);

    // Redireciona para o login após sucesso
    router.push("/login");
  };

  return (
    <FormContainer>
      <FormTitle>Escolha sua nova senha</FormTitle>
      <FormSubtitle>Deve ter no mínimo 8 caracteres.</FormSubtitle>

      <form onSubmit={handleSubmit}>
        <Input
          label="Senha"
          type="password"
          placeholder="Escolha sua senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {errors.password && (
          <div
            style={{
              color: "red",
              fontSize: "0.875rem",
              marginTop: "-16px",
              marginBottom: "16px",
            }}
          >
            {errors.password}
          </div>
        )}

        <Input
          label="Confirmar senha"
          type="password"
          placeholder="Escolha sua senha"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        {errors.confirmPassword && (
          <div
            style={{
              color: "red",
              fontSize: "0.875rem",
              marginTop: "-16px",
              marginBottom: "16px",
            }}
          >
            {errors.confirmPassword}
          </div>
        )}

        <Button type="submit" fullWidth>
          Recuperar senha
        </Button>
      </form>

      <ProgressSteps currentStep={3} totalSteps={3} />
    </FormContainer>
  );
};

export default ForgotPasswordNewPassword;
