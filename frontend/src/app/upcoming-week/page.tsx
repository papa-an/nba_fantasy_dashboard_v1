"use client";

import React, { useEffect, useState } from 'react';
import { FastForward, Info } from 'lucide-react';
import { fetchUpcomingSchedule, fetchTeams } from '@/lib/api';
import { ScheduleAnalysis } from '@/components/dashboard/ScheduleAnalysis';

export default function UpcomingWeekPage() {
    const [data, setData] = useState<any>(null);
    const [teams, setTeams] = useState<any[]>([]);
    const [selectedTeamId, setSelectedTeamId] = useState<number | null>(null);
    const [loading, setLoading] = useState(true);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
        async function init() {
            try {
                const teamsData = await fetchTeams();
                setTeams(teamsData);
                if (teamsData.length > 0) {
                    setSelectedTeamId(teamsData[0].id);
                }
            } catch (e) { console.error(e); }
        }
        init();
    }, []);

    useEffect(() => {
        async function load() {
            setLoading(true);
            try {
                const scheduleData = await fetchUpcomingSchedule(selectedTeamId || undefined);
                setData(scheduleData);
            } catch (error) {
                console.error("Failed to load schedule:", error);
            } finally {
                setLoading(false);
            }
        }
        load();
    }, [selectedTeamId]);

    const dateSub = mounted && data ? `${new Date(data.start_date).toLocaleDateString()} - ${new Date(data.end_date).toLocaleDateString()}` : marqueeDate(data);

    function marqueeDate(data: any) {
        if (!data) return 'Loading...';
        return `Matchup ${data.period}`;
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
                        <FastForward className="text-primary w-8 h-8" /> Upcoming Week Analysis
                    </h1>
                    <p className="text-muted-foreground">
                        {data ? `Matchup ${data.period} • ${dateSub}` : 'Loading...'}
                    </p>
                </div>

                <div className="flex items-center gap-3 bg-white/5 p-1.5 rounded-2xl border border-white/10">
                    <span className="text-xs font-semibold uppercase text-muted-foreground ml-3 hidden md:block">Highlight:</span>
                    <select
                        value={selectedTeamId || ''}
                        onChange={(e) => setSelectedTeamId(Number(e.target.value))}
                        className="bg-secondary text-foreground px-4 py-2 rounded-xl border-none focus:ring-2 focus:ring-primary/50 text-sm font-medium outline-none cursor-pointer"
                    >
                        <option value="">None</option>
                        {teams.map(team => (
                            <option key={team.id} value={team.id}>{team.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/20 rounded-2xl p-4 flex gap-3 text-sm text-blue-400">
                <Info className="w-5 h-5 flex-shrink-0" />
                <p>Plan ahead. Look for 4-game players on the waiver wire now to secure next week's advantage.</p>
            </div>

            {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {Array.from({ length: 9 }).map((_, i) => (
                        <div key={i} className="glass h-64 rounded-3xl animate-pulse" />
                    ))}
                </div>
            ) : (
                <ScheduleAnalysis data={data} days={data?.days || []} />
            )}
        </div>
    );
}
