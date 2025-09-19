import { createContext } from "react"

interface IsDashboardLoadedProps {
  isLoaded: boolean
  setIsLoaded: React.Dispatch<React.SetStateAction<boolean>>
}

const defaultValues: IsDashboardLoadedProps = {
  isLoaded: false,
  setIsLoaded: () => {}
}

export const IsDashboardLoadedContext = createContext<IsDashboardLoadedProps>(defaultValues)
