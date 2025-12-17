"use strict";
import axios from "axios";
import { useAuthStore } from "../stores/authStore.js";

let apiURL = 'https://cipherbrush.ru/api/';
apiURL = apiURL.replace(/"/g, "").trim();
if (!apiURL.endsWith("/")) apiURL += "/";
const config = {
  baseURL: apiURL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
  crossDomain: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
};

const _axios = axios.create(config);

_axios.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    console.log(authStore.token);
    if (authStore.token) {
      config.headers["Authorization"] = `Bearer ${authStore.token}`;
    }
    config.withCredentials = true;
    return config;
  },
  (error) => Promise.reject(error)
);

_axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const authStore = useAuthStore();

    if (error.response && error.response.status === 401) {
      try {
        // Если есть метод refresh в store, используем его
        if (authStore.refresh) {
          await authStore.refresh();
          const newToken = authStore.token;
          if (newToken) {
            error.config.headers["Authorization"] = `Bearer ${newToken}`;
          }
          if (!error.config._retry) {
            error.config._retry = true;
            return _axios.request(error.config);
          }
        } else {
          // Если нет refresh метода, просто разлогиниваем
          authStore.logout();
        }
      } catch (refreshError) {
        console.error("Token expired, logging out...");
        authStore.logout();
      }
    }

    if (error.response && error.response.status === 405) {
      console.error("Method Not Allowed - проверь endpoint и метод запроса");
    }

    return Promise.reject(error);
  }
);

const Plugin = {
  install(app) {
    app.config.globalProperties.$axios = _axios;
    app.config.globalProperties.axios = _axios;
    app.provide("axios", _axios);
  },
};

export const axiosInstance = _axios;
export default Plugin;