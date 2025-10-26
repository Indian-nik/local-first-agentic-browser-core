// ============================================
// CONDA React Components Library
// Modern React components for CONDA Design System
// ============================================

import React, { useState, useEffect, useRef, createContext, useContext } from 'react';

// ========== BUTTON COMPONENT ==========
export const CondaButton = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  type = 'button',
  className = '',
  ...props
}) => {
  const classes = `conda-button conda-button-${variant} conda-button-${size} ${className}`;
  
  return (
    <button
      type={type}
      className={classes}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

// ========== CARD COMPONENT ==========
export const CondaCard = ({
  children,
  variant = 'default',
  interactive = false,
  elevated = false,
  className = '',
  ...props
}) => {
  const classes = `conda-card ${
    elevated ? 'conda-card-elevated' : ''
  } ${
    interactive ? 'conda-card-interactive' : ''
  } ${className}`;
  
  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

// ========== BADGE COMPONENT ==========
export const CondaBadge = ({
  children,
  variant = 'primary',
  className = '',
  ...props
}) => {
  return (
    <span className={`conda-badge conda-badge-${variant} ${className}`} {...props}>
      {children}
    </span>
  );
};

// ========== MODAL COMPONENT ==========
export const CondaModal = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = 'medium',
  closeOnOverlay = true,
  closeOnEsc = true,
  showClose = true
}) => {
  const modalRef = useRef(null);
  
  useEffect(() => {
    if (closeOnEsc) {
      const handleEscape = (e) => {
        if (e.key === 'Escape' && isOpen) {
          onClose();
        }
      };
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [closeOnEsc, isOpen, onClose]);
  
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  const handleOverlayClick = (e) => {
    if (closeOnOverlay && e.target === e.currentTarget) {
      onClose();
    }
  };
  
  return (
    <div className={`conda-modal-overlay ${isOpen ? 'active' : ''}`} onClick={handleOverlayClick}>
      <div className={`conda-modal conda-modal-${size}`} ref={modalRef} role="dialog" aria-modal="true">
        <div className="conda-modal-header">
          <h2 className="conda-modal-title">{title}</h2>
          {showClose && (
            <button
              className="conda-modal-close"
              onClick={onClose}
              aria-label="Close modal"
            >
              &times;
            </button>
          )}
        </div>
        <div className="conda-modal-body">
          {children}
        </div>
        {footer && (
          <div className="conda-modal-footer">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};

// ========== TABS COMPONENT ==========
export const CondaTabs = ({ children, defaultTab = 0, onChange }) => {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  const handleTabChange = (index) => {
    setActiveTab(index);
    if (onChange) onChange(index);
  };
  
  const tabs = React.Children.toArray(children);
  
  return (
    <div className="conda-tabs">
      <div className="conda-tabs-nav" role="tablist">
        {tabs.map((tab, index) => (
          <button
            key={index}
            className={`conda-tab-button ${index === activeTab ? 'active' : ''}`}
            onClick={() => handleTabChange(index)}
            role="tab"
            aria-selected={index === activeTab}
            aria-controls={`conda-tab-panel-${index}`}
          >
            {tab.props.icon && <span className="conda-tab-icon">{tab.props.icon}</span>}
            {tab.props.label}
          </button>
        ))}
      </div>
      {tabs.map((tab, index) => (
        <div
          key={index}
          className={`conda-tab-content ${index === activeTab ? 'active' : ''}`}
          role="tabpanel"
          id={`conda-tab-panel-${index}`}
          hidden={index !== activeTab}
        >
          {tab.props.children}
        </div>
      ))}
    </div>
  );
};

export const CondaTab = ({ label, icon, children }) => {
  return <>{children}</>;
};

// ========== FORM COMPONENTS ==========
export const CondaInput = ({
  label,
  error,
  success,
  helpText,
  required = false,
  className = '',
  ...props
}) => {
  const inputClass = `conda-form-input ${
    error ? 'error' : ''
  } ${
    success ? 'success' : ''
  } ${className}`;
  
  return (
    <div className="conda-form-group">
      {label && (
        <label className={`conda-form-label ${required ? 'required' : ''}`}>
          {label}
        </label>
      )}
      <input className={inputClass} {...props} />
      {helpText && <span className="conda-form-help">{helpText}</span>}
      {error && <span className="conda-form-error">{error}</span>}
      {success && <span className="conda-form-success">{success}</span>}
    </div>
  );
};

export const CondaTextarea = ({
  label,
  error,
  helpText,
  required = false,
  className = '',
  ...props
}) => {
  return (
    <div className="conda-form-group">
      {label && (
        <label className={`conda-form-label ${required ? 'required' : ''}`}>
          {label}
        </label>
      )}
      <textarea
        className={`conda-form-input conda-form-textarea ${error ? 'error' : ''} ${className}`}
        {...props}
      />
      {helpText && <span className="conda-form-help">{helpText}</span>}
      {error && <span className="conda-form-error">{error}</span>}
    </div>
  );
};

export const CondaSelect = ({
  label,
  options,
  error,
  helpText,
  required = false,
  className = '',
  ...props
}) => {
  return (
    <div className="conda-form-group">
      {label && (
        <label className={`conda-form-label ${required ? 'required' : ''}`}>
          {label}
        </label>
      )}
      <select
        className={`conda-form-input conda-form-select ${error ? 'error' : ''} ${className}`}
        {...props}
      >
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {helpText && <span className="conda-form-help">{helpText}</span>}
      {error && <span className="conda-form-error">{error}</span>}
    </div>
  );
};

// ========== NAVIGATION COMPONENT ==========
export const CondaNav = ({ logo, items, sticky = false }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState(null);
  
  return (
    <nav className={`conda-nav ${sticky ? 'conda-nav-sticky' : ''}`} role="navigation">
      <div className="conda-nav-container">
        {logo && (
          <a href={logo.href || '#'} className="conda-nav-logo">
            {logo.text}
          </a>
        )}
        
        <button
          className={`conda-nav-toggle ${isOpen ? 'active' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
          aria-expanded={isOpen}
        >
          <span className="conda-nav-toggle-icon"></span>
          <span className="conda-nav-toggle-icon"></span>
          <span className="conda-nav-toggle-icon"></span>
        </button>
        
        <ul className={`conda-nav-menu ${isOpen ? 'active' : ''}`} role="menubar">
          {items.map((item, index) => (
            <li
              key={index}
              className={`conda-nav-item ${
                item.dropdown ? 'conda-nav-item-dropdown' : ''
              } ${
                activeDropdown === index ? 'active' : ''
              }`}
              role="none"
            >
              {item.dropdown ? (
                <>
                  <button
                    className="conda-nav-link"
                    onClick={() => setActiveDropdown(activeDropdown === index ? null : index)}
                    role="menuitem"
                    aria-haspopup="true"
                    aria-expanded={activeDropdown === index}
                  >
                    {item.label} <span className="conda-nav-dropdown-arrow">▼</span>
                  </button>
                  <ul className="conda-nav-dropdown" role="menu">
                    {item.dropdown.map((subItem, subIndex) => (
                      <li key={subIndex} role="none">
                        <a
                          href={subItem.href || '#'}
                          className="conda-nav-dropdown-item"
                          role="menuitem"
                        >
                          {subItem.icon && <span className="conda-nav-icon">{subItem.icon}</span>}
                          {subItem.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                </>
              ) : (
                <a
                  href={item.href || '#'}
                  className={`conda-nav-link ${item.active ? 'active' : ''}`}
                  role="menuitem"
                >
                  {item.icon && <span className="conda-nav-icon">{item.icon}</span>}
                  {item.label}
                </a>
              )}
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

// ========== THEME PROVIDER ==========
const ThemeContext = createContext();

export const CondaThemeProvider = ({ children, defaultTheme = 'default' }) => {
  const [theme, setTheme] = useState(defaultTheme);
  
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useCondaTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useCondaTheme must be used within CondaThemeProvider');
  }
  return context;
};

// Export all components
export default {
  Button: CondaButton,
  Card: CondaCard,
  Badge: CondaBadge,
  Modal: CondaModal,
  Tabs: CondaTabs,
  Tab: CondaTab,
  Input: CondaInput,
  Textarea: CondaTextarea,
  Select: CondaSelect,
  Nav: CondaNav,
  ThemeProvider: CondaThemeProvider,
  useTheme: useCondaTheme
};
