import axios from "axios";

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;

const axiosInstance = axios.create({
  baseURL: baseUrl,
  timeout: 5600,
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
