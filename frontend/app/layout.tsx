import { MatchesProvider } from "../context/MatchesContext";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <MatchesProvider>
          {children}
        </MatchesProvider>
      </body>
    </html>
  );
}
