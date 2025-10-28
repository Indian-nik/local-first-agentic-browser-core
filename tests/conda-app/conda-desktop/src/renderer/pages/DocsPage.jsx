import React from 'react';

function DocsPage() {
  const sections = [
    {
      title: 'Getting Started',
      items: ['Installation', 'Quick Start', 'Configuration']
    },
    {
      title: 'Components',
      items: ['Buttons', 'Forms', 'Cards', 'Navigation', 'Modals']
    },
    {
      title: 'Theming',
      items: ['Color System', 'Typography', 'Spacing', 'Breakpoints']
    },
    {
      title: 'Advanced',
      items: ['Accessibility', 'Customization', 'API Reference']
    }
  ];

  return (
    <div className="docs-page">
      <header className="page-header">
        <h1>Documentation</h1>
        <p>Complete guide to using the CONDA Design System</p>
      </header>

      <div className="docs-layout">
        <aside className="docs-sidebar">
          {sections.map((section, index) => (
            <div key={index} className="docs-section">
              <h3>{section.title}</h3>
              <ul>
                {section.items.map((item, i) => (
                  <li key={i}>
                    <a href={`#${item.toLowerCase().replace(' ', '-')}`}>
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </aside>

        <div className="docs-content">
          <article>
            <h2>Welcome to CONDA Documentation</h2>
            <p>
              The CONDA Design System is a comprehensive UI toolkit that provides
              everything you need to build beautiful, accessible applications.
            </p>

            <h3>Key Features</h3>
            <ul>
              <li>20+ production-ready components</li>
              <li>9 pre-built themes with full customization</li>
              <li>WCAG 2.1 Level AA accessibility compliance</li>
              <li>Cross-platform desktop support</li>
              <li>Responsive design out of the box</li>
            </ul>

            <h3>Installation</h3>
            <pre><code>npm install conda-design-system</code></pre>

            <h3>Usage</h3>
            <pre><code>import 'conda-design-system/dist/styles.css';

// Use components
&lt;button className="btn btn-primary"&gt;Click me&lt;/button&gt;</code></pre>
          </article>
        </div>
      </div>
    </div>
  );
}

export default DocsPage;
