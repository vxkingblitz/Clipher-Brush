<template>
  <div class="select-wrapper">
    <p class="select-label">{{ label }}</p>
    <div class="custom-select" tabindex="1" @blur="handleBlur">
      
      <div 
        class="selected" 
        :class="{ open }" 
        :style="{ color: hasValue ? 'var(--color-black)' : 'var(--color-dark-gray)' }" 
        @click="toggleOpen"
      >
        {{ hasValue ? displayValue : placeholderdata }}
      </div>
      
      <transition name="slide-up">
        <div 
          v-if="open"
          :class="{ items: true, dropdownUp: dropdownUp }" 
          ref="dropdown" 
          :style="dropdownUp ? { bottom: '120%' } : {}"
        >
          <div class="search" v-if="searchable" @click="open = true">
            <InputField 
              :label="''" 
              :type="'search'" 
              :placeholder="'Поиск'" 
              :modelValue="searchTerm"
              @update:modelValue="searchTerm = $event"
            />
          </div>
          
          <div class="custom-input" v-if="showCustomInput">
            <InputField 
              :label="''" 
              :type="'text'" 
              :placeholder="''" 
              :modelValue="valueCustomInput"
              @update:modelValue="valueCustomInput = $event"
            />
            <IconButton @click="handleCustomInputAccept" :icon="'check.svg'" :color="'var(--color-accent)'"/>
          </div>
          
          <div 
            v-if="customValue && !showCustomInput" 
            @click="showCustomInput = true" 
            class="custom-value-button"
          >
            Указать свое значение
          </div>
          
          <div style="padding: 0 15px;" v-if="!filteredOptions.length">Здесь пока ничего нет</div>
          
          <div @click="handleOptionClick('Все')" v-if="selectAll">Все</div>
          
          <div
            v-for="option in filteredOptions"
            :key="getOptionKey(option)"
            @click="handleOptionClick(option)"
            class="option-item"
          >
            <span v-html="highlightMatch(getOptionName(option))"></span>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomSelect',
  props: {
    options: {
      type: [Array, Object],
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    placeholderdata: {
      type: String,
      default: ''
    },
    modelValue: {
      default: null
    },
    searchable: {
      type: Boolean,
      default: false
    },
    customValue: {
      type: Boolean,
      default: false
    },
    selectAll: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      open: false,
      searchTerm: '',
      dropdownUp: false,
      valueCustomInput: '',
      showCustomInput: false,
      internalValue: this.modelValue
    };
  },
  computed: {
    optionsList() {
      if (Array.isArray(this.options)) {
        return this.options;
      } else if (typeof this.options === 'object' && this.options !== null) {
        return Object.entries(this.options).map(([id, name]) => ({
          id,
          name
        }));
      }
      return [];
    },
    
    filteredOptions() {
      const term = this.searchTerm.toLowerCase();
      return this.optionsList.filter(option => 
        this.getOptionName(option).toLowerCase().includes(term)
      );
    },

    hasValue() {
      if (
        this.internalValue === null ||
        this.internalValue === undefined ||
        (typeof this.internalValue === "string" && this.internalValue.trim() === "")
      ) {
        return false;
      }
      if (
        typeof this.internalValue === "object" &&
        Object.keys(this.internalValue).length === 0
      ) {
        return false;
      }
      return true;
    },

    displayValue() {
      return this.hasValue ? this.getOptionName(this.internalValue) : '';
    }
  },
  watch: {
    modelValue(newValue) {
      this.internalValue = newValue;
    },
    
    internalValue(newValue) {
      this.$emit('update:modelValue', newValue);
    }
  },
  methods: {
    toggleOpen() {
      if (this.open) {
        this.open = false;
        setTimeout(() => {
          this.dropdownUp = false;
        }, 200);
      } else {
        this.checkDropdownDirection();
        this.open = true;
        this.showCustomInput = false;
        this.valueCustomInput = '';
      }
    },
    
    handleBlur() {
      setTimeout(() => {
        if (!this.$refs.dropdown?.contains(document.activeElement)) {
          this.open = false;
          setTimeout(() => {
            this.dropdownUp = false;
          }, 200);
        }
      }, 100);
    },
    
    checkDropdownDirection() {
      if (!this.$refs.dropdown) return;
      
      const dropdownRect = this.$refs.dropdown.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      const spaceBelow = windowHeight - dropdownRect.bottom;
      const estimatedHeight = 200;

      this.dropdownUp = spaceBelow < estimatedHeight;
    },
    
    handleOptionClick(option) {
      this.internalValue = option;
      this.open = false;
      this.searchTerm = '';
    },
    
    handleCustomInputAccept() {
      if (this.valueCustomInput) {
        this.internalValue = this.valueCustomInput;
        this.showCustomInput = false;
        this.valueCustomInput = '';
        this.open = false;
      }
      this.$emit('customValueAdded', this.internalValue);
    },
    
    getOptionKey(option) {
      return option?.id || option;
    },
    
    getOptionName(option) {
      if (!option) return '';
      
      const name = option?.name ?? option;
      return String(name)
    },
    
    highlightMatch(optionName) {
      const term = this.searchTerm.toLowerCase();
      const index = optionName.toLowerCase().indexOf(term);
      
      if (index > -1 && term.length > 0) {
        const before = optionName.substr(0, index);
        const match = optionName.substr(index, term.length);
        const after = optionName.substr(index + term.length);
        
        return `${before}<span style="color: var(--color-accent);">${match}</span>${after}`;
      }
      return optionName;
    }
  }
};
</script>



