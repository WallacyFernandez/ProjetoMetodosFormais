export interface LoginResponse {
  access: string;
  refresh?: string;
  token?: string;
  auth_token?: string;
}

export interface UserProfile {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  name?: string;
  email?: string;
  groups: string[];
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

export interface RegisterResponse {
  tokens: LoginResponse;
  user: UserProfile;
}

