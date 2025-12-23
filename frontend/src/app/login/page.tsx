"use client";

import React, { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { Dribbble as Basketball, Loader2, AlertCircle, RefreshCw } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(false);
    }, []);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        if (loading) return;

        setLoading(true);
        setError(null);

        try {
            console.log("Attempting login...");
            const { data, error: loginError } = await supabase.auth.signInWithPassword({
                email,
                password,
            });

            if (loginError) {
                setError(loginError.message);
                setLoading(false);
                return;
            }

            if (data?.user) {
                console.log("Login success! Redirecting...");
                // Standard location change is most reliable for setting cookies 
                window.location.href = '/';
            }
        } catch (err: any) {
            setError("Connection failure. Please refresh.");
            setLoading(false);
        }
    };

    const handleReset = async () => {
        // Clear all local storage and cookies to fix stuck sessions
        localStorage.clear();
        sessionStorage.clear();
        await supabase.auth.signOut();
        window.location.reload();
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#09090b] px-4">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="max-w-md w-full glass rounded-[2.5rem] p-10 shadow-2xl border border-white/5 bg-white/[0.02] backdrop-blur-2xl"
            >
                <div className="flex flex-col items-center mb-10">
                    <div className="bg-orange-500/20 p-5 rounded-3xl mb-6 border border-orange-500/30 shadow-[0_0_30px_rgba(249,115,22,0.2)]">
                        <Basketball className="w-10 h-10 text-orange-500" />
                    </div>
                    <h1 className="text-3xl font-black text-white text-center">
                        NBA <span className="text-orange-500">Dashboard</span>
                    </h1>
                </div>

                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-[10px] font-bold uppercase tracking-widest text-white/30 ml-2">Email Address</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:ring-2 focus:ring-orange-500/40 transition-all text-white font-medium"
                            placeholder="manager@espn.com"
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-[10px] font-bold uppercase tracking-widest text-white/30 ml-2">Secret Key</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:ring-2 focus:ring-orange-500/40 transition-all text-white font-medium"
                            placeholder="••••••••"
                        />
                    </div>

                    <AnimatePresence>
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="flex items-center gap-3 p-4 bg-orange-500/10 border border-orange-500/20 rounded-2xl text-orange-500 text-xs font-bold"
                            >
                                <AlertCircle className="w-4 h-4 shrink-0" />
                                <p>{error}</p>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-orange-500 h-16 rounded-2xl font-black text-white hover:bg-orange-600 transition-all shadow-[0_10px_20px_rgba(249,115,22,0.2)] active:scale-[0.98] disabled:opacity-50"
                    >
                        {loading ? <Loader2 className="w-6 h-6 animate-spin mx-auto" /> : 'Enter Arena'}
                    </button>

                    <button
                        type="button"
                        onClick={handleReset}
                        className="w-full text-[10px] font-bold text-white/20 hover:text-white/60 transition-colors uppercase tracking-[0.2em] flex items-center justify-center gap-2 mt-4"
                    >
                        <RefreshCw className="w-3 h-3" />
                        Reset Connection Session
                    </button>
                </form>
            </motion.div>
        </div>
    );
}
