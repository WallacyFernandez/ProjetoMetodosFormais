import { createContext } from "react"

interface IsSidebarProps {
  isCollapsed: boolean
  setIsCollapsed: React.Dispatch<React.SetStateAction<boolean>>
}

const defaultValues: IsSidebarProps = {
  isCollapsed: false,
  setIsCollapsed: () => {}
}

export const IsSidebarOnContext = createContext<IsSidebarProps>(defaultValues)
