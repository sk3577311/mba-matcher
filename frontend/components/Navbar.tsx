"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full bg-gradient-to-r from-indigo-800 via-purple-800 to-indigo-800 shadow-md py-4 px-6 flex justify-between items-center sticky top-0 z-50">
      <div className="flex items-center space-x-2">
        <img src="/logo.png" alt="Orbit AI" className="w-8 h-8" />
        <span className="text-xl font-bold">Orbit AI</span>
      </div>
      <div className="space-x-4">
        <Link href="/match">Match</Link>
        <Link href="/universities">Universities</Link>
      </div>
    </nav>
  );
}
