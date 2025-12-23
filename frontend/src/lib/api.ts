import axios from 'axios';
import { supabase } from './supabase';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_BASE_URL,
});

// Add a request interceptor to include the Supabase JWT
api.interceptors.request.use(async (config) => {
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
        config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// --- Fantasy Intelligence Endpoints ---

export const fetchNews = async () => {
    const { data } = await api.get('/news');
    return data;
};

export const fetchPlayerRankings = async () => {
    const { data } = await api.get('/nba/rankings');
    return data;
};
