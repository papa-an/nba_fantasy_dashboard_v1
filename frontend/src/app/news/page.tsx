"use client";

import React, { useEffect, useState } from 'react';
import { Newspaper, RefreshCw, User, ExternalLink } from 'lucide-react';
import { fetchNews } from '@/lib/api';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export default function NewsPage() {
    const [news, setNews] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const loadNews = async () => {
        setLoading(true);
        try {
            const newsData = await fetchNews();
            setNews(newsData);
        } catch (error) {
            console.error("Failed to load news:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadNews();
    }, []);

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
                        <Newspaper className="text-primary w-8 h-8" /> Latest Player News
                    </h1>
                    <p className="text-muted-foreground">Scraped from NBC Sports (Rotoworld)</p>
                </div>

                <button
                    onClick={loadNews}
                    disabled={loading}
                    className="flex items-center gap-2 bg-white/5 hover:bg-white/10 px-4 py-2 rounded-xl border border-white/10 transition-all active:scale-95 disabled:opacity-50"
                >
                    <RefreshCw className={cn("w-4 h-4", loading && "animate-spin")} />
                    <span className="font-medium">Refresh</span>
                </button>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {loading ? (
                    Array.from({ length: 6 }).map((_, i) => (
                        <div key={i} className="glass-card h-48 rounded-3xl animate-pulse" />
                    ))
                ) : news.length > 0 ? (
                    news.map((item, idx) => (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: idx * 0.05 }}
                            key={idx}
                            className="glass rounded-3xl p-6 hover:border-primary/30 transition-all group flex flex-col h-full"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary/10 to-secondary flex items-center justify-center border border-white/5">
                                        <User className="w-6 text-primary" />
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-lg group-hover:text-primary transition-colors leading-tight">
                                            {item.player}
                                        </h3>
                                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wider">{item.team}</p>
                                    </div>
                                </div>
                                <span className="text-[10px] bg-white/5 px-2 py-1 rounded-lg text-muted-foreground font-semibold">
                                    {item.date}
                                </span>
                            </div>

                            <div className="space-y-3 flex-grow">
                                <p className="font-semibold text-foreground/90">{item.headline}</p>
                                <div className="p-4 bg-black/20 rounded-2xl border border-white/5 italic text-sm text-muted-foreground leading-relaxed">
                                    {item.report}
                                </div>
                            </div>

                            <div className="mt-6 flex items-center justify-between border-t border-white/5 pt-4">
                                <div className="flex items-center gap-2">
                                    <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_rgba(239,68,68,0.5)]" />
                                    <span className="text-xs font-bold text-primary uppercase tracking-tighter">Verified Meta</span>
                                </div>
                                <a href="#" className="flex items-center gap-1 text-xs text-muted-foreground hover:text-primary transition-colors">
                                    Source <ExternalLink className="w-3 h-3" />
                                </a>
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center glass rounded-3xl">
                        <p className="text-muted-foreground">No player news found at the moment.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
