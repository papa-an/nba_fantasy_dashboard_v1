"use client";

import React, { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import { Dribbble as Basketball, Save, Shield, Info, AlertCircle, CheckCircle, X, Copy } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SettingsPage() {
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [showHelp, setShowHelp] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);
    const [formData, setFormData] = useState({
        league_id: '',
        swid: '',
        espn_s2: '',
        season: 2026
    });
    const router = useRouter();

    useEffect(() => {
        async function loadSettings() {
            setLoading(true);
            const { data: { user } } = await supabase.auth.getUser();
            if (!user) {
                router.push('/login');
                return;
            }

            const { data, error } = await supabase
                .from('league_settings')
                .select('*')
                .single();

            if (data) {
                setFormData({
                    league_id: data.league_id || '',
                    swid: data.swid || '',
                    espn_s2: data.espn_s2 || '',
                    season: data.season || 2026
                });
            }
            setLoading(false);
        }
        loadSettings();
    }, [router]);

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setMessage(null);

        const { data: { user } } = await supabase.auth.getUser();
        if (!user) return;

        const { error } = await supabase
            .from('league_settings')
            .upsert({
                id: user.id,
                email: user.email,
                league_id: formData.league_id,
                swid: formData.swid,
                espn_s2: formData.espn_s2,
                season: formData.season
            });

        if (error) {
            setMessage({ type: 'error', text: 'Failed to save settings: ' + error.message });
        } else {
            setMessage({ type: 'success', text: 'Account connected successfully! Dashboard is now live.' });
            setTimeout(() => router.push('/'), 2000);
        }
        setSaving(false);
    };

    if (loading) return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
    );

    return (
        <div className="max-w-2xl mx-auto py-10 space-y-8 h-full flex flex-col justify-center relative">
            {/* Help Modal */}
            <AnimatePresence>
                {showHelp && (
                    <motion.div
                        initial={{ opacity: 0, backdropFilter: "blur(0px)" }}
                        animate={{ opacity: 1, backdropFilter: "blur(8px)" }}
                        exit={{ opacity: 0, backdropFilter: "blur(0px)" }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40"
                        onClick={() => setShowHelp(false)}
                    >
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.95, opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                            className="bg-[#09090b] border border-white/10 rounded-3xl p-8 max-w-lg w-full shadow-2xl relative overflow-hidden"
                        >
                            <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-transparent via-orange-500 to-transparent opacity-50" />
                            <button
                                onClick={() => setShowHelp(false)}
                                className="absolute top-4 right-4 text-white/40 hover:text-white transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>

                            <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                                <Info className="text-orange-500" />
                                How to find Credentials
                            </h3>

                            <div className="space-y-6 overflow-y-auto max-h-[60vh] pr-2 scrollbar-thin scrollbar-thumb-orange-500/20">
                                <div className="space-y-2">
                                    <h4 className="font-semibold text-orange-400 text-sm uppercase tracking-wider">1. League ID</h4>
                                    <p className="text-sm text-gray-400">
                                        Go to your ESPN League home page. Look at the URL bar:
                                        <br />
                                        <code className="bg-white/5 px-2 py-1 rounded text-xs mt-1 block">
                                            fantasy.espn.com/.../league?leagueId=<span className="text-orange-500 font-bold">12345678</span>
                                        </code>
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <h4 className="font-semibold text-orange-400 text-sm uppercase tracking-wider">2. SWID & ESPN_S2 DO NOT SHARE!</h4>
                                    <p className="text-sm text-gray-400">
                                        These are secret cookies that grant access to your private league.
                                    </p>
                                    <ul className="list-disc list-inside text-sm text-gray-400 space-y-2 ml-1">
                                        <li>Open your League Page in <b>Chrome/Edge</b>.</li>
                                        <li>Press <kbd className="bg-white/10 px-1 rounded">F12</kbd> to open Developer Tools.</li>
                                        <li>Click the <b>Application</b> tab (top menu).</li>
                                        <li>Expand <b>Cookies</b> in the left sidebar.</li>
                                        <li>Click on <span className="text-white">fantasy.espn.com</span>.</li>
                                        <li>Find <b>SWID</b> and <b>espn_s2</b> in the list.</li>
                                    </ul>
                                </div>

                                <div className="bg-orange-500/10 p-4 rounded-xl border border-orange-500/20">
                                    <p className="text-xs text-orange-200">
                                        <b>Tip:</b> Copy the values exactly as they appear. SWID includes the curly braces <code>{`{...}`}</code>.
                                    </p>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className="space-y-2">
                <h1 className="text-3xl font-black flex items-center gap-3">
                    <Basketball className="text-orange-500 w-8 h-8" />
                    Connect Your <span className="text-orange-500 text-gradient-orange">League</span>
                </h1>
                <p className="text-muted-foreground">Linked to: <span className="text-foreground font-medium underline underline-offset-4">your account</span></p>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-3xl p-8 border border-white/5 relative overflow-hidden"
            >
                <div className="absolute top-0 right-0 p-8 opacity-5">
                    <Shield className="w-32 h-32" />
                </div>

                <form onSubmit={handleSave} className="space-y-6 relative z-10">
                    <div className="grid grid-cols-1 gap-6">
                        <div className="space-y-2">
                            <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground ml-1">League ID</label>
                            <input
                                type="text"
                                value={formData.league_id}
                                onChange={(e) => setFormData({ ...formData, league_id: e.target.value })}
                                placeholder="e.g. 1573125237"
                                required
                                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:ring-2 focus:ring-orange-500/50 transition-all font-mono text-sm"
                            />
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground ml-1">SWID Token</label>
                                <button
                                    type="button"
                                    onClick={() => setShowHelp(true)}
                                    className="flex items-center gap-1 text-[10px] text-orange-500/70 hover:text-orange-500 cursor-help transition-colors"
                                >
                                    <Info className="w-3" /> How to find?
                                </button>
                            </div>
                            <input
                                type="text"
                                value={formData.swid}
                                onChange={(e) => setFormData({ ...formData, swid: e.target.value })}
                                placeholder="{8A84D699-...}"
                                required
                                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:ring-2 focus:ring-orange-500/50 transition-all font-mono text-sm"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground ml-1">ESPN S2 Key</label>
                            <textarea
                                rows={3}
                                value={formData.espn_s2}
                                onChange={(e) => setFormData({ ...formData, espn_s2: e.target.value })}
                                placeholder="AEBTXHDY..."
                                required
                                className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 outline-none focus:ring-2 focus:ring-orange-500/50 transition-all font-mono text-sm resize-none"
                            />
                        </div>
                    </div>

                    {message && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className={`flex items-center gap-3 p-4 rounded-2xl text-sm font-medium border ${message.type === 'success'
                                ? 'bg-green-500/10 border-green-500/20 text-green-500'
                                : 'bg-red-500/10 border-red-500/20 text-red-500'
                                }`}
                        >
                            {message.type === 'success' ? <CheckCircle className="w-5 h-5 shrink-0" /> : <AlertCircle className="w-5 h-5 shrink-0" />}
                            {message.text}
                        </motion.div>
                    )}

                    <button
                        type="submit"
                        disabled={saving}
                        className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-5 rounded-2xl transition-all shadow-[0_8px_30px_rgb(249,115,22,0.3)] flex items-center justify-center gap-2 active:scale-[0.98] disabled:opacity-50"
                    >
                        {saving ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                <Save className="w-5 h-5" />
                                Save & Secure Account
                            </>
                        )}
                    </button>
                </form>
            </motion.div>

            <div className="text-center">
                <p className="text-xs text-muted-foreground max-w-sm mx-auto">
                    Your credentials are encrypted and stored in your private Supabase instance. Only you can access this data.
                </p>
            </div>
        </div>
    );
}
