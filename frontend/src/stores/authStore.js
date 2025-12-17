import { defineStore } from 'pinia';
import axiosInstance from '../plugins/axios';
import { useRequestsStore } from './requestsStore'
import router from '../router/router.js';
import { useAlertsStore } from './alertsStore';

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

                const response = await this._makeRequest({
                    method: 'post',
                    url: 'auth/telegram/',
                    data: {
                        init_data: initData
                    }
                }, "auth failed")

                this.token = response.access_token;
                this.user = { user_id: response.user_id };
                
                localStorage.setItem('tg_token', this.token);
                localStorage.setItem('tg_user', JSON.stringify(this.user));
                
                try {
                    await router.push({ name: 'Feed', params: { tab: 'all' } });
                } catch (routerError) {
                    console.error('Router navigation error:', routerError);
                    const alertsStore = useAlertsStore();
                    alertsStore.showNotification({
                        message: 'Ошибка навигации',
                        status: 'error'
                    });
                }
                
                return response;
            } catch (error) {
                console.error('Login error:', error);
                const alertsStore = useAlertsStore();
                alertsStore.showNotification({
                    message: error.message || 'Ошибка авторизации',
                    status: 'error'
                });
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