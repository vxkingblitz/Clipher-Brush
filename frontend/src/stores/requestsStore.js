import { defineStore } from 'pinia'
import { axiosInstance } from '../plugins/axios'
import { useAuthStore } from './authStore'
import { useAlertsStore } from './alertsStore'

export const useRequestsStore = defineStore('requests', {
    actions: {
        /**
         * Универсальная функция для отправки HTTP запросов
         * @param {Object} config - конфигурация axios (method, url, data, headers и т.д.)
         * @param {String|null} successMessage - опциональное сообщение об успехе
         * @param {Boolean} replaceShopId - опционально: заменить {shopId} в URL на текущий shop ID
         * @returns {Promise} - данные из response.data
         */
        async _makeRequest(config, successMessage = null, replaceShopId = false) {
            try {
                // Обработка замены {shopId} в URL
                let finalUrl = config.url
                if (replaceShopId && config.url && config.url.includes('{shopId}')) {
                    const shopsStore = useShopsStore()
                    if (!shopsStore.currentShop?.id) {
                        throw new Error('Текущий магазин не выбран')
                    }
                    finalUrl = config.url.replace('{shopId}', shopsStore.currentShop.id)
                }

                // Выполнение запроса (токен добавляется автоматически через interceptor)
                const response = await axiosInstance({
                    ...config,
                    url: finalUrl,
                    headers: {
                        ...config.headers,
                    },
                })

                const responseData = response.data
                

                return responseData
            } catch (error) {
                const alertsStore = useAlertsStore()
                let errorMessage = 'Произошла ошибка'

                if (error.response?.data && typeof error.response.data === 'object') {
                    const errorData = error.response.data
                    if ('status' in errorData && 'messages' in errorData) {
                        errorMessage = this._formatErrorMessage(errorData)
                    } else if (errorData.message) {
                        errorMessage = errorData.message
                    } else if (error.response.data?.detail) {
                        errorMessage = error.response.data.detail
                    }
                } else if (error.message) {
                    errorMessage = error.message
                }

                alertsStore.showNotification({
                    message: errorMessage,
                    status: 'error'
                })

                throw error
            }
        },

        /**
         * Форматирует сообщение об ошибке из формата {status, title, messages}
         * @param {Object} errorData - объект с полями status, title, messages
         * @returns {String} - отформатированное сообщение
         */
        _formatErrorMessage(errorData) {
            if (errorData.messages && Array.isArray(errorData.messages) && errorData.messages.length > 0) {
                // Используем первое сообщение из массива (обычно это русское)
                return errorData.messages[0]
            } else if (errorData.title) {
                return errorData.title
            } else if (errorData.message) {
                return errorData.message
            }
            return 'Произошла ошибка'
        }
    }
})