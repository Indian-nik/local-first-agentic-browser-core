// ============================================
// CONDA Web Components (Custom Elements)
// Framework-agnostic reusable components
// ============================================

// Button Component
class CondaButtonElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  
  connectedCallback() {
    const variant = this.getAttribute('variant') || 'primary';
    const size = this.getAttribute('size') || 'medium';
    const disabled = this.hasAttribute('disabled');
    
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="../../src/styles/conda-design-system.css">
      <button class="conda-button conda-button-${variant} conda-button-${size}" ${disabled ? 'disabled' : ''}>
        <slot></slot>
      </button>
    `;
    
    this.shadowRoot.querySelector('button').addEventListener('click', (e) => {
      this.dispatchEvent(new CustomEvent('conda-click', { detail: e, bubbles: true }));
    });
  }
}

// Modal Component
class CondaModalElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  
  connectedCallback() {
    this.render();
    this.attachEvents();
  }
  
  render() {
    const title = this.getAttribute('title') || 'Modal';
    const size = this.getAttribute('size') || 'medium';
    const isOpen = this.hasAttribute('open');
    
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="../../src/styles/conda-design-system.css">
      <link rel="stylesheet" href="../../src/styles/components.css">
      <div class="conda-modal-overlay ${isOpen ? 'active' : ''}">
        <div class="conda-modal conda-modal-${size}" role="dialog">
          <div class="conda-modal-header">
            <h2 class="conda-modal-title">${title}</h2>
            <button class="conda-modal-close">&times;</button>
          </div>
          <div class="conda-modal-body">
            <slot></slot>
          </div>
          <div class="conda-modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    `;
  }
  
  attachEvents() {
    const closeBtn = this.shadowRoot.querySelector('.conda-modal-close');
    const overlay = this.shadowRoot.querySelector('.conda-modal-overlay');
    
    closeBtn?.addEventListener('click', () => this.close());
    overlay?.addEventListener('click', (e) => {
      if (e.target === overlay) this.close();
    });
  }
  
  open() {
    this.setAttribute('open', '');
    this.shadowRoot.querySelector('.conda-modal-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  
  close() {
    this.removeAttribute('open');
    this.shadowRoot.querySelector('.conda-modal-overlay').classList.remove('active');
    document.body.style.overflow = '';
    this.dispatchEvent(new CustomEvent('conda-close', { bubbles: true }));
  }
}

// Tabs Component
class CondaTabsElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open'});
    this.activeTab = 0;
  }
  
  connectedCallback() {
    this.render();
    this.attachEvents();
  }
  
  render() {
    const tabs = Array.from(this.querySelectorAll('conda-tab'));
    
    this.shadowRoot.innerHTML = `
      <link rel="stylesheet" href="../../src/styles/conda-design-system.css">
      <link rel="stylesheet" href="../../src/styles/components.css">
      <div class="conda-tabs">
        <div class="conda-tabs-nav" role="tablist">
          ${tabs.map((tab, i) => `
            <button 
              class="conda-tab-button ${i === this.activeTab ? 'active' : ''}"
              data-index="${i}"
              role="tab"
            >
              ${tab.getAttribute('label')}
            </button>
          `).join('')}
        </div>
        <div class="tab-panels">
          <slot></slot>
        </div>
      </div>
    `;
  }
  
  attachEvents() {
    this.shadowRoot.querySelectorAll('.conda-tab-button').forEach((btn, index) => {
      btn.addEventListener('click', () => this.selectTab(index));
    });
  }
  
  selectTab(index) {
    this.activeTab = index;
    this.shadowRoot.querySelectorAll('.conda-tab-button').forEach((btn, i) => {
      btn.classList.toggle('active', i === index);
    });
    
    this.querySelectorAll('conda-tab').forEach((tab, i) => {
      tab.style.display = i === index ? 'block' : 'none';
    });
    
    this.dispatchEvent(new CustomEvent('conda-tab-change', { 
      detail: { index }, 
      bubbles: true 
    }));
  }
}

class CondaTabElement extends HTMLElement {
  constructor() {
    super();
  }
}

// Register all components
customElements.define('conda-button', CondaButtonElement);
customElements.define('conda-modal', CondaModalElement);
customElements.define('conda-tabs', CondaTabsElement);
customElements.define('conda-tab', CondaTabElement);

// Export for module use
export { CondaButtonElement, CondaModalElement, CondaTabsElement, CondaTabElement };
