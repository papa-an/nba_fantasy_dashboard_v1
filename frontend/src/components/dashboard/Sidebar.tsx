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

    const [isCollapsed, setIsCollapsed] = React.useState(false);

    const handleLogout = async () => {
        await supabase.auth.signOut();
        router.push('/login');
        router.refresh();
    };

    return (
        <div
            className={cn(
                "h-full glass border-r border-border/50 flex flex-col transition-all duration-300 relative",
                isCollapsed ? "w-20" : "w-64"
            )}
        >
            <button
                onClick={() => setIsCollapsed(!isCollapsed)}
                className="absolute -right-3 top-8 z-50 bg-background border border-orange-500/20 text-orange-500 p-1.5 rounded-full hover:bg-orange-500 hover:text-white transition-all shadow-lg"
            >
                {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronRight className="w-4 h-4 rotate-180" />}
            </button>

            <div className={cn("p-6", isCollapsed && "px-3")}>
                <div className={cn("flex items-center gap-3 mb-8", isCollapsed && "justify-center")}>
                    <div className="bg-orange-500/20 p-2 rounded-xl border border-orange-500/30 shrink-0">
                        <Basketball className="w-6 text-orange-500" />
                    </div>
                    {!isCollapsed && (
                        <h1 className="text-xl font-bold tracking-tight overflow-hidden whitespace-nowrap">
                            NBA <span className="text-orange-500 text-gradient-orange">Fantasy</span>
                        </h1>
                    )}
                </div>

                <nav className="space-y-1">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center px-4 py-3 rounded-xl transition-all duration-200 group",
                                    isActive
                                        ? "bg-primary/10 text-primary border border-primary/20"
                                        : "text-muted-foreground hover:text-foreground hover:bg-white/5",
                                    isCollapsed ? "justify-center px-2" : "justify-between"
                                )}
                                title={isCollapsed ? item.name : undefined}
                            >
                                <div className="flex items-center gap-3">
                                    <item.icon className={cn("w-5 shrink-0 transition-transform group-hover:scale-110", isActive && "text-primary")} />
                                    {!isCollapsed && <span className="font-medium whitespace-nowrap">{item.name}</span>}
                                </div>
                                {isActive && !isCollapsed && <ChevronRight className="w-4 h-4" />}
                            </Link>
                        );
                    })}
                </nav>
            </div>

            <div className={cn("mt-auto p-6 border-t border-border/50 space-y-4", isCollapsed && "px-3")}>
                {!isCollapsed && (
                    <div className="glass-card p-4 rounded-2xl">
                        <p className="text-xs text-muted-foreground mb-1 uppercase tracking-wider font-semibold">League Status</p>
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                            <span className="text-sm font-medium">Live Connection</span>
                        </div>
                    </div>
                )}

                <Link
                    href="/settings"
                    className={cn(
                        "flex items-center gap-3 px-4 py-2 w-full text-muted-foreground hover:text-foreground transition-colors group",
                        isCollapsed && "justify-center px-0"
                    )}
                    title="Settings"
                >
                    <Settings className="w-5 group-hover:rotate-45 transition-transform" />
                    {!isCollapsed && <span className="text-sm font-medium">Settings</span>}
                </Link>

                <button
                    onClick={handleLogout}
                    className={cn(
                        "flex items-center gap-3 px-4 py-2 w-full text-red-500/70 hover:text-red-500 transition-colors group",
                        isCollapsed && "justify-center px-0"
                    )}
                    title="Logout"
                >
                    <LogOut className="w-5" />
                    {!isCollapsed && <span className="text-sm font-medium">Logout</span>}
                </button>
            </div>
        </div>
    );
}
