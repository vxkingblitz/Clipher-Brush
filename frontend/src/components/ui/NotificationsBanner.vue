<template>
    <div class="alert" :class="{ 'show': isVisible, 'hide': !isVisible }" :style="{ backgroundColor: backgroundColor() }">
        <h4>{{ title }}</h4>
        <p>{{ message }}</p>
        <!-- <div @click="hideNotification" style="display: flex; align-items: center; cursor: pointer;">
            <svg width="10" height="10" viewBox="0 0 6 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.29294 3.00003L0.146484 5.14648L0.853591 5.85359L3.00004 3.70714L5.1465 5.85359L5.85361 5.14648L3.70715 3.00003L5.85359 0.853591L5.14648 0.146484L3.00004 2.29292L0.853605 0.146484L0.146499 0.853591L2.29294 3.00003Z" fill="white"/>
            </svg>
        </div> -->
    </div>
</template>

<script>
import { useAlertsStore } from '../../stores/alertsStore.js';
import { mapStores } from 'pinia'

export default {
    computed: {
        ...mapStores(useAlertsStore),
        isVisible(){
            return this.alertsStore.notification.isVisible
        },
        message(){
            return this.alertsStore.notification.message
        },
        status(){
            return this.alertsStore.notification.status
        },
        title(){
            switch (this.status) {
                case 'error':
                    return 'Произошла ошибка!'
                    break;
                case 'success':
                    return 'Успешно!'
                    break;
                case 'notify':
                    return 'Внимание!'
                    break;
                default:
                    break;
            }
        }
    },
    methods:{
        backgroundColor(){
            switch (this.status) {
                case 'error':
                    return 'var(--color-red)'
                    break;
                case 'success':
                    return 'var(--color-green)'
                    break;
                case 'notify':
                    return 'var(--color-yellow)'
                    break;
                default:
                    break;
            }
        },
    }
};
</script>

<style scoped>
svg:hover path{
    fill: rgb(161, 161, 161);
}
.alert {
    position: fixed;
    /* bottom: 20px;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0; */
    top: 50px;
    right: 50px;
    overflow: hidden;
    text-overflow: ellipsis;
    border-radius: 10px;
    padding: 10px 15px;
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: start;
    gap: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transition: all .2s cubic-bezier(0.560, 1.555, 0.305, 0.940);
    width: 300px;
}
p{
    margin: 0;
    color: var(--color-white);
    font-family: 'Jost';
    font-size: 12px;
    font-weight: 300;
}
h4{
    margin: 0;
    color: var(--color-white);
    font-family: 'Jost';
    font-size: 16px;
    font-weight: 500;
}
.alert.show {
    opacity: 1;
    transform: translateX(0);
    scale: 1;
}

.alert.hide {
    opacity: 0;
    scale: .8;
    transform: translateX(100px);
    pointer-events: none;
}
@media (max-width: 768px){
    .alert{
        top: 20px;
        margin-left: auto;
        margin-right: auto;
        left: 0;
        right: 0;
    }
    .alert.show {
        opacity: 1;
        transform: translateX(0);
        transform: translateY(0);
        scale: 1;
    }

    .alert.hide {
        opacity: 0;
        scale: .8;
        transform: translateX(0);
        transform: translateY(-100px);
        pointer-events: none;
    }
}
</style>