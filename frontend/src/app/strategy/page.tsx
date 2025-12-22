"use client";

import React, { useEffect, useState } from 'react';
import { Target, Zap, TrendingUp, Info, Trophy } from 'lucide-react';
import { fetchTeams, fetchRoster } from '@/lib/api';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export default function StrategyPage() {
    const [teams, setTeams] = useState<any[]>([]);
    const [selectedTeamId, setSelectedTeamId] = useState<number | null>(null);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadTeams() {
            try {
                const teamsData = await fetchTeams();
                setTeams(teamsData);
                if (teamsData.length > 0) {
                    setSelectedTeamId(teamsData[0].id);
                }
            } catch (error) {
                console.error("Failed to load teams:", error);
            }
        }
        loadTeams();
    }, []);

    useEffect(() => {
        if (!selectedTeamId) return;

        async function loadRoster() {
            if (selectedTeamId === null) return;
            setLoading(true);
            try {
                const rosterData = await fetchRoster(selectedTeamId);
                setData(rosterData);
            } catch (error) {
                console.error("Failed to load roster:", error);
            } finally {
                setLoading(false);
            }
        }
        loadRoster();
    }, [selectedTeamId]);

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
                        <Target className="text-primary w-8 h-8" /> Strategy Room
                    </h1>
                    <p className="text-muted-foreground">AI-Powered Roster DNA & League Matrix</p>
                </div>

                <div className="flex items-center gap-3 bg-white/5 p-1.5 rounded-2xl border border-white/10">
                    <span className="text-xs font-semibold uppercase text-muted-foreground ml-3 hidden md:block">Analyze:</span>
                    <select
                        value={selectedTeamId || ''}
                        onChange={(e) => setSelectedTeamId(Number(e.target.value))}
                        className="bg-secondary text-foreground px-4 py-2 rounded-xl border-none focus:ring-2 focus:ring-primary/50 text-sm font-medium outline-none cursor-pointer"
                    >
                        {teams.map(team => (
                            <option key={team.id} value={team.id}>{team.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left: League Power Matrix Placeholder */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="glass rounded-3xl p-8 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                            <TrendingUp className="w-48 h-48 -mr-12 -mt-12" />
                        </div>
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-bold">League Power Matrix</h2>
                            <span className="bg-primary/20 text-primary text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-widest">Phase 2</span>
                        </div>

                        <div className="flex flex-col items-center justify-center py-24 text-center space-y-4">
                            <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-2">
                                <div className="w-8 h-8 rounded-full border-2 border-dashed border-primary/50 animate-spin-slow" />
                            </div>
                            <p className="text-lg font-semibold">9-Cat Z-Score Heatmap coming soon</p>
                            <p className="text-muted-foreground max-w-sm text-sm">We're calibrating league medians and standard deviations to provide deep category strengths analysis.</p>
                        </div>
                    </div>
                </div>

                {/* Right: Roster DNA */}
                <div className="space-y-6">
                    <div className="glass rounded-3xl p-6">
                        <h2 className="text-xl font-bold mb-6">Roster DNA</h2>
                        {loading ? (
                            <div className="py-20 flex justify-center"><div className="w-8 h-8 border-3 border-primary/20 border-t-primary rounded-full animate-spin" /></div>
                        ) : (
                            <div className="space-y-3">
                                {data?.roster.map((player: any, idx: number) => (
                                    <motion.div
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: idx * 0.03 }}
                                        key={player.name}
                                        className="flex items-center justify-between p-3 rounded-2xl bg-white/5 border border-white/5 hover:border-primary/20 transition-all group"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-[10px] font-bold text-primary">
                                                {player.position}
                                            </div>
                                            <span className="text-sm font-semibold">{player.name}</span>
                                        </div>
                                        <span className={cn(
                                            "text-[10px] font-bold px-2 py-0.5 rounded-full uppercase",
                                            player.injury_status === 'ACTIVE' ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
                                        )}>
                                            {player.injury_status === 'ACTIVE' ? 'Active' : player.injury_status}
                                        </span>
                                    </motion.div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* AI Insights Section */}
            {!loading && data?.insights && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <InsightCard
                        title="Roster Composition"
                        icon={<Zap className="text-primary w-5 h-5" />}
                        content={data.insights.composition_report}
                        color="border-primary"
                        bg="bg-primary/5"
                    />
                    <InsightCard
                        title="How to Win"
                        icon={<Trophy className="text-green-500 w-5 h-5" />}
                        content={data.insights.win_strategy}
                        color="border-green-500"
                        bg="bg-green-500/5"
                    />
                    <InsightCard
                        title="How to Improve"
                        icon={<Info className="text-blue-500 w-5 h-5" />}
                        content={data.insights.improvement_plan}
                        color="border-blue-500"
                        bg="bg-blue-500/5"
                    />
                </div>
            )}
        </div>
    );
}

function InsightCard({ title, icon, content, color, bg }: any) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className={cn("glass-card rounded-3xl p-6 border-t-4", color, bg)}
        >
            <div className="flex items-center gap-3 mb-4">
                {icon}
                <h3 className="font-bold">{title}</h3>
            </div>
            <div
                className="text-sm text-muted-foreground leading-relaxed prose prose-invert max-w-none"
                dangerouslySetInnerHTML={{ __html: content }}
            />
        </motion.div>
    );
}
