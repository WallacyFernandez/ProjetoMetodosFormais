import { UserDataProps } from "@/types/GlobalTypes";
import { createContext } from "react";

interface DataUserProps {
    user: UserDataProps | null,
    setUser: React.Dispatch<React.SetStateAction<UserDataProps | null>>
}

const defaultValues: DataUserProps = {
    user: null,
    setUser: () => {}
};

export const UserDataContext = createContext<DataUserProps>(defaultValues)