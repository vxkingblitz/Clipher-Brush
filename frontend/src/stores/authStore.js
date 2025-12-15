import { defineStore } from 'pinia';
import axiosInstance from '../plugins/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('tg_token') || null,
        user: null,
        isLoading: false
    }),

    getters: {
        isAuthenticated: (state) => !!state.token
    },

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

                const response = await axiosInstance.post('/auth/telegram/', {
                    init_data: initData
                });

                this.token = response.data.access_token;
                this.user = { user_id: response.data.user_id };
                
                localStorage.setItem('tg_token', response.data.access_token);
                localStorage.setItem('tg_user', JSON.stringify({ user_id: response.data.user_id }));
                
                return response.data;
            } catch (error) {
                console.error('Login error:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        restoreSession() {
            const savedUser = localStorage.getItem('tg_user');
            if (savedUser) {
                this.user = JSON.parse(savedUser);
            }
        },

        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('tg_token');
            localStorage.removeItem('tg_user');
        },

        async initialize() {
            this.restoreSession();
            
            // Проверяем наличие Telegram WebApp
            const tg = window.Telegram?.WebApp;
            if (!tg) {
                console.warn('Telegram WebApp not available');
                return;
            }

            // Если есть токен, но нет пользователя, пытаемся восстановить сессию
            if (this.token && !this.user) {
                try {
                    // Можно добавить проверку токена через API
                    // Пока просто восстанавливаем из localStorage
                    this.restoreSession();
                } catch (error) {
                    console.error('Session restore failed:', error);
                    this.logout();
                }
            }
            
            // Если нет токена, но есть данные из Telegram, авторизуемся
            if (!this.token && tg.initData) {
                try {
                    await this.login();
                } catch (error) {
                    console.error('Initial login failed:', error);
                }
            }
            
            // Если есть initData, но нет токена, пытаемся авторизоваться
            if (!this.token && tg.initDataUnsafe?.user) {
                try {
                    await this.login();
                } catch (error) {
                    console.error('Telegram login failed:', error);
                }
            }
        }
    }
});