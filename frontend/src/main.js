import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/router.js'

import NavBar from "./components/ui/NavBar.vue";
import TabMenu from "./components/ui/TabMenu.vue";
import PaintingCard from "./components/PaintingCard.vue";
import ButtonComponent from "./components/ui/ButtonComponent.vue";
import InputField from "./components/ui/TextField.vue";
import SelectList from "./components/ui/SelectList.vue";
import SkeletonLoader from "./components/ui/SkeletonLoader.vue";
import Notification from "./components/ui/NotificationsBanner.vue";

const app = createApp(App)
const pinia = createPinia()


app.component('NavBar', NavBar);
app.component('TabMenu', TabMenu);
app.component('PaintingCard', PaintingCard);
app.component('ButtonComponent', ButtonComponent);
app.component('InputField', InputField);
app.component('SelectList', SelectList);
app.component('SkeletonLoader', SkeletonLoader);
app.component('Notification', Notification);

app.use(pinia)
app.use(router)

app.mount('#app')
