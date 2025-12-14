import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/router.js'

import NavBar from "./components/ui/NavBar.vue";

const app = createApp(App)
const pinia = createPinia()


app.component('NavBar', NavBar);

app.use(pinia)
app.use(router)

app.mount('#app')
