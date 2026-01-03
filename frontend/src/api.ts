import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // In production or docker, this might need adjustment/proxy
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
