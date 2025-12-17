<template>
    <div id="pageView" class="createWrapper">
        <h1 style="margin-bottom: 40px;" v-if="step == 1">Добро пожаловать в <br> создание волшебства!</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 2">Еще чуть-чуть :)</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 3">Создание шедевра!</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 4">Все готово!</h1>

        <div id="pageView" class="createContent" v-if="step == 1" @click="openFileInput()">
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
            <div v-else style="display: flex; flex-direction: column; gap: 30px; align-items: center; justify-content: center;">
                <img :src="photoPreview" alt="photo_for_drawing" class="imagePreview">
                <div class="actions">
                    <ButtonComponent :variant="1" :label="'Далее'" @click.stop="handleHapticFeedback(); step = 2" :isLoading="false"/>
                    <ButtonComponent :variant="3" :label="'Изменить изображение'" @click.stop="handleHapticFeedback(); openFileInput()" :isLoading="false"/>
                </div>
            </div>
        </div>


        <div id="pageView" class="createContent" v-if="step == 2">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <div class="actions">
                <InputField
                    :required="true"
                    :type="'tel'"
                    :placeholder="'Введите количество цветов'"
                    v-model="formData.colors_amount"
                />
                <SelectList
                    :options="markers_list"
                    :searchable="false"
                    :placeholderdata="'Выберите набор маркеров'"
                    v-model="formData.markers_set"
                />
                <ButtonComponent :variant="1" :label="'Создать раскраску'" @click="handleHapticFeedback(); step = 3; generatePainting()" :isLoading="false" :disabled="!formData.colors_amount || !formData.markers_set"/>
            </div>
        </div>

        <div id="pageView" class="createContent" v-if="step == 3">
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
import { useGeneratorStore } from '../stores/paintingGenerateStore'
import { mapStores } from 'pinia'

export default {
    data(){
        return{
            photoPreview: null,
            step: 1,

            formData:{
                photo: null,
                colors_amount: '',
                markers_set: '',
            },

            markers_list:[
                'Без набора',
                'GuangNa, 240шт',
                'GuangNa, 120шт',
                'GuangNa, 64шт',
                'GuangNa, 32шт',
                'Languo , 240шт',
                'Languo , 120шт',
                'Languo , 64шт',
                'Languo , 32шт',
            ]
        }
    },
    methods: {
        handleHapticFeedback() {
            if (window.Telegram?.WebApp?.HapticFeedback) {
                window.Telegram.WebApp.HapticFeedback.impactOccurred('light')
            }
        },
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
        },
        async generatePainting(){
            // Преобразуем markers_set из строки в ID или null
            // Если выбрано "Без набора", передаем null
            let markers_set_id = null;
            if (this.formData.markers_set && this.formData.markers_set !== 'Без набора') {
                // Здесь можно добавить маппинг строк в ID, если нужно
                // Пока передаем null, если не "Без набора"
                markers_set_id = null; // TODO: добавить маппинг строк в реальные ID из БД
            }
            
            let payload = {
                photo: this.formData.photo,
                // Не передаем category_id если он 0 или не выбран
                ...(this.formData.category_id && this.formData.category_id > 0 ? { category_id: this.formData.category_id } : {}),
                ...(markers_set_id ? { markers_set_id: markers_set_id } : {}),
                colors_amount: parseInt(this.formData.colors_amount) || 0,
            }
            
            console.log('Sending payload:', payload);
            
            try {
                await this.generatorStore.generatePainting(payload);
                this.step = 4; // Переход на шаг "Все готово"
            } catch (error) {
                console.error('Ошибка генерации:', error);
                alert('Произошла ошибка при создании раскраски');
                this.step = 2; // Возврат на шаг выбора параметров
            }
        },
    },
    beforeUnmount() {
        if (this.photoPreview) {
            URL.revokeObjectURL(this.photoPreview);
        }
    },
    computed: {
        ...mapStores(useGeneratorStore),
    },
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