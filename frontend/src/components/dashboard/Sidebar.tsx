"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    Trophy,
    Target,
    Newspaper,
    Calendar,
    FastForward,
    ChevronRight,
    Settings,
    LogOut,
    Dribbble as Basketball
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';

const navItems = [
    { name: 'Standings', icon: Trophy, href: '/' },
    { name: 'Strategy Room', icon: Target, href: '/strategy' },
    { name: 'Player News', icon: Newspaper, href: '/news' },
    { name: 'Current Week', icon: Calendar, href: '/current-week' },
    { name: 'Upcoming Week', icon: FastForward, href: '/upcoming-week' },
];

export function Sidebar() {
    const pathname = usePathname();
    const router = useRouter();

    const handleLogout = async () => {
        await supabase.auth.signOut();
        router.push('/login');
        router.refresh();
    };

    return (
        <div className="w-64 h-full glass border-r border-border/50 flex flex-col">
            <div className="p-6">
                <div className="flex items-center gap-3 mb-8">
                    <div className="bg-orange-500/20 p-2 rounded-xl border border-orange-500/30">
                        <Basketball className="w-6 text-orange-500" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight">NBA <span className="text-orange-500 text-gradient-orange">Fantasy</span></h1>
                </div>

                <nav className="space-y-1">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-200 group",
                                    isActive
                                        ? "bg-primary/10 text-primary border border-primary/20"
                                        : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                                )}
                            >
                                <div className="flex items-center gap-3">
                                    <item.icon className={cn("w-5 transition-transform group-hover:scale-110", isActive && "text-primary")} />
                                    <span className="font-medium">{item.name}</span>
                                </div>
                                {isActive && <ChevronRight className="w-4 h-4" />}
                            </Link>
                        );
                    })}
                </nav>
            </div>

            <div className="mt-auto p-6 border-t border-border/50 space-y-4">
                <div className="glass-card p-4 rounded-2xl">
                    <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider font-semibold">League Status</p>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-sm font-medium">Live Connection</span>
                    </div>
                </div>

                <button className="flex items-center gap-3 px-4 py-2 w-full text-muted-foreground hover:text-foreground transition-colors group">
                    <Settings className="w-5 group-hover:rotate-45 transition-transform" />
                    <span className="text-sm font-medium">Settings</span>
                </button>

                <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-4 py-2 w-full text-red-500/70 hover:text-red-500 transition-colors group"
                >
                    <LogOut className="w-5" />
                    <span className="text-sm font-medium">Logout</span>
                </button>
            </div>
        </div>
    );
}