<style scoped>
.select-label{
  font-size: 14px;
  color: var(--color-dark-grey);
  margin: 0;
  font-family: 'Jost';
}
.select-wrapper{
  position: relative;
  display: flex;
  flex-direction: column;
}
.custom-input{
  display: flex;
  align-items: center;
  gap: 6px;
}
.select-hide {
  display: none;
}

.custom-value-button {  
  cursor: pointer;
  padding: 0 15px;
  border-bottom: solid 1px #C6CBD2;
  background-color: var(--color-white);
}
.items.dropdownUp {
  z-index: 9999;
}
.search>>>input{
  border: none;
}

.search{
  border-bottom: solid 1px #C6CBD2;
  height: fit-content;
}

.custom-select {
  width: 100%;
  text-align: left;
  justify-items: center;
  outline: none;
  height: 50px;
  line-height: 50px;
  font-family: 'Jost';
  border: 1px solid var(--color-main);
  border-radius: 32px;
  font-size: 16px;
}

.selected {
  background-color: transparent;
  border-radius: 10px;
  padding: 0 15px;
  cursor: pointer;
  user-select: none;
  height: 34px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.selected.open {
  border-radius: 10px;
}

/* .selected:after {
  position: absolute;
  content: "";
  top: 22px;
  right: 1em;
  width: 0;
  height: 0;
  border: 3px solid transparent;
  border-color: var(--color-main) transparent transparent transparent;

  rotate: 0deg;
  transition: .3s ease all;
}

.selected.open:after{
  top: 20px;
  rotate: 180deg;
  transition: .3s ease all;
} */



.option-item {
  color: var(--color-dark-grey);
  background-color: var(--color-white);
  padding: 0 15px;
  cursor: pointer;
  user-select: none;
}

.option-item:hover, .custom-value-button:hover {
  background-color: #e7e7e7;
}


.selectHide div{
  padding-left: 1em;
  padding-right: 1em;
}

.selectHide {
  opacity: 0;
  max-height: 170px;
  overflow-y: scroll;
  margin-top: 10px;
  color: var(--color-dark-grey);
  border-radius: 10px;
  position: absolute;
  background-color: #FFFFFF;
  left: 0;
  right: 0;
  z-index: 1;
  filter: drop-shadow(0 0 10px rgb(227, 227, 227));
  transition: all .2s ease;
  visibility: hidden;
}

.items {
  opacity: 1;
  max-height: 170px;
  overflow-x: hidden;
  overflow-y: scroll;
  margin-top: 20px;
  color: var(--color-black);
  border-radius: 32px;
  border: 1px solid var(--color-main);
  position: absolute;
  background-color: var(--color-white);
  left: 0;
  right: 0;
  z-index: 1;
  filter: drop-shadow(0 0 10px rgb(227, 227, 227));
  width: 100%;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: transform 0.33s cubic-bezier(0.38, 0.12, 0.3, 1), opacity 0.33s cubic-bezier(0.38, 0.12, 0.3, 1);
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
.slide-up-enter-to,
.slide-up-leave-from {
  transform: translateY(0);
  opacity: 1;
}

@media (max-width: 768px){
  .select-wrapper{
    position: inherit;
    display: flex;
    flex-direction: column;
  }
  .items {
    opacity: 1;
    max-height: 80svh;
    overflow-x: hidden;
    overflow-y: scroll;
    color: var(--color-black);
    border-radius: 32px 32px 0 0;
    border: 1px solid var(--color-main);
    position: fixed;
    background-color: var(--color-white);
    bottom: 0;
    left: 0;
    width: 100%;
    padding-bottom: 100px;
    z-index: 20;
    filter: drop-shadow(0 0 10px rgb(227, 227, 227));
  }
}
</style>