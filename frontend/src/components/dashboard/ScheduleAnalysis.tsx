"use client";

import React from 'react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { ChevronRight, ArrowRight, Info } from 'lucide-react';

interface MatchupProps {
    data: any;
    days: string[];
}

export function ScheduleAnalysis({ data, days }: MatchupProps) {
    if (!data) return null;

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {data.matchups.map((matchup: any, idx: number) => (
                <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: idx * 0.05 }}
                    key={idx}
                    className={cn(
                        "glass rounded-3xl overflow-hidden flex flex-col border transition-all",
                        matchup.is_my_matchup ? "border-primary/50 shadow-[0_0_20px_rgba(239,68,68,0.1)]" : "border-white/5"
                    )}
                >
                    {/* Header */}
                    <div className="bg-white/5 px-5 py-4 flex items-center justify-between border-b border-white/5">
                        <div className="flex-1 text-center font-bold text-[13px] truncate pr-2">{matchup.home_team.name}</div>
                        <div className="text-[10px] font-bold text-muted-foreground uppercase px-2 py-0.5 bg-black/40 rounded italic">VS</div>
                        <div className="flex-1 text-center font-bold text-[13px] truncate pl-2">{matchup.away_team.name}</div>
                    </div>

                    <div className="p-5 flex-grow space-y-4">
                        {/* Total Games Comparison */}
                        <div className="space-y-2">
                            <TeamRow name={matchup.home_team.name} total={matchup.home_team.total_games} />
                            <TeamRow name={matchup.away_team.name} total={matchup.away_team.total_games} />
                        </div>

                        {/* Advantage Banner */}
                        <div className={cn(
                            "py-2.5 rounded-2xl text-center text-xs font-bold border",
                            matchup.diff === 0 ? "bg-blue-500/10 text-blue-400 border-blue-500/20" :
                                matchup.diff > 0 ? "bg-green-500/10 text-green-400 border-green-500/20" :
                                    "bg-red-500/10 text-red-400 border-red-500/20"
                        )}>
                            {matchup.diff === 0 ? "⚖️ Matchup Even" : `🎯 ${matchup.advantage_message} Advantage`}
                        </div>

                        {/* Daily Breakdown */}
                        <div className="pt-2">
                            <div className="flex items-center gap-2 mb-2 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                                <span>Daily Breakdown</span>
                                <div className="h-px bg-white/5 flex-1" />
                            </div>

                            <div className="overflow-x-auto pb-2 scrollbar-hide">
                                <table className="w-full text-center">
                                    <thead>
                                        <tr>
                                            <th className="w-16"></th>
                                            {days.map((day, dIdx) => (
                                                <th key={dIdx} className="text-[9px] font-bold text-muted-foreground py-1 px-1">{day}</th>
                                            ))}
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td className="text-[9px] font-bold text-muted-foreground text-left truncate max-w-[60px]">{matchup.home_team.name.substring(0, 6)}..</td>
                                            {matchup.home_team.daily_counts.map((count: number, cIdx: number) => (
                                                <td key={cIdx} className="p-1">
                                                    <div className={cn(
                                                        "w-5 h-5 flex items-center justify-center rounded-md text-[9px] font-bold",
                                                        count > 0 ? "bg-primary/20 text-primary border border-primary/20" : "bg-white/5 text-muted-foreground"
                                                    )}>{count}</div>
                                                </td>
                                            ))}
                                        </tr>
                                        <tr>
                                            <td className="text-[9px] font-bold text-muted-foreground text-left truncate max-w-[60px]">{matchup.away_team.name.substring(0, 6)}..</td>
                                            {matchup.away_team.daily_counts.map((count: number, cIdx: number) => (
                                                <td key={cIdx} className="p-1">
                                                    <div className={cn(
                                                        "w-5 h-5 flex items-center justify-center rounded-md text-[9px] font-bold",
                                                        count > 0 ? "bg-primary/20 text-primary border border-primary/20" : "bg-white/5 text-muted-foreground"
                                                    )}>{count}</div>
                                                </td>
                                            ))}
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </motion.div>
            ))}
        </div>
    );
}

function TeamRow({ name, total }: { name: string, total: number }) {
    return (
        <div className="flex items-center justify-between p-2 rounded-xl bg-white/5 border border-white/5 group hover:bg-white/[0.08] transition-colors">
            <span className="text-[11px] font-medium text-muted-foreground truncate max-w-[140px]">{name}</span>
            <div className="flex items-center gap-2">
                <div className="w-8 h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: `${Math.min(100, (total / 50) * 100)}%` }} />
                </div>
                <span className="text-lg font-bold text-primary tabular-nums">{total}</span>
            </div>
        </div>
    );
}
