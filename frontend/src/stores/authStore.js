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
                const userData = tg.initDataUnsafe.user;

                if (!userData) {
                    throw new Error('User data not available');
                }

                const response = await axiosInstance.post('/auth/telegram', {
                    initData: initData,
                    user: userData
                });

                this.token = response.data.token;
                this.user = response.data.user;
                
                localStorage.setItem('tg_token', response.data.token);
                localStorage.setItem('tg_user', JSON.stringify(response.data.user));
                
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
            
            if (this.token && !this.user) {
                try {
                    await this.login();
                } catch (error) {
                    console.error('Auto-login failed:', error);
                    this.logout();
                }
            }
            
            if (!this.token && window.Telegram?.WebApp?.initDataUnsafe?.user) {
                try {
                    await this.login();
                } catch (error) {
                    console.error('Initial login failed:', error);
                }
            }
        }
    }
});