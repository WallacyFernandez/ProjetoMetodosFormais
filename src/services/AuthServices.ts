import { http } from "@/services/httpClient";
import { saveTokens } from "@/utils/auth";
import type { LoginResponse, UserProfile, RegisterResponse, RegisterData } from "@/types/api";

export async function Login(email: string, password: string): Promise<LoginResponse> {
  const data = await http.post<{ data: { tokens: LoginResponse } }>("/api/v1/auth/login/", { email, password }, { suppressErrorToast: true, context: "Login" });
  const tokens = data.data.tokens;
  if (tokens.access) saveTokens(tokens.access, tokens.refresh);
  return tokens;
}

export async function Register(registerData: RegisterData): Promise<RegisterResponse> {
  const data = await http.post<{ data: { tokens: LoginResponse, user: UserProfile } }>("/api/v1/auth/register/", registerData, { suppressErrorToast: true, context: "Cadastro" });
  const tokens = data.data.tokens;
  if (tokens.access) saveTokens(tokens.access, tokens.refresh);
  return data.data;
}

export async function GetUserData(): Promise<UserProfile> {
  const data = await http.get<{ data: UserProfile }>("/api/v1/auth/me/", { context: "Carregar dados do usuário" });
  return data.data;
}