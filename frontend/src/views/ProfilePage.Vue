<template>
  <div id="pageView" class="profileWrapper">
    <h1>Добро пожаловать<br>в твои шедевры!</h1>

    <TabMenu
        style="position: sticky; top: 0; z-index: 1; background-color: var(--color-white);"
        v-model="menuTab" 
        :tabs="[
            { id: 'favourites', label: 'Избранное' },
            { id: 'my_works', label: 'Мои работы' },
        ]" 
        @tab-change="val => setTab(val)"
    />

    <section class="feed-content">
        <PaintingCard v-for="i in 10" :key="i.id"/>
    </section>
  </div>
</template>

<script>
export default {
    data(){
        return{
            menuTab: 'favourites',
        }
    },
    methods:{
        setTab(tab) {
            this.$router.push({ name: 'Profile', params: { tab } })
        },
    }
}
</script>

<style scoped>
.feed-content{
    padding: 0 6px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: 1fr;
    grid-column-gap: 6px;
    grid-row-gap: 6px;
    margin-bottom: 110px;
}
</style>