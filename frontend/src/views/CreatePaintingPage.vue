<template>
    <div id="pageView" class="createWrapper">
        <h1 v-if="step == 1">Добро пожаловать в <br> создание волшебства!</h1>
        <h1 v-if="step == 2">Еще чуть-чуть :)</h1>
        <h1 v-if="step == 3">Создание шедевра!</h1>
        <h1 v-if="step == 4">Все готово!</h1>

        <div id="pageView" class="createContent" v-if="step == 1" @click="openFileInput">
            <input 
                ref="fileInput" 
                type="file" 
                accept="image/jpeg,image/png,image/jpg" 
                style="display: none;" 
                @change="handleFileSelect"
            />
            <div class="addPhoto" v-if="!formData.photo">
                <img src="../assets/img/brush.png" alt="brush">
                <h2>Создай свой рисунок</h2>
                <p>Добавь свое изоюражение сюда и начнется магия</p>
                <span>jpg, png</span>
            </div>
            <div v-else style="display: flex; flex-direction: column; gap: 30px; align-items: center; justify-content: center; margin-top: 30px;">
                <img :src="photoPreview" alt="photo_for_drawing" class="imagePreview">
                <div class="actions">
                    <ButtonComponent :variant="1" :label="'Далее'" @click.stop="window.Telegram.WebApp.HapticFeedback.impactOccurred('light'); step = 2" :isLoading="false"/>
                    <ButtonComponent :variant="3" :label="'Изменить изображение'" @click.stop="window.Telegram.WebApp.HapticFeedback.impactOccurred('light'); openFileInput" :isLoading="false"/>
                </div>
            </div>
        </div>


        <div id="pageView" class="createContent" v-if="step == 2" style="height: 70vh;">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <div class="actions">
                <InputField
                    :required="true"
                    :type="'tel'"
                    :placeholder="'Введите количество цветов'"
                    v-model="s"
                />
                <SelectList
                    :options="['1 день', '1 неделя', '1 месяц', '6 месяев', 'Год']"
                    :searchable="false"
                    :placeholderdata="'Выберите период'"
                />
                <ButtonComponent :variant="1" :label="'Создать раскраску'" @click="window.Telegram.WebApp.HapticFeedback.impactOccurred('light'); step = 3" :isLoading="false"/>
            </div>
        </div>

        <div id="pageView" class="createContent" v-if="step == 3" style="height: 70vh;">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <h4>Генерация изображения</h4>
            <div class="loadingStatusWrapper">
                <div class="loadingStatusActive" style="width: 60%;"></div>
            </div>
            <span>Подбираем цвета...</span>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            photoPreview: null,
            step: 1,

            formData:{
                photo: null,
                colors_amount: Number,
                markers_set: Object,
            }
        }
    },
    methods: {
        openFileInput() {
            this.$refs.fileInput?.click();
        },
        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                if (file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg') {
                    this.formData.photo = file;
                    this.photo = true;
                    this.photoPreview = URL.createObjectURL(file);
                } else {
                    alert('Пожалуйста, выберите файл в формате JPG или PNG');
                }
            }
        }
    },
    beforeUnmount() {
        if (this.photoPreview) {
            URL.revokeObjectURL(this.photoPreview);
        }
    }
}
</script>

<style scoped>
h4{
    margin: 26px 0;
    font-size: 20px;
    font-weight: 500;
    color: var(--color-black);
}
span{
    font-size: 15px;
    font-weight: 500;
    color: var(--color-dark-gray);
}
.loadingStatusWrapper{
    position: relative;
    height: 20px;
    background-color: var(--color-light-gray);
    border-radius: 10px;
    overflow: hidden;
    width: 80vw;
}
.loadingStatusActive{
    position: absolute;
    height: 20px;
    background-color: var(--color-main);
}
.imagePreview{
    object-fit: cover;
    width: 50vw;
    height: 40vh;
    border-radius: 32px;
}
.actions{
    width: 314px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
}
.createWrapper{
    height: 100svh;
}
.createContent{
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 60%;
    align-items: center;
    justify-content: center;
}
.addPhoto{
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
    justify-content: center;
    border: 1px dashed var(--color-black);
    border-radius: 32px;
    width: 280px;
    aspect-ratio: 1;
}
.addPhoto h2{
    text-align: center;
    color: var(--color-black);
    margin: 0;
    font-weight: 500;
    font-size: 20px;
}
.addPhoto p{
    text-align: center;
    color: var(--color-dark-gray);
    margin: 0;
    font-weight: 400;
    font-size: 15px;
}
.addPhoto span{
    text-align: center;
    color: var(--color-blue);
    margin: 0;
    font-weight: 400;
    font-size: 12px;
    margin: 24px 0 10px 0
}
</style>