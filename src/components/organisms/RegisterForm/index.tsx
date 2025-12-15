"use client";

import React, { useState, useContext } from "react";
import styled from "styled-components";
import Logo from "@/components/atoms/Logo";
import Button from "@/components/atoms/Button";
import TextLink from "@/components/atoms/TextLink";
import RegisterSteps from "@/components/molecules/RegisterSteps";
import ProgressDots from "@/components/molecules/ProgressDots";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { Register, GetUserData } from "@/services/AuthServices";
import { UserDataContext } from "@/context/UserDataContext";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import type { RegisterData } from "@/types/api";
import {
  getErrorMessage,
  getFieldError,
  getAllErrorMessages,
  extractFieldErrors,
} from "@/utils/httpErrorToast";
import { validateStrongPassword } from "@/utils/passwordValidation";
import type { HttpError } from "@/services/httpClient";

const Container = styled.div`
  display: flex;
  min-height: 100vh;
  background-color: ${(props) => props.theme.colors.backgroundSecondary};
`;

const LeftSection = styled.div`
  width: 40%;
  display: flex;
  flex-direction: column;
  padding: 5rem 0rem 2rem 9rem;
  justify-content: space-between;
`;

const RightSection = styled.div`
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  padding: 5rem 9rem 2rem 2rem;
`;

const FormContainer = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  max-width: 500px;
  border-radius: ${(props) => props.theme.borderRadius.lg};
  margin-top: 2rem;
  position: relative;
  overflow: hidden;
`;

const FormWrapper = styled.div<{
  $isActive: boolean;
  $step: number;
  $currentStep: number;
}>`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  transform: ${(props) => {
    if (props.$isActive) return "translateY(0)";
    if (props.$step > props.$currentStep) return "translateY(100%)";
    return "translateY(-100%)";
  }};
`;

const FormHeader = styled.div`
  text-align: center;
  margin-bottom: 1.5rem;
`;

const FormTitle = styled.h1`
  font-size: ${(props) => props.theme.fontSizes.xxl};
  font-weight: 600;
  color: ${(props) => props.theme.colors.darkText};
  margin-bottom: 0.5rem;
`;

const FormSubtitle = styled.p`
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.mediumGrey};
`;

const Form = styled.form`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const FormInput = styled.div`
  margin-bottom: 1rem;
`;

const InputLabel = styled.label`
  display: block;
  font-size: ${(props) => props.theme.fontSizes.lg};
  color: ${(props) => props.theme.colors.darkText};
  font-weight: 600;
  margin-bottom: 8px;
`;

const PasswordInputContainer = styled.div`
  position: relative;
  width: 100%;
`;

const PasswordToggleButton = styled.button`
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: ${(props) => props.theme.colors.mediumGrey};
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    color: ${(props) => props.theme.colors.darkText};
  }
`;

const StyledInput = styled.input`
  width: 100%;
  background: transparent;
  padding: 12px;
  color: ${(props) => props.theme.colors.input};
  border: 2px solid ${(props) => props.theme.colors.input};
  border-radius: ${(props) => props.theme.borderRadius.lg};
  font-size: ${(props) => props.theme.fontSizes.md};

  &::placeholder {
    color: ${(props) => props.theme.colors.mediumGrey};
    opacity: 0.7;
  }

  &:focus {
    border-color: ${(props) => props.theme.colors.primaryGreen};
    outline: none;
  }

  /* Estilos para sobrescrever o autofill do navegador */
  &:-webkit-autofill,
  &:-webkit-autofill:hover,
  &:-webkit-autofill:focus,
  &:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px
      ${(props) => props.theme.colors.backgroundSecondary} inset !important;
    -webkit-text-fill-color: ${(props) => props.theme.colors.input} !important;
    transition: background-color 5000s ease-in-out 0s;
  }
`;

const FooterSection = styled.div`
  margin-top: auto;
  max-width: 500px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const LinksContainer = styled.div`
  display: flex;
  justify-content: flex-start;
  margin: 1rem 0;
  gap: 5rem;
`;

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const BackButton = styled(Button)`
  background-color: transparent;
  color: ${(props) => props.theme.colors.mediumGrey};
  border: 2px solid ${(props) => props.theme.colors.mediumGrey};

  &:hover {
    background-color: ${(props) => props.theme.colors.ghostWhite};
    color: ${(props) => props.theme.colors.darkText};
    border-color: ${(props) => props.theme.colors.darkText};
  }
