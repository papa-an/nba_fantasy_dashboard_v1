"use client";

import React, { useEffect, useState } from 'react';
import { Trophy, ArrowUpRight, ArrowDownRight, Minus, AlertCircle, RefreshCw } from 'lucide-react';
import { fetchStandings, fetchLeagueInfo } from '@/lib/api';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export default function StandingsPage() {
  const [standings, setStandings] = useState<any[]>([]);
  const [leagueInfo, setLeagueInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching league data...");
      const [standingsData, infoData] = await Promise.all([
        fetchStandings(),
        fetchLeagueInfo()
      ]);
      setStandings(standingsData);
      setLeagueInfo(infoData);
    } catch (err: any) {
      console.error("Failed to load standings:", err);
      setError(err.response?.data?.detail || err.message || "Failed to connect to backend server");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-orange-500/20 border-t-orange-500 rounded-full animate-spin" />
        <p className="text-sm text-muted-foreground animate-pulse">Syncing with ESPN...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-6 max-w-md mx-auto text-center">
        <div className="bg-red-500/10 p-6 rounded-full">
          <AlertCircle className="w-12 h-12 text-red-500" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">Connection Issue</h2>
          <p className="text-muted-foreground"> {error} </p>
          <p className="text-xs text-orange-500/70">Please ensure your League ID and Credentials are correct in Settings.</p>
        </div>
        <button
          onClick={loadData}
          className="flex items-center gap-2 bg-white/5 hover:bg-white/10 px-6 py-3 rounded-2xl transition-all border border-white/10"
        >
          <RefreshCw className="w-4 h-4" />
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div>
        <h1 className="text-3xl font-bold mb-2">League Standings</h1>
        <p className="text-muted-foreground">{leagueInfo?.name} • Season {leagueInfo?.season}</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div className="glass shadow-2xl rounded-3xl overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white/5">
                <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Rank</th>
                <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Team</th>
                <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Owner</th>
                <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground text-center">W-L-T</th>
                <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground text-right mr-4">Win %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {standings.map((team, idx) => (
                <motion.tr
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  key={team.id}
                  className="hover:bg-white/[0.02] transition-colors group"
                >
                  <td className="px-6 py-5">
                    <span className={cn(
                      "w-8 h-8 flex items-center justify-center rounded-lg font-bold text-sm",
                      team.rank === 1 ? "bg-yellow-500/20 text-yellow-500" :
                        team.rank === 2 ? "bg-gray-400/20 text-gray-400" :
                          team.rank === 3 ? "bg-amber-600/20 text-amber-600" :
                            "bg-white/5 text-muted-foreground"
                    )}>
                      {team.rank}
                    </span>
                  </td>
                  <td className="px-6 py-5">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-orange-500/20 flex items-center justify-center text-lg shadow-inner">
                        🏀
                      </div>
                      <span className="font-bold group-hover:text-orange-500 transition-colors">{team.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5 text-muted-foreground text-sm">{team.owner}</td>
                  <td className="px-6 py-5 text-center">
                    <div className="flex items-center justify-center gap-2 font-mono">
                      <span className="text-green-500 font-bold">{team.wins}</span>
                      <span className="text-muted-foreground">-</span>
                      <span className="text-red-500 font-bold">{team.losses}</span>
                      <span className="text-muted-foreground">-</span>
                      <span className="text-gray-500 font-bold">{team.ties}</span>
                    </div>
                  </td>
                  <td className="px-6 py-5 text-right font-mono font-bold text-lg mr-4">
                    {team.win_pct.toFixed(3)}
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
