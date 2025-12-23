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

export const fetchLeagueInfo = async () => {
    const { data } = await api.get('/league/info');
    return data;
};

export const fetchStandings = async () => {
    const { data } = await api.get('/league/standings');
    return data;
};

export const fetchTeams = async () => {
    const { data } = await api.get('/league/teams');
    return data;
};

export const fetchRoster = async (teamId: number) => {
    const { data } = await api.get(`/team/${teamId}/roster`);
    return data;
};

export const fetchNews = async () => {
    const { data } = await api.get('/news');
    return data;
};

export const fetchCurrentSchedule = async (teamId?: number) => {
    const { data } = await api.get('/schedule/current', {
        params: { my_team_id: teamId }
    });
    return data;
};

export const fetchUpcomingSchedule = async (teamId?: number) => {
    const { data } = await api.get('/schedule/upcoming', {
        params: { my_team_id: teamId }
    });
    return data;
};
