import { defineStore } from 'pinia';
import axiosInstance from '../plugins/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('tg_token') || null,
        user: null,
        isLoading: false
    }),

    actions: {
        async login() {
            try {
                this.isLoading = true;
                
                const tg = window.Telegram?.WebApp;
                if (!tg) {
                    throw new Error('Telegram WebApp not available');
                }

                const initData = tg.initData;
                if (!initData) {
                    throw new Error('Telegram initData not available');
                }

                // Авторизация через бэкенд: создаем/обновляем пользователя и получаем JWT
                // Внешний URL: https://cipherbrush.ru/api/auth/auth/telegram/
                const response = await axiosInstance.post('/auth/auth/telegram/', {
                    init_data: initData
                });

                this.token = response.data.access_token;
                this.user = { user_id: response.data.user_id };
                
                localStorage.setItem('tg_token', this.token);
                localStorage.setItem('tg_user', JSON.stringify(this.user));
                
                return response.data;
            } catch (error) {
                console.error('Login error:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        async initialize() {
            try {
                // Если токен уже есть (например, из предыдущей сессии), просто восстановим данные пользователя
                const savedToken = localStorage.getItem('tg_token');
                const savedUser = localStorage.getItem('tg_user');

                if (savedToken && savedUser) {
                    this.token = savedToken;
                    this.user = JSON.parse(savedUser);
                    return;
                }

                await this.login();
            } catch (error) {
                throw new Error(error);
            }
        }
    }
});