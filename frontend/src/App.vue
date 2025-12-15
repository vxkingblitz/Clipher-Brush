<template>
  <div id="app">
    <RouterView style="padding-top: 10%;"/>
    <NavBar/>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useAuthStore } from './stores/authStore';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();

    onMounted(async () => {
      // Инициализация Telegram WebApp
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
      }

      // Авторизация через Telegram мини-приложение
      await authStore.initialize();
    });
  }
}
</script>

<style>
* {
  -webkit-tap-highlight-color: transparent;
  -webkit-appearance: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -o-user-select: none;
  user-select: none;
}


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Jost", sans-serif;
}
:root{
  --color-main: #71557B;
  --color-black: #0B0909;
  --color-white: #F4F4F4;
  --color-red: #AD0303;
  --color-blue: #0066C5;
  --color-light-gray: #E2E2E2;
  --color-dark-gray: #7B7B7B;
}
body{
  background-color: var(--color-white);
  margin: 0;
  padding: 0;
}
h1{
  text-align: center;
  color: var(--color-black);
  font-size: 30px;
  font-weight: 500;
  line-height: 30px;
}
#pageView{
  animation: show .5s ease forwards;
}
@keyframes show {
    0% {
        margin-top: 10px;
        opacity: 0;
    }
    100% {
        margin-top: 0;
        opacity: 1;
    }
}


.messageBox{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.messageBox span{
    margin-top: -30px;
    font-weight: 500;
}
</style>