import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
	baseURL: API_BASE_URL,
	withCredentials: true,
	headers: {
		'Content-Type': 'application/json',
	},
})

export async function registerUser({ username, password }) {
	const { data } = await api.post('/users/register/', { username, password })
	return data
}

export async function loginUser({ username, password }) {
	const { data } = await api.post('/users/login/', { username, password })
	return data
}

export async function logoutUser() {
	const { data } = await api.get('/users/logout/')
	return data
}

export async function getMe() {
	const { data } = await api.get('/users/me/')
	return data
}

export async function fetchQuestions() {
	const { data } = await api.get('/assesment/questions/')
	return data
}

export async function submitAssessment({ username, answers }) {
	const { data } = await api.post('/assesment/submit/', { username, answers })
	return data
}

export async function fetchProfile(username) {
	const { data } = await api.get(`/assesment/profile/${encodeURIComponent(username)}/`)
	return data
}
