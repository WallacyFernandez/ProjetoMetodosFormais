"use client";

import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import Button from "@/components/atoms/Button";
import TextLink from "@/components/atoms/TextLink";
import ProgressSteps from "@/components/atoms/ProgressSteps";
import CodeInput from "@/components/atoms/CodeInput";
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

const CodeContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
`;

const ResendLinkContainer = styled.div`
  text-align: center;
  margin-bottom: 24px;
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.darkText};

  a {
    color: ${(props) => props.theme.colors.primaryGreen};
    text-decoration: underline;
    cursor: pointer;

    &:hover {
      color: ${(props) => props.theme.colors.secondaryGreen};
    }
  }
`;

const BackLinkContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 16px;
`;

const ForgotPasswordCode = () => {
  const [code, setCode] = useState(["", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);
  const router = useRouter();

  useEffect(() => {
    inputRefs.current = inputRefs.current.slice(0, 4);
  }, []);

  const handleCodeChange = (index: number, value: string) => {
    if (value.length > 1) return; // Limita a um caractere por campo

    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    // Move para o próximo campo se um valor foi inserido
    if (value && index < 3) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (
    index: number,
    e: React.KeyboardEvent<HTMLInputElement>,
  ) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      // Move para o campo anterior se o campo atual estiver vazio e backspace for pressionado
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const fullCode = code.join("");
    if (fullCode.length !== 4) {
      return;
    }

    // Aqui seria feita a validação do código com o backend
    console.log("Código enviado:", fullCode);

    // Redireciona para a próxima tela (nova senha)
    router.push("/recuperar-senha/nova-senha");
  };

  const handleResendCode = () => {
    // Aqui seria feita a chamada para reenviar o código
    console.log("Reenviando código...");
  };

  return (
    <FormContainer>
      <FormTitle>Esqueceu sua senha?</FormTitle>
      <FormSubtitle>
        Nós enviamos um código para example@example.com
      </FormSubtitle>

      <form onSubmit={handleSubmit}>
        <CodeContainer>
          {code.map((digit, index) => (
            <CodeInput
              key={index}
              ref={(el) => (inputRefs.current[index] = el)}
              value={digit}
              onChange={(value) => handleCodeChange(index, value)}
              onKeyDown={(e) => handleKeyDown(index, e)}
              autoFocus={index === 0}
            />
          ))}
        </CodeContainer>

        <ResendLinkContainer>
          Não recebeu o código?{" "}
          <a onClick={handleResendCode}>Clique aqui para reenviar</a>
        </ResendLinkContainer>

        <Button type="submit" fullWidth>
          Continuar
        </Button>
      </form>

      <BackLinkContainer>
        <TextLink href="/recuperar-senha" color="secondary">
          Voltar
        </TextLink>
      </BackLinkContainer>

      <ProgressSteps currentStep={2} totalSteps={3} />
    </FormContainer>
  );
};

export default ForgotPasswordCode;
