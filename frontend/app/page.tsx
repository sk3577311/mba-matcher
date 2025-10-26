"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import Lottie from "lottie-react";
import { useMatches } from "../context/MatchesContext";

export default function Home() {
  const [form, setForm] = useState({ gpa: "", gmat_score: "", work_experience: "", program_type: "MBA" });
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { setMatches } = useMatches();
  const BaseUrl = "https://mba-matcher.onrender.com";

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      gpa: parseFloat(form.gpa),
      gmat_score: parseInt(form.gmat_score) || 0,
      work_experience: parseInt(form.work_experience) || 0,
      program_type: form.program_type
    };

    try {
      const res = await axios.post(`${BaseUrl}/api/match`, payload);
      setMatches(res.data.slice(0, 20)); // top 20 results
      router.push("/results");
    } catch (err: any) {
      console.error(err);
      alert("Failed to fetch matches. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between p-4 bg-gray-800 shadow-md">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12">
            <Lottie animationData={require("../public/logo.json")} loop={true} />
          </div>
          <span className="text-xl font-bold">Orbit AI</span>
        </div>
        <div className="flex gap-4">
          <a href="#form" className="hover:text-yellow-400">Match</a>
          <a href="#universities" className="hover:text-yellow-400">Universities</a>
        </div>
      </nav>

      {/* Hero + Form */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-8">
        <div className="w-full max-w-xl p-8 bg-gradient-to-tr from-indigo-800 to-purple-800 rounded-3xl shadow-2xl transform transition-all hover:scale-105 duration-500">
          <h1 className="text-4xl font-extrabold mb-8 text-center text-indigo-200 animate-pulse tracking-wide">
            🚀 Find Your Top University Matches
          </h1>

          <form id="form" onSubmit={handleSubmit} className="space-y-6">
            <input
              type="number"
              step="0.01"
              className="w-full border-none p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 bg-gray-900 text-white placeholder-indigo-300 shadow-inner transition-all duration-300"
              placeholder="GPA (0.0 - 4.0)"
              value={form.gpa}
              onChange={e => setForm({ ...form, gpa: e.target.value })}
              required
            />
            <input
              type="number"
              className="w-full border-none p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 bg-gray-900 text-white placeholder-indigo-300 shadow-inner transition-all duration-300"
              placeholder="GMAT Score (0 - 800)"
              value={form.gmat_score}
              onChange={e => setForm({ ...form, gmat_score: e.target.value })}
              required
            />
            <input
              type="number"
              className="w-full border-none p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 bg-gray-900 text-white placeholder-indigo-300 shadow-inner transition-all duration-300"
              placeholder="Work Experience (years)"
              value={form.work_experience}
              onChange={e => setForm({ ...form, work_experience: e.target.value })}
              required
            />
            <select
              className="w-full border-none p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 bg-gray-900 text-white placeholder-indigo-300 shadow-inner transition-all duration-300"
              value={form.program_type}
              onChange={e => setForm({ ...form, program_type: e.target.value })}
            >
              <option>MBA</option>
              <option>MS</option>
            </select>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 py-4 rounded-xl text-white font-bold hover:from-purple-600 hover:to-indigo-600 transition-all duration-500 animate-pulse shadow-lg hover:shadow-2xl"
            >
              {loading ? "Searching..." : "Find Matches"}
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-4 bg-gray-800 text-gray-400 text-center">
        © 2025 Orbit AI. Built with ❤️ by Sameer
      </footer>
    </div>
  );
}
