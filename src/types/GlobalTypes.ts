export interface ButtonsConfig {
  titleBtn: string,
  type: 'primary' | 'secondary',
  action: () => () => void
};

export interface Project {
  id: string;
  title: string;
  description: string;
  endDate: Date;
  status: 'Finalizado' | 'Em-progresso' | 'Pendente';
  submission: 'Enviado' | 'Carregar';
};

export interface UserDataProps {
  id: number,
  username: string,
  name: string,
  email: string,
  groups: string[]
};