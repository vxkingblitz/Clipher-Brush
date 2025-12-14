<template>
    <div class="skeleton">
  
    </div>
</template>

<script>
    export default {

    }
</script>

<style scoped>
.skeleton {
    background: linear-gradient(90deg, var(--color-white), var(--color-light-gray), var(--color-white));
    background-size: 200% 100%;
    border-radius: 32px;
    animation: shimmer 3s infinite linear;
    margin-bottom: 4px;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}
</style>