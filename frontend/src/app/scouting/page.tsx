"use client";

import React, { useEffect, useState } from 'react';
import { fetchPlayerRankings } from '@/lib/api';
import {
    Loader2,
    TrendingUp,
    TrendingDown,
    ArrowUpDown,
    Info
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

type PlayerStats = {
    PLAYER_ID: number;
    PLAYER_NAME: string;
    TEAM_ABBREVIATION: string;
    MIN: number;
    PTS: number;
    REB: number;
    AST: number;
    STL: number;
    BLK: number;
    FG3M: number;
    FG_PCT: number;
    FT_PCT: number;
    TOV: number;
    TOTAL_Z: number;
    RANK: number;
    [key: string]: any; // For dynamic Z-score access
};

export default function ScoutingPage() {
    const [players, setPlayers] = useState<PlayerStats[]>([]);
    const [loading, setLoading] = useState(true);
    const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>({ key: 'TOTAL_Z', direction: 'desc' });

    useEffect(() => {
        const loadData = async () => {
            // In demo mode or if backend fails, use placeholder
            try {
                const data = await fetchPlayerRankings();
                setPlayers(data);
            } catch (error) {
                console.error("Failed to load rankings:", error);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);

    const handleSort = (key: string) => {
        let direction: 'asc' | 'desc' = 'desc';
        if (sortConfig && sortConfig.key === key && sortConfig.direction === 'desc') {
            direction = 'asc';
        }
        setSortConfig({ key, direction });
    };

    const sortedPlayers = React.useMemo(() => {
        let sortableItems = [...players];
        if (sortConfig !== null) {
            sortableItems.sort((a, b) => {
                if (a[sortConfig.key] < b[sortConfig.key]) {
                    return sortConfig.direction === 'asc' ? -1 : 1;
                }
                if (a[sortConfig.key] > b[sortConfig.key]) {
                    return sortConfig.direction === 'asc' ? 1 : -1;
                }
                return 0;
            });
        }
        return sortableItems;
    }, [players, sortConfig]);

    const getZScoreColor = (value: number) => {
        if (value >= 2.0) return "text-green-400 font-bold";
        if (value >= 1.0) return "text-green-300";
        if (value > 0) return "text-green-100";
        if (value > -1.0) return "text-white/60";
        if (value > -2.0) return "text-red-300";
        return "text-red-400 font-bold";
    };

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center">
                <Loader2 className="w-10 h-10 animate-spin text-orange-500" />
            </div>
        );
    }

    const [expandedPlayerId, setExpandedPlayerId] = useState<number | null>(null);
    const [consistencyData, setConsistencyData] = useState<Record<number, any>>({});
    const [loadingConsistency, setLoadingConsistency] = useState(false);

    // ... (existing useEffect)

    const handleRowClick = async (playerId: number) => {
        if (expandedPlayerId === playerId) {
            setExpandedPlayerId(null);
            return;
        }

        setExpandedPlayerId(playerId);

        if (!consistencyData[playerId]) {
            setLoadingConsistency(true);
            try {
                // Determine API path dynamically - in real app import from api
                // helping consistency with local dev vs prod
                const { fetchPlayerConsistency } = await import('@/lib/api');
                const data = await fetchPlayerConsistency(playerId);
                setConsistencyData(prev => ({ ...prev, [playerId]: data }));
            } catch (error) {
                console.error("Failed to fetch consistency:", error);
            } finally {
                setLoadingConsistency(false);
            }
        }
    };

    return (
        <div className="p-6 md:p-8 max-w-[1600px] mx-auto space-y-8 animate-fade-in relative">
            {/* Header */}
            <div className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold tracking-tight">Scouting <span className="text-gradient-orange">Dashboard</span></h1>
                <p className="text-muted-foreground flex items-center gap-2">
                    <Info className="w-4 h-4" />
                    Click on a player to see their <span className="text-orange-400 font-semibold">Consistency Grade</span> & Volatility Analysis.
                </p>
            </div>

            {/* Main Table Card */}
            <div className="glass-card rounded-2xl overflow-hidden border border-white/5 shadow-2xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-white/5 text-xs uppercase font-semibold text-muted-foreground">
                            <tr>
                                <th className="px-4 py-4 w-12 text-center">Rk</th>
                                <th className="px-4 py-4 min-w-[180px]">Player</th>
                                <th
                                    className="px-4 py-4 cursor-pointer hover:text-white transition-colors text-right"
                                    onClick={() => handleSort('TOTAL_Z')}
                                >
                                    Value (Z) <ArrowUpDown className="w-3 h-3 inline ml-1" />
                                </th>
                                {['PTS', 'REB', 'AST', 'FG3M', 'STL', 'BLK', 'FG_PCT', 'FT_PCT', 'TOV'].map((cat) => (
                                    <th
                                        key={cat}
                                        className="px-3 py-4 text-right cursor-pointer hover:text-white transition-colors"
                                        onClick={() => handleSort(cat)}
                                    >
                                        {cat}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {sortedPlayers.map((player) => (
                                <React.Fragment key={player.PLAYER_ID}>
                                    <motion.tr
                                        layout
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        onClick={() => handleRowClick(player.PLAYER_ID)}
                                        className={cn(
                                            "cursor-pointer transition-colors group",
                                            expandedPlayerId === player.PLAYER_ID ? "bg-white/10" : "hover:bg-white/5"
                                        )}
                                    >
                                        <td className="px-4 py-3 text-center text-muted-foreground font-mono">{player.RANK}</td>
                                        <td className="px-4 py-3 font-medium text-white">
                                            <div className="flex flex-col">
                                                <span>{player.PLAYER_NAME}</span>
                                                <span className="text-xs text-muted-foreground">{player.TEAM_ABBREVIATION} • {player.MIN.toFixed(1)} MPG</span>
                                            </div>
                                        </td>
                                        <td className="px-4 py-3 text-right bg-white/5 font-mono text-base">
                                            <span className={getZScoreColor(player.TOTAL_Z)}>
                                                {player.TOTAL_Z.toFixed(2)}
                                            </span>
                                        </td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.PTS.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.REB.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.AST.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.FG3M.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.STL.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.BLK.toFixed(1)}</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{(player.FG_PCT * 100).toFixed(1)}%</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{(player.FT_PCT * 100).toFixed(1)}%</td>
                                        <td className="px-3 py-3 text-right tabular-nums text-white/80">{player.TOV.toFixed(1)}</td>
                                    </motion.tr>

                                    {/* Expanded Content */}
                                    {expandedPlayerId === player.PLAYER_ID && (
                                        <tr className="bg-black/20">
                                            <td colSpan={13} className="p-0">
                                                <motion.div
                                                    initial={{ height: 0, opacity: 0 }}
                                                    animate={{ height: "auto", opacity: 1 }}
                                                    className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6 border-b border-orange-500/20"
                                                >
                                                    {loadingConsistency && !consistencyData[player.PLAYER_ID] ? (
                                                        <div className="col-span-3 flex justify-center py-8">
                                                            <Loader2 className="w-6 h-6 animate-spin text-orange-500" />
                                                        </div>
                                                    ) : consistencyData[player.PLAYER_ID] ? (
                                                        <>
                                                            <div className="bg-background/50 p-4 rounded-xl border border-white/10 flex flex-col items-center justify-center text-center">
                                                                <span className="text-muted-foreground text-xs uppercase tracking-wider mb-2">Consistency Grade</span>
                                                                <span className={cn(
                                                                    "text-5xl font-black",
                                                                    consistencyData[player.PLAYER_ID].consistency_grade.startsWith("A") ? "text-green-400" :
                                                                        consistencyData[player.PLAYER_ID].consistency_grade === "B" ? "text-blue-400" :
                                                                            consistencyData[player.PLAYER_ID].consistency_grade === "C" ? "text-yellow-400" : "text-red-400"
                                                                )}>
                                                                    {consistencyData[player.PLAYER_ID].consistency_grade}
                                                                </span>
                                                                <span className="text-xs text-muted-foreground mt-2">Based on Last 20 Games</span>
                                                            </div>

                                                            <div className="col-span-2 grid grid-cols-3 gap-4">
                                                                {Object.entries(consistencyData[player.PLAYER_ID].volatility_stats).map(([key, val]: [string, any]) => (
                                                                    <div key={key} className="bg-background/30 p-3 rounded-lg border border-white/5">
                                                                        <div className="text-[10px] text-muted-foreground uppercase">{key.replace('_STD', '')} Volatility</div>
                                                                        <div className="text-lg font-mono font-medium text-white">{val} <span className="text-xs text-muted-foreground">σ</span></div>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </>
                                                    ) : (
                                                        <div className="col-span-3 text-center text-muted-foreground py-4">
                                                            No consistency data available
                                                        </div>
                                                    )}
                                                </motion.div>
                                            </td>
                                        </tr>
                                    )}
                                </React.Fragment>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
