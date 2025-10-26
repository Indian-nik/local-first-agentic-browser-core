import { useState } from 'react';
import DOMPurify from 'dompurify';

function ComponentsPage() {
  const [selectedComponent, setSelectedComponent] = useState(null);

  const components = [
    {
      name: 'Button',
      description: 'Versatile button component with multiple variants',
      code: '<button class="conda-btn conda-btn-primary">Primary Button</button>'
    },
    {
      name: 'Card',
      description: 'Container for content with optional header and footer',
      code: '<div class="conda-card"><h3>Card Title</h3><p>Card content goes here</p></div>'
    },
    {
      name: 'Input',
      description: 'Form input with validation states',
      code: '<input type="text" class="conda-input" placeholder="Enter text">'
    },
    {
      name: 'Badge',
      description: 'Small status indicator',
      code: '<span class="conda-badge conda-badge-success">Active</span>'
    },
    {
      name: 'Alert',
      description: 'Notification message component',
      code: '<div class="conda-alert conda-alert-info">This is an informational message</div>'
    }
  ];

  return (
    <div className="conda-page">
      <div className="conda-page-header">
        <h1>🧩 Component Library</h1>
        <p>Explore all CONDA UI components</p>
      </div>

      <div className="components-grid">
        {components.map((component, index) => (
          <div
            key={index}
            className="component-card"
            onClick={() => setSelectedComponent(component)}
          >
            <h3>{component.name}</h3>
            <p>{component.description}</p>
            <div 
              className="component-preview"
              dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(component.code) }}
            />
          </div>
        ))}
      </div>

      {selectedComponent && (
        <div className="component-modal" onClick={() => setSelectedComponent(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>{selectedComponent.name}</h2>
            <p>{selectedComponent.description}</p>
            <div className="code-block">
              <pre>{selectedComponent.code}</pre>
            </div>
            <div 
              className="component-preview-large"
              dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(selectedComponent.code) }}
            />
            <button className="conda-btn" onClick={() => setSelectedComponent(null)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ComponentsPage;
