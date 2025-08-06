import { createContext, useState, useContext, ReactNode } from "react";

type MenuKey = "Categories" | "Shops" | "Location" | "Prices" | null;

interface MenuContextProps {
  activeMenu: MenuKey;
  setActiveMenu: (menu: MenuKey) => void;
}

const MenuContext = createContext<MenuContextProps | undefined>(undefined);

export const useMenu = () => {
  const context = useContext(MenuContext);
  if (!context) throw new Error("useMenu must be used within MenuProvider");
  return context;
};

export const MenuProvider = ({ children }: { children: ReactNode }) => {
  const [activeMenu, setActiveMenu] = useState<MenuKey>(null);

  return (
    <MenuContext.Provider value={{ activeMenu, setActiveMenu }}>
      {children}
    </MenuContext.Provider>
  );
};
