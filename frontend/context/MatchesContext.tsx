"use client";
import { createContext, useContext, useState, ReactNode } from "react";

interface MatchesContextType {
  matches: any[];
  setMatches: (data: any[]) => void;
}

const MatchesContext = createContext<MatchesContextType | undefined>(undefined);

export const MatchesProvider = ({ children }: { children: ReactNode }) => {
  const [matches, setMatches] = useState<any[]>([]);
  return (
    <MatchesContext.Provider value={{ matches, setMatches }}>
      {children}
    </MatchesContext.Provider>
  );
};

export const useMatches = (): MatchesContextType => {
  const context = useContext(MatchesContext);
  if (!context) throw new Error("useMatches must be used within MatchesProvider");
  return context;
};
