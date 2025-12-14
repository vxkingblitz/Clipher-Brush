<template>
    <div class="textfield-wrapper" :style="{'gap': label ? '6px' : '0'}">
        <div class="textfileld-row">
            <!-- <p class="label">{{ label }}</p> -->
            <ToolTip v-if="tooltip" :text="tooltip"/>
        </div>
        <div class="input-container">
            <img 
                v-if="iconStart" 
                :src="getIconPath(iconStart)" 
                class="icon-start"
                :alt="iconStart"
            />
            <div style="position: relative;">
                <input
                    :type="type"
                    :maxlength="maxLength"
                    :value="modelValue"
                    :placeholder="placeholder"
                    @input="onInput($event.target.value)"
                    :style="{ 
                        borderColor: error ? 'var(--color-red)' : '',
                        paddingLeft: iconStart ? '40px' : '15px'
                    }"
                    :required="required"
                    :disabled="disabled"
                    :class="{ 'with-icon-start': iconStart }"
                />
                <svg  
                    v-if="modelValue.length > 0" 
                    @click="onInput('')" 
                    width="10" 
                    height="10" 
                    viewBox="0 0 10 10" 
                    fill="none" 
                    xmlns="http://www.w3.org/2000/svg"
                    class="icon-clear"
                >
                    <path d="M5.97331 5L9.66665 8.69333V9.66667H8.69331L4.99998 5.97333L1.30665 9.66667H0.333313V8.69333L4.02665 5L0.333313 1.30667V0.333332H1.30665L4.99998 4.02667L8.69331 0.333332H9.66665V1.30667L5.97331 5Z" fill="#B5B7CB"/>
                </svg>
            </div>
            <p v-if="maxLength > 0" class="counter">
                {{ modelValue.length }}/{{ maxLength }}
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: "TextField",
    props: {
        label: String,
        type: {
            type: String,
            default: 'text'
        },
        maxLength: Number,
        error: Boolean,
        modelValue: {
            type: String,
            default: '',
        },
        placeholder: String,
        required: {
            type: Boolean,
            default: false
        },
        tooltip: {
            type: String,
            default: null,
        },
        disabled: Boolean,
        iconStart: {
            type: String,
            default: null
        }
    },
    methods: {
        onInput(newValue) {
            this.$emit('update:modelValue', newValue);
            this.$emit('update:value', newValue);
        },
        getIconPath(iconName) {
            return new URL(`/src/assets/icons/${iconName}.svg`, import.meta.url).href;
        }
    },
};
</script>

<style scoped>
.textfileld-row{
    display: flex;
    align-items: center;
    gap: 10px;
}
.input-container {
    position: relative;
    width: 100%;
}
.icon-start {
    position: absolute;
    left: 13px;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    z-index: 1;
    pointer-events: none;
}
.icon-clear{
    cursor: pointer;
    position: absolute;
    width: 10px;
    aspect-ratio: 1;
    right: 15px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
    top: '18px'
}
.icon-clear:hover{
    filter: brightness(50%);
}
.textfield-wrapper{
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
    position: relative;
}
input{
    font-size: 16px;
    border-radius: 32px;
    padding: 12px 20px;
    border: 1px solid var(--color-main);
    color: var(--color-black);
    padding-right: 35px;
    font-family: 'Jost';
    background-color: var(--color-white);
    width: 100%;
    box-sizing: border-box;
}
input.with-icon-start {
    padding-left: 40px;
}
input::placeholder{
    font-family: 'Jost';
    color: var(--color-dark-gray);
}
.label{
    font-size: 14px;
    color: var(--color-dark-grey);
    margin: 0;
    font-family: 'Jost';
}
.counter{
    font-size: 14px;
    color: #808080;
    display: flex;
    justify-content: end;
    text-align: end;
    margin: 0;
    margin-top: 4px;
}
</style>