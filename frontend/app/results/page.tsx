"use client";
import { useMatches } from "../../context/MatchesContext";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function Results() {
  const { matches } = useMatches();
  const [topMatches, setTopMatches] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (matches && matches.length > 0) {
      // Normalize backend response structure
      const normalized = matches.map((m) => ({
        name: m.name || m.university || "Unknown University",
        probability: parseFloat(m.probability || m.admission_chance || 0),
        avg_gpa: m.avg_gpa ?? m.program_stats?.avg_gpa ?? "N/A",
        avg_gmat: m.avg_gmat ?? m.program_stats?.avg_gmat ?? "N/A",
        acceptance_rate:
          m.acceptance_rate ?? m.program_stats?.acceptance_rate ?? "N/A",
        program_type: m.program_type || "MBA",
      }));
      setTopMatches(normalized.slice(0, 3));
      setLoading(false);
    } else {
      setLoading(false);
    }
  }, [matches]);

  if (loading)
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white">
        <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-indigo-300">Analyzing your profile...</p>
      </div>
    );

  if (matches.length === 0)
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white">
        <p className="text-xl text-indigo-300">No results yet. Please submit your details to get matches.</p>
      </div>
    );

  // Chart setup
  const labels = topMatches.map((r) => r.name);
  const chartData = {
    labels,
    datasets: [
      {
        label: "Admission Probability (%)",
        data: topMatches.map((r) => r.probability),
        backgroundColor: "rgba(129, 140, 248, 0.8)",
        borderRadius: 8,
      },
    ],
  };

  return (
    <div className="bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 min-h-screen text-white p-6">
      <h2 className="text-4xl font-extrabold mb-8 text-center text-indigo-400 animate-pulse tracking-wide">
        🚀 Your Top University Matches
      </h2>

      {/* Top 3 Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 mb-16">
        {topMatches.map((m, i) => (
          <div
            key={i}
            className="bg-gradient-to-br from-indigo-600 to-purple-600 p-6 rounded-3xl shadow-lg transform transition-all duration-500 hover:scale-105 hover:shadow-2xl border border-indigo-400/40"
          >
            <h3 className="text-2xl font-bold mb-3 text-white">{m.name}</h3>
            <p className="text-indigo-200 mb-3">
              Admission Chance:{" "}
              <span className="text-white font-semibold">{m.probability}%</span>
            </p>

            <div className="space-y-2 text-indigo-100">
              <p>Avg GPA: {m.avg_gpa}</p>
              <p>Avg GMAT: {m.avg_gmat}</p>
              <p>
                Acceptance Rate:{" "}
                {m.acceptance_rate !== "N/A"
                  ? `${m.acceptance_rate}%`
                  : "N/A"}
              </p>
              <p>Program: {m.program_type}</p>
            </div>

            <div className="mt-5 h-2 w-full bg-indigo-300/30 rounded-full overflow-hidden">
              <div
                className="h-2 bg-white rounded-full transition-all duration-1000 ease-out"
                style={{ width: `${m.probability}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="bg-gray-800/60 p-6 rounded-3xl shadow-xl mb-16 backdrop-blur-md border border-indigo-400/20">
        <Bar
          data={chartData}
          options={{
            responsive: true,
            plugins: {
              legend: { labels: { color: "white" } },
            },
            scales: {
              x: { ticks: { color: "white" }, grid: { color: "#444" } },
              y: { ticks: { color: "white" }, grid: { color: "#444" } },
            },
          }}
        />
      </div>

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
    </div>
  );
}
