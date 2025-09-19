'use client';

import { ThemeProvider } from "styled-components";
import theme from "./styles/theme";
import { useEffect, useState } from "react";
import { IsSidebarOnContext } from "@/context/IsSidebarOnContext";
import { UserDataContext } from "@/context/UserDataContext";
import { Bounce, ToastContainer } from "react-toastify";
import { UserDataProps } from "@/types/GlobalTypes";
import { IsDashboardLoadedContext } from "@/context/IsDashboardLoadedContext";
import { storage } from "@/utils/Storage";
import { GetUserData } from "@/services/AuthServices";

export default function Providers({ children }: { children: React.ReactNode }) {
  const [ isCollapsed, setIsCollapsed ] = useState<boolean>(false)
  const [ user, setUser ] = useState<UserDataProps | null>(null)
  const [ isLoaded, setIsLoaded ] = useState<boolean>(false)

  useEffect(() => {
    const accessToken = storage.get('accessToken')
    if(!accessToken) return
    (async () => {
      try {
        const data = await GetUserData()
        if(data) {
          setUser({
            id: data.id,
            username: data.username,
            name: data.name ?? '',
            email: data.email ?? '',
            // compat com tipo atual do contexto
            groups: (data.groups as unknown as []) ?? []
          })
        }
      } catch (error) {
        // silencioso por enquanto; toasts já são mostrados em fluxos explícitos
      }
    })()
  }, [])


  return (
    <ThemeProvider theme={theme}>
      <IsSidebarOnContext.Provider value={{ isCollapsed, setIsCollapsed }}>
        <UserDataContext.Provider value={{ user, setUser }}>
          {/* Solução temporária */}
          <IsDashboardLoadedContext.Provider value={{ isLoaded, setIsLoaded }}>
            <ToastContainer
              position="bottom-left"
              autoClose={5000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover={false}
              theme="light"
              transition={Bounce}
              />
            {children}
          </IsDashboardLoadedContext.Provider>
        </UserDataContext.Provider>
      </IsSidebarOnContext.Provider>
    </ThemeProvider>
  );
} 