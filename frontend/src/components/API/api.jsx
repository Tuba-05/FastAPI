// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// 1. Automatically add the Access Token to every outgoing request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 2. Handle 401 (Expired Token) errors automatically
api.interceptors.response.use(
  (response) => response, 
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Call your refresh endpoint 
        // (The Refresh Token cookie is sent automatically by the browser)
        const res = await axios.post("http://localhost:8000/refresh", {}, { withCredentials: true });
        
        if (res.status === 200) {
          const newToken = res.data.access_token;
          localStorage.setItem("token", newToken);
          
          // Retry the original request with the new token
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, logout the user
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// part  to be added in auth pages i think :)
import api from './api';

const Dashboard = () => {
  const fetchData = async () => {
    try {
      // No need to manually add headers! The interceptor does it.
      const response = await api.get("/protected-data");
      console.log(response.data);
    } catch (err) {
      console.log("Session expired or error occurred");
    }
  };

  return <button onClick={fetchData}>Get Private Data</button>;
};
