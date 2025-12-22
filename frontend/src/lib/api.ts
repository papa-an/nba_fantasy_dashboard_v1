import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_BASE_URL,
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
