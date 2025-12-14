<template>
  <div id="app">
    <RouterView/>
    <NavBar/>
  </div>
</template>

<script>
</script>

<style>

*::-webkit-scrollbar,
html *::-webkit-scrollbar {
  height: 12px;
  width: 12px;
}
*::-webkit-scrollbar-track,
html *::-webkit-scrollbar-track {
  background: transparent;
}
*::-webkit-scrollbar-thumb,
html *::-webkit-scrollbar-thumb {
  background-color: #E5E8EB;
  border-radius: 5px;
  border: 3px solid transparent;
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