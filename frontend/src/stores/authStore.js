import { defineStore } from 'pinia';
import axiosInstance from '../plugins/axios';
import { useRequestsStore } from './requestsStore'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: null,
        user: null,
        isLoading: false
    }),

    actions: {
        async _makeRequest(config, errorMessage, successMessage) {
            const requestsStore = useRequestsStore()
            try {
                return await requestsStore._makeRequest(config, successMessage)
            } catch (error) {
            if (errorMessage) {
                throw new Error(errorMessage)
            }
            throw error
            }
        },


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

                const tokens = await this._makeRequest({
                    method: 'post',
                    url: 'auth/telegram/',
                    data: {
                        init_data: initData
                    }
                }, "auth failed")

                this.token = tokens.access_token;
                this.user = { user_id: tokens.user_id };
                
                localStorage.setItem('tg_token', this.token);
                localStorage.setItem('tg_user', JSON.stringify(this.user));
                
                return tokens;
            } catch (error) {
                console.error('Login error:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        async initialize() {
            try {
                await this.login();
            } catch (error) {
                throw new Error(error);
            }
        }
    }
});