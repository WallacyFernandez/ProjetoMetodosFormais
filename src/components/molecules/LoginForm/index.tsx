"use client";

import React, { useContext, useState } from "react";
import styled from "styled-components";
import Input from "@/components/atoms/Input";
import Button from "@/components/atoms/Button";
import TextLink from "@/components/atoms/TextLink";
import Logo from "@/components/atoms/Logo";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { storage } from "@/utils/Storage";
import { UserDataContext } from "@/context/UserDataContext";
import { GetUserData, Login } from "@/services/AuthServices";
import { ErrorToast } from "@/utils/Toastify";
import { toast } from "react-toastify";
import { getErrorMessage } from "@/utils/httpErrorToast";
import type { HttpError } from "@/services/httpClient";

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

const ForgotPasswordContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 16px;
`;

const LogoContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
`;

const LogoText = styled.p`
  font-size: ${(props) => props.theme.fontSizes.lg};
  color: ${(props) => props.theme.colors.darkText};
  margin-top: 8px;
  font-weight: 600;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const RegisterLink = styled.div`
  margin-top: 20px;
  text-align: center;
  font-size: ${(props) => props.theme.fontSizes.sm};

  a {
    color: ${(props) => props.theme.colors.primaryGreen};
    text-decoration: none;
    font-weight: 500;

    &:hover {
      text-decoration: underline;
    }
  }
`;

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { user, setUser } = useContext(UserDataContext);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email?.trim() || !password?.trim()) {
      console.log("Error getting email or password", email, password);
      return;
    }

    const Auth = () => {
      const login = async () => {
        try {
          const data = await Login(email, password);
          if (data?.access) {
            return true;
          } else {
            console.log("Failed getting tokens.");
            return false;
          }
        } catch (error) {
          console.error("Failed login:", error);
          throw error; // Re-throw para ser capturado no catch externo
        }
      };

      const fetchUserData = async () => {
        try {
          const getData = await GetUserData();
          if (getData) {
            setUser({
              id: getData.id,
              username: getData.username,
              name: getData.name ?? "",
              email: getData.email ?? "",
              groups: (getData.groups as unknown as string[]) ?? [],
            });
          }
        } catch (error) {
          console.log("Failed getting data.", error);
        }
      };

      return { login, fetchUserData };
    };

    const { login, fetchUserData } = Auth();

    const toastId = toast.loading("Realizando login...");
    try {
      const success = await login();
      if (!success) {
        throw new Error("Falha no login");
      }
      await fetchUserData();
      // marca para exibir o toast no dashboard
      if (typeof window !== "undefined") {
        sessionStorage.setItem("justLoggedIn", "true");
      }
      toast.dismiss(toastId);
      router.replace("/dashboard");
    } catch (err: any) {
      const errorMessage = getErrorMessage(
        err as HttpError,
        "Falha ao fazer o login. Verifique suas credenciais.",
      );
      toast.update(toastId, {
        render: errorMessage,
        type: "error",
        isLoading: false,
        autoClose: 4000,
      });
      ErrorToast(errorMessage);
    }
  };

  return (
    <FormContainer>
      <LogoContainer>
        <Logo variant="blue" width={70} height={40} />
        <LogoText>CashLab</LogoText>
      </LogoContainer>
      <FormTitle>Acesse sua conta</FormTitle>
      <FormSubtitle>Digite as informações necessárias abaixo.</FormSubtitle>

      <form onSubmit={handleSubmit}>
        <Input
          label="Email"
          type="email"
          placeholder="Digite seu email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <Input
          label="Senha"
          type="password"
          placeholder="Digite sua senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <Button type="submit" fullWidth>
          Entrar
        </Button>

        <ForgotPasswordContainer>
          <TextLink href="/recuperar-senha">Esqueceu sua senha?</TextLink>
        </ForgotPasswordContainer>
      </form>
      <RegisterLink>
        Não tem uma conta? <Link href="/cadastro">Cadastre-se</Link>
      </RegisterLink>
    </FormContainer>
  );
};

export default LoginForm;
