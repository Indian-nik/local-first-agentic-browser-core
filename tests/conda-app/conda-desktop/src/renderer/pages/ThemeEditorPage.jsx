import React, { useState } from 'react';

function ThemeEditorPage({ onThemeChange }) {
  const [customColors, setCustomColors] = useState({
    primary: '#00d4ff',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8'
  });

  const handleColorChange = (key, value) => {
    setCustomColors(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="theme-editor-page">
      <header className="page-header">
        <h1>Theme Editor</h1>
        <p>Customize your design system colors and styles</p>
      </header>

      <div className="theme-editor-layout">
        <div className="color-controls">
          <h3>Color Palette</h3>
          {Object.entries(customColors).map(([key, value]) => (
            <div key={key} className="color-control">
              <label>
                {key.charAt(0).toUpperCase() + key.slice(1)}
                <input
                  type="color"
                  value={value}
                  onChange={(e) => handleColorChange(key, e.target.value)}
                />
                <span className="color-value">{value}</span>
              </label>
            </div>
          ))}
          <button className="btn btn-primary">Apply Theme</button>
          <button className="btn btn-secondary">Export CSS</button>
        </div>

        <div className="theme-preview">
          <h3>Preview</h3>
          <div className="preview-content" style={{ '--primary-color': customColors.primary }}>
            <button className="btn btn-primary">Primary Button</button>
            <button className="btn btn-secondary">Secondary Button</button>
            <div className="card">
              <h4>Sample Card</h4>
              <p>This is how your theme will look</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ThemeEditorPage;
