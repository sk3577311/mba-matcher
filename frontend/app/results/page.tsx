"use client";
import { useMatches } from "../../context/MatchesContext";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import Lottie from "lottie-react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// ✅ Make sure all are registered
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Results() {
  const { matches } = useMatches();
  const [topMatches, setTopMatches] = useState<any[]>([]);

  useEffect(() => {
    setTopMatches(matches.slice(0, 3));
  }, [matches]);

  const labels = matches.map((r) => r.name);
  const chartData = {
    labels,
    datasets: [
      {
        label: "Admission Probability (%)",
        data: matches.map((r) => r.probability),
        backgroundColor: "rgba(139, 92, 246, 0.8)", // purple accent
        borderRadius: 6,
      },
    ],
  };

  return (
    <div className="min-h-screen flex flex-col justify-between bg-gradient-to-b from-gray-900 via-gray-950 to-gray-900 text-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between p-4 bg-white text-black shadow-md">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12">
            <Lottie animationData={require("../../public/logo.json")} loop={true} />
          </div>
          <span className="text-xl font-bold">Orbit AI</span>
        </div>
        <a
          href="/"
          className="text-sm text-gray-300 hover:text-purple-400 transition"
        >
          ← Back to Home
        </a>
      </nav>
      {/* Main Content */}
      <main className="flex-grow flex flex-col items-center justify-center p-6 space-y-10">
        <h2 className="text-3xl md:text-4xl font-extrabold text-purple-400">
          🚀 Your Top University Matches
        </h2>

        {/* Top Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 max-w-5xl w-full">
          {topMatches.map((m, i) => (
            <div
              key={i}
              className="bg-gradient-to-r from-purple-600 to-indigo-600 p-6 rounded-3xl shadow-lg transform transition duration-300 hover:scale-105"
            >
              <h3 className="text-xl font-bold mb-2">{m.name}</h3>
              <p className="text-purple-200 mb-2">
                Admission Chance:{" "}
                <span className="text-white font-semibold">
                  {m.probability}%
                </span>
              </p>
              <div className="text-purple-100 space-y-1 text-sm">
                <p>Avg GPA: {m.avg_gpa}</p>
                <p>Avg GMAT: {m.avg_gmat}</p>
                <p>Acceptance Rate: {m.acceptance_rate}%</p>
                <p>Program: {m.program_type}</p>
              </div>
              <div className="mt-4 h-2 w-full bg-purple-300 rounded-full overflow-hidden">
                <div
                  className="h-2 bg-white rounded-full transition-all duration-1000"
                  style={{ width: `${m.probability}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        {/* Chart */}
        {matches.length > 0 && (
          <div className="bg-gray-900/80 p-6 rounded-3xl shadow-2xl w-full max-w-4xl">
            <Bar
              data={chartData}
              options={{
                responsive: true,
                plugins: { legend: { labels: { color: "white" } } },
                scales: {
                  x: { ticks: { color: "white" } },
                  y: { ticks: { color: "white" } },
                },
              }}
            />
          </div>
        )}

        {/* Table */}
        <div className="bg-gray-900/70 p-6 rounded-3xl shadow-2xl overflow-x-auto backdrop-blur-md border border-indigo-400/20">
          <table className="w-full table-auto text-white border-separate border-spacing-0">
            <thead>
              <tr className="bg-gray-800 border-b border-indigo-500">
                <th className="p-4 text-left uppercase tracking-wider text-indigo-300">
                  University
                </th>
                <th className="p-4 text-left uppercase tracking-wider text-indigo-300">
                  Probability (%)
                </th>
                <th className="p-4 text-left uppercase tracking-wider text-indigo-300">
                  Program
                </th>
              </tr>
            </thead>
            <tbody>
              {matches.map((r, i) => (
                <tr
                  key={i}
                  className="border-b border-gray-700 hover:bg-indigo-800 hover:scale-[1.02] transform transition duration-300 cursor-pointer"
                >
                  <td className="p-4">{r.name || r.university}</td>
                  <td className="p-4">
                    {parseFloat(r.probability || r.admission_chance || 0)}%
                  </td>
                  <td className="p-4">{r.program_type || "MBA"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full text-center text-sm text-gray-400 py-4 border-t border-gray-800">
        © 2025 Orbit AI. Built with ❤️ by Sameer
      </footer>
    </div>
  );
}
