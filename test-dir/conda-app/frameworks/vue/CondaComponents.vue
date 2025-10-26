<script setup>
// CONDA Vue 3 Components Library - Composition API
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
</script>

<script>
// Button Component
export const CondaButton = {
  name: 'CondaButton',
  props: {
    variant: { type: String, default: 'primary' },
    size: { type: String, default: 'medium' },
    disabled: Boolean
  },
  template: `
    <button 
      :class="['conda-button', \`conda-button-\${variant}\`, \`conda-button-\${size}\`]"
      :disabled="disabled"
      @click="$emit('click', $event)"
    >
      <slot />
    </button>
  `
};

// Modal Component
export const CondaModal = {
  name: 'CondaModal',
  props: {
    modelValue: Boolean,
    title: String,
    size: { type: String, default: 'medium' },
    closeOnOverlay: { type: Boolean, default: true },
    showClose: { type: Boolean, default: true }
  },
  emits: ['update:modelValue', 'close'],
  setup(props, { emit }) {
    const close = () => {
      emit('update:modelValue', false);
      emit('close');
    };
    
    const handleOverlay = (e) => {
      if (props.closeOnOverlay && e.target === e.currentTarget) {
        close();
      }
    };
    
    const handleEscape = (e) => {
      if (e.key === 'Escape' && props.modelValue) {
        close();
      }
    };
    
    watch(() => props.modelValue, (isOpen) => {
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    
    onMounted(() => {
      document.addEventListener('keydown', handleEscape);
    });
    
    onUnmounted(() => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    });
    
    return { close, handleOverlay };
  },
  template: `
    <Teleport to="body">
      <div v-if="modelValue" :class="['conda-modal-overlay', { active: modelValue }]" @click="handleOverlay">
        <div :class="['conda-modal', \`conda-modal-\${size}\`]" role="dialog" aria-modal="true">
          <div class="conda-modal-header">
            <h2 class="conda-modal-title">{{ title }}</h2>
            <button v-if="showClose" class="conda-modal-close" @click="close" aria-label="Close">&times;</button>
          </div>
          <div class="conda-modal-body">
            <slot />
          </div>
          <div v-if="$slots.footer" class="conda-modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Teleport>
  `
};

// Tabs Component
export const CondaTabs = {
  name: 'CondaTabs',
  props: {
    modelValue: { type: Number, default: 0 }
  },
  emits: ['update:modelValue', 'change'],
  setup(props, { emit, slots }) {
    const activeTab = ref(props.modelValue);
    
    const selectTab = (index) => {
      activeTab.value = index;
      emit('update:modelValue', index);
      emit('change', index);
    };
    
    watch(() => props.modelValue, (val) => {
      activeTab.value = val;
    });
    
    return { activeTab, selectTab };
  },
  template: `
    <div class="conda-tabs">
      <div class="conda-tabs-nav" role="tablist">
        <button
          v-for="(tab, index) in $slots.default()"
          :key="index"
          :class="['conda-tab-button', { active: activeTab === index }]"
          @click="selectTab(index)"
          role="tab"
          :aria-selected="activeTab === index"
        >
          {{ tab.props?.label }}
        </button>
      </div>
      <div
        v-for="(tab, index) in $slots.default()"
        :key="index"
        :class="['conda-tab-content', { active: activeTab === index }]"
        role="tabpanel"
      >
        <component :is="tab" v-if="activeTab === index" />
      </div>
    </div>
  `
};

export const CondaTab = {
  name: 'CondaTab',
  props: { label: String, icon: String },
  template: '<div><slot /></div>'
};

// Input Component  
export const CondaInput = {
  name: 'CondaInput',
  props: {
    modelValue: [String, Number],
    label: String,
    error: String,
    helpText: String,
    required: Boolean
  },
  emits: ['update:modelValue'],
  template: `
    <div class="conda-form-group">
      <label v-if="label" :class="['conda-form-label', { required }]">{{ label }}</label>
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :class="['conda-form-input', { error }]"
        v-bind="$attrs"
      />
      <span v-if="helpText" class="conda-form-help">{{ helpText }}</span>
      <span v-if="error" class="conda-form-error">{{ error }}</span>
    </div>
  `
};

export default {
  CondaButton,
  CondaModal,
  CondaTabs,
  CondaTab,
  CondaInput
};
</script>
