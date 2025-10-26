import { useState } from 'react';
import DOMPurify from 'dompurify';

function PlaygroundPage() {
  const [htmlCode, setHtmlCode] = useState('<div class="conda-card">\n  <h3>Sample Card</h3>\n  <p>Edit the code to see changes!</p>\n</div>');
  const [cssCode, setCssCode] = useState('.conda-card {\n  padding: 20px;\n  border-radius: 8px;\n  background: var(--conda-bg-secondary);\n}');

  return (
    <div className="conda-page">
      <div className="conda-page-header">
        <h1>🎮 Interactive Playground</h1>
        <p>Experiment with CONDA components in real-time</p>
      </div>

      <div className="playground-container">
        <div className="playground-editors">
          <div className="playground-editor">
            <div className="editor-header">
              <span className="editor-label">HTML</span>
            </div>
            <textarea
              className="code-editor"
              value={htmlCode}
              onChange={(e) => setHtmlCode(e.target.value)}
              spellCheck="false"
            />
          </div>

          <div className="playground-editor">
            <div className="editor-header">
              <span className="editor-label">CSS</span>
            </div>
            <textarea
              className="code-editor"
              value={cssCode}
              onChange={(e) => setCssCode(e.target.value)}
              spellCheck="false"
            />
          </div>
        </div>

        <div className="playground-preview">
          <div className="preview-header">
            <span className="preview-label">Preview</span>
          </div>
          <div className="preview-content">
            <style>{cssCode}</style>
            <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(htmlCode) }} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default PlaygroundPage;
