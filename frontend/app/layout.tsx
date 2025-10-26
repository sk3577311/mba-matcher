import { MatchesProvider } from "../context/MatchesContext";
import "./globals.css";
import Navbar from "../components/Navbar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <MatchesProvider>
          <Navbar />
          {children}
        </MatchesProvider>
      </body>
    </html>
  );
}