`;

const RegisterForm = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [passwordErrors, setPasswordErrors] = useState<string[]>([]);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    password_confirm: "",
  });
  const totalSteps = 2; // CashLab: 2 passos - informações pessoais e credenciais
  const { setUser } = useContext(UserDataContext);
  const router = useRouter();

  const handlePersonalInfoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentStep(2);
  };

  const handleEmailPasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validação de senha forte
    const passwordValidation = validateStrongPassword(formData.password);

    if (!passwordValidation.isValid) {
      setPasswordErrors(passwordValidation.errors);
      toast.error(
        passwordValidation.errors[0] ||
          "A senha não atende aos requisitos de segurança",
      );
      return;
    }

    setPasswordErrors([]);

    // Verifica se as senhas coincidem
    if (formData.password !== formData.password_confirm) {
      toast.error("As senhas não coincidem");
      return;
    }

    setLoading(true);
    const toastId = toast.loading("Criando sua conta...");

    try {
      // Criar o objeto no formato esperado pela API
      const registerData: RegisterData = {
        email: formData.email,
        username: formData.username,
        password: formData.password,
        password_confirm: formData.password_confirm,
        first_name: formData.first_name,
        last_name: formData.last_name,
      };

      // Registrar usuário
      const response = await Register(registerData);

      // Buscar dados do usuário
      const userData = await GetUserData();

      // Atualizar contexto do usuário
      setUser({
        id: userData.id,
        username: userData.username,
        name:
          userData.full_name || `${userData.first_name} ${userData.last_name}`,
        email: userData.email || "",
        groups: userData.groups || [],
      });

      toast.update(toastId, {
        render: "Conta criada com sucesso! Redirecionando...",
        type: "success",
        isLoading: false,
        autoClose: 2000,
      });

      // Marcar para exibir toast no dashboard
      if (typeof window !== "undefined") {
        sessionStorage.setItem("justRegistered", "true");
      }

      // Redirecionar para dashboard
      setTimeout(() => {
        router.replace("/dashboard");
      }, 2000);
    } catch (error: any) {
      console.error("Erro no cadastro:", error);

      const httpError = error as HttpError;

      // Extrai erros específicos de campos
      const fieldErrors = extractFieldErrors(httpError);

      // Campos da etapa 1 (informações pessoais)
      const step1Fields = ["first_name", "last_name", "username"];

      // Verifica se há erros em campos da etapa 1
      const hasStep1Errors = step1Fields.some((field) => fieldErrors[field]);

      // Se houver erros na etapa 1, volta para ela
      if (hasStep1Errors) {
        setCurrentStep(1);
      }

      // Filtra campos que não são do formulário (como timestamp)
      const formFields = [
        "first_name",
        "last_name",
        "username",
        "email",
        "password",
        "password_confirm",
      ];
      const relevantErrors: Record<string, string[]> = {};

      Object.keys(fieldErrors).forEach((field) => {
        if (formFields.includes(field)) {
          relevantErrors[field] = fieldErrors[field];
        }
      });

      // Monta mensagem de erro
      let errorMessage: string;
      const errorKeys = Object.keys(relevantErrors);

      if (errorKeys.length > 0) {
        // Se houver múltiplos erros relevantes, mostra todos
        if (errorKeys.length > 1) {
          const messages = errorKeys.map((field) => {
            const fieldName =
              field === "first_name"
                ? "Nome"
                : field === "last_name"
                  ? "Sobrenome"
                  : field === "username"
                    ? "Nome de usuário"
                    : field === "email"
                      ? "Email"
                      : field === "password"
                        ? "Senha"
                        : field === "password_confirm"
                          ? "Confirmação de senha"
                          : field;
            return `${fieldName}: ${relevantErrors[field][0]}`;
          });
          errorMessage = `Erros encontrados:\n${messages.join("\n")}`;
        } else {
          // Se houver apenas um erro, mostra diretamente
          const field = errorKeys[0];
          const fieldName =
            field === "first_name"
              ? "Nome"
              : field === "last_name"
                ? "Sobrenome"
                : field === "username"
                  ? "Nome de usuário"
                  : field === "email"
                    ? "Email"
                    : field === "password"
                      ? "Senha"
                      : field === "password_confirm"
                        ? "Confirmação de senha"
                        : field;
          errorMessage = `${fieldName}: ${relevantErrors[field][0]}`;
        }
      } else {
        // Fallback para mensagens genéricas
        errorMessage = getErrorMessage(
          httpError,
          "Erro ao criar conta. Verifique os dados e tente novamente.",
        );
      }

      toast.update(toastId, {
        render: errorMessage,
        type: "error",
        isLoading: false,
        autoClose: 5000,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setCurrentStep((prev) => prev - 1);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container>
      <LeftSection>
        <RegisterSteps currentStep={currentStep} />
        <LinksContainer>
          <TextLink href="/" color="secondary">
            ← Voltar para o início
          </TextLink>
          <TextLink href="/" color="secondary">
            Acesse sua conta
          </TextLink>
        </LinksContainer>
      </LeftSection>
      <RightSection>
        <FormContainer>
          <FormWrapper
            $isActive={currentStep === 1}
            $step={1}
            $currentStep={currentStep}
          >
            <FormHeader>
              <Logo variant="blue" />
              <FormTitle>Suas informações</FormTitle>
              <FormSubtitle>
                Digite as informações necessárias abaixo.
              </FormSubtitle>
            </FormHeader>

            <Form onSubmit={handlePersonalInfoSubmit}>
              <FormInput>
                <InputLabel>Nome</InputLabel>
                <StyledInput
                  placeholder="Digite seu primeiro nome"
                  value={formData.first_name}
                  onChange={(e) =>
                    setFormData({ ...formData, first_name: e.target.value })
                  }
                  required
                />
              </FormInput>
              <FormInput>
                <InputLabel>Sobrenome</InputLabel>
                <StyledInput
                  placeholder="Digite seu sobrenome"
                  value={formData.last_name}
                  onChange={(e) =>
                    setFormData({ ...formData, last_name: e.target.value })
                  }
                  required
                />
              </FormInput>
              <FormInput>
                <InputLabel>Nome de usuário</InputLabel>
                <StyledInput
                  placeholder="Digite seu nome de usuário"
                  value={formData.username}
                  onChange={(e) =>
                    setFormData({ ...formData, username: e.target.value })
                  }
                  required
                />
              </FormInput>
              <Button type="submit" fullWidth>
                Continuar
              </Button>
            </Form>
          </FormWrapper>

          <FormWrapper
            $isActive={currentStep === 2}
            $step={2}
            $currentStep={currentStep}
          >
            <FormHeader>
              <Logo variant="blue" />
              <FormTitle>Email e senha</FormTitle>
              <FormSubtitle>Digite seu email e senha abaixo.</FormSubtitle>
            </FormHeader>

            <Form onSubmit={handleEmailPasswordSubmit}>
              <FormInput>
                <InputLabel>Email</InputLabel>
                <StyledInput
                  type="email"
                  placeholder="Digite seu email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  required
                />
              </FormInput>
              <FormInput>
                <InputLabel>Senha</InputLabel>
                <PasswordInputContainer>
                  <StyledInput
                    type={showPassword ? "text" : "password"}
                    placeholder="Digite sua senha forte"
                    value={formData.password}
                    onChange={(e) => {
                      const newPassword = e.target.value;
                      setFormData({ ...formData, password: newPassword });
                      // Valida em tempo real
                      if (newPassword.length > 0) {
                        const validation = validateStrongPassword(newPassword);
                        setPasswordErrors(validation.errors);
                      } else {
                        setPasswordErrors([]);
                      }
                    }}
                    required
                    minLength={8}
                  />
                  <PasswordToggleButton
                    type="button"
                    onClick={togglePasswordVisibility}
                    aria-label={
                      showPassword ? "Ocultar senha" : "Mostrar senha"
                    }
                  >
                    {showPassword ? (
                      <FaEye size={20} />
                    ) : (
                      <FaEyeSlash size={20} />
                    )}
                  </PasswordToggleButton>
                </PasswordInputContainer>
                {passwordErrors.length > 0 && (
                  <div style={{ marginTop: "8px", fontSize: "0.875rem" }}>
                    {passwordErrors.map((error, index) => (
                      <div
                        key={index}
                        style={{
                          color: "#ef4444",
                          marginBottom: "4px",
                          fontSize: "0.8rem",
                        }}
                      >
                        • {error}
                      </div>
                    ))}
                  </div>
                )}
                {formData.password.length > 0 &&
                  passwordErrors.length === 0 && (
                    <div
                      style={{
                        marginTop: "8px",
                        fontSize: "0.875rem",
                        color: "#10b981",
                      }}
                    >
                      ✓ Senha forte
                    </div>
                  )}
              </FormInput>
              <FormInput>
                <InputLabel>Confirmar Senha*</InputLabel>
                <StyledInput
                  type="password"
                  placeholder="Confirme sua senha"
                  value={formData.password_confirm}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      password_confirm: e.target.value,
                    })
                  }
                  required
                />
              </FormInput>
              <ButtonContainer>
                <Button type="submit" fullWidth disabled={loading}>
                  {loading ? "Criando conta..." : "Finalizar Cadastro"}
                </Button>
                <BackButton
                  type="button"
                  fullWidth
                  onClick={handleBack}
                  disabled={loading}
                >
                  Voltar
                </BackButton>
              </ButtonContainer>
            </Form>
          </FormWrapper>
        </FormContainer>
        <FooterSection>
          <ProgressDots totalSteps={totalSteps} currentStep={currentStep} />
        </FooterSection>
      </RightSection>
    </Container>
  );
};

export default RegisterForm;
