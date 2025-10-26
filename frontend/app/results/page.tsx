"use client";
import { useMatches } from "../../context/MatchesContext";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip);

export default function Results() {
  const { matches } = useMatches();
  const [topMatches, setTopMatches] = useState<any[]>([]);

  useEffect(() => {
    setTopMatches(matches.slice(0, 3)); // top 3 cards
  }, [matches]);

  const labels = matches.map(r => r.name);
  const chartData = {
    labels,
    datasets: [
      {
        label: "Admission Probability (%)",
        data: matches.map(r => r.probability),
        backgroundColor: "rgba(99, 102, 241, 0.7)",
        borderRadius: 6
      }
    ]
  };

  return (
    <div className="bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 min-h-screen text-white p-6">
      <h2 className="text-4xl font-extrabold mb-8 text-center text-indigo-400 animate-pulse">
        🚀 Your Top University Matches
      </h2>

      {/* Top 3 Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-12">
        {topMatches.map((m, i) => (
          <div
            key={i}
            className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-3xl shadow-xl transform transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:rotate-1"
          >
            <h3 className="text-2xl font-bold mb-2">{m.name}</h3>
            <p className="text-indigo-200 mb-2">
              Admission Chance: <span className="text-white font-semibold">{m.probability}%</span>
            </p>
            <div className="space-y-1 text-indigo-100">
              <p>Avg GPA: {m.avg_gpa}</p>
              <p>Avg GMAT: {m.avg_gmat}</p>
              <p>Acceptance Rate: {m.acceptance_rate}%</p>
              <p>Program: {m.program_type}</p>
            </div>
            <div className="mt-4 h-2 w-full bg-indigo-300 rounded-full overflow-hidden">
              <div
                className="h-2 bg-white rounded-full transition-all duration-1000"
                style={{ width: `${m.probability}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="bg-gray-800 p-6 rounded-3xl shadow-2xl mb-12">
        <Bar
          data={chartData}
          options={{
            responsive: true,
            plugins: { legend: { labels: { color: "white" } } },
            scales: {
              x: { ticks: { color: "white" } },
              y: { ticks: { color: "white" } }
            }
          }}
        />
      </div>

      {/* Table */}
      <div className="bg-gray-900 p-6 rounded-3xl shadow-2xl overflow-x-auto">
        <table className="w-full table-auto text-white border-separate border-spacing-0">
          <thead>
            <tr className="bg-gray-800 border-b border-indigo-500">
              <th className="p-4 text-left uppercase tracking-wider text-indigo-300">University</th>
              <th className="p-4 text-left uppercase tracking-wider text-indigo-300">Probability (%)</th>
              <th className="p-4 text-left uppercase tracking-wider text-indigo-300">Program</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((r, i) => (
              <tr
                key={i}
                className="border-b border-gray-700 hover:bg-indigo-800 hover:scale-105 transform transition duration-300 cursor-pointer"
              >
                <td className="p-4">{r.name}</td>
                <td className="p-4">{r.probability}%</td>
                <td className="p-4">{r.program_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
