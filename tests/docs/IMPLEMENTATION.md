# CONDA Design System - Implementation Guide

## 🐍 Overview

CONDA is a modern, playful UI/UX design system inspired by the adaptability and fluid nature of anacondas. This guide provides comprehensive instructions for implementing and using the CONDA design system.

## 📁 Project Structure

```
conda-app/
├── src/
│   ├── components/        # Reusable UI components
│   ├── styles/           # Design system CSS
│   │   └── conda-design-system.css
│   ├── assets/           # SVG logos and images
│   │   ├── logo-primary.svg
│   │   └── logo-icon.svg
│   └── utils/            # Utility functions
├── public/               # Static files
│   └── index.html        # Main landing page
└── docs/                 # Documentation
    └── IMPLEMENTATION.md # This file
```

## 🎨 Design System Colors

### Primary Palette (Anaconda-inspired Greens)
- `--conda-primary: #43B02A` - Main brand color
- `--conda-primary-dark: #2E7D1E` - Darker variant
- `--conda-primary-light: #6FCF52` - Lighter variant
- `--conda-primary-pale: #E8F6E3` - Very light background

### Secondary Palette (Complementary Blues)
- `--conda-secondary: #0D7A8A` - Secondary brand color
- `--conda-secondary-dark: #075E6B` - Darker variant
- `--conda-secondary-light: #1BA1B5` - Lighter variant

### Accent Colors (Playful Highlights)
- `--conda-accent-orange: #FF6B35`
- `--conda-accent-purple: #8B5CF6`
- `--conda-accent-yellow: #FFD93D`
- `--conda-accent-pink: #F72585`

## 🔧 Getting Started

### 1. Installation

```bash
# Clone or download the project
git clone <repository-url>
cd conda-app

# No build step required - pure HTML/CSS
# Simply open public/index.html in a browser
```

### 2. Development Setup

For local development with live reload:

```bash
# Option 1: Using Python's built-in server
python -m http.server 8000

# Option 2: Using Node.js http-server
npx http-server -p 8000

# Option 3: Using VS Code Live Server extension
# Right-click index.html -> Open with Live Server
```

### 3. Using the Design System

Include the design system CSS in your HTML:

```html
<link rel="stylesheet" href="../src/styles/conda-design-system.css">
```

## 🧩 Component Usage

### Buttons

```html
<!-- Primary Button -->
<button class="conda-button conda-button-primary">
  Primary Action
</button>

<!-- Secondary Button -->
<button class="conda-button conda-button-secondary">
  Secondary Action
</button>

<!-- Outline Button -->
<button class="conda-button conda-button-outline">
  Outline Action
</button>

<!-- Ghost Button -->
<button class="conda-button conda-button-ghost">
  Ghost Action
</button>

<!-- Button Sizes -->
<button class="conda-button conda-button-primary conda-button-sm">Small</button>
<button class="conda-button conda-button-primary">Default</button>
<button class="conda-button conda-button-primary conda-button-lg">Large</button>
<button class="conda-button conda-button-primary conda-button-xl">Extra Large</button>
```

### Cards

```html
<div class="conda-card">
  <div class="conda-card-header">
    <h3 class="conda-card-title">Card Title</h3>
    <p class="conda-card-subtitle">Card subtitle or description</p>
  </div>
  <div class="conda-card-content">
    <p>Main card content goes here...</p>
  </div>
  <div class="conda-card-footer">
    <span class="conda-badge conda-badge-primary">Badge</span>
    <button class="conda-button conda-button-sm conda-button-ghost">Action</button>
  </div>
</div>
```

### Badges

```html
<span class="conda-badge conda-badge-primary">Primary</span>
<span class="conda-badge conda-badge-success">Success</span>
<span class="conda-badge conda-badge-warning">Warning</span>
<span class="conda-badge conda-badge-error">Error</span>
```

### Grid System

```html
<div class="conda-container">
  <div class="conda-grid conda-grid-cols-3">
    <div>Column 1</div>
    <div>Column 2</div>
    <div>Column 3</div>
  </div>
</div>
```

## ✨ Animations

The design system includes several built-in animations:

### Anaconda Coil Animation
```html
<img src="logo.svg" class="animate-coil">
```

### Slide Animations
```html
<div class="animate-slide-up">Slides up on load</div>
<div class="animate-slide-in-right">Slides in from right</div>
```

### Other Animations
```html
<div class="animate-fade-in">Fades in</div>
<div class="animate-bounce">Bounces continuously</div>
<button class="animate-pulse-glow">Pulsing glow effect</button>
```

## 🎭 Typography

### Font Families
- **Primary**: Inter (body text, UI elements)
- **Display**: Poppins (headings, hero text)
- **Monospace**: Fira Code (code, terminal)

### Headings
```html
<h1>H1 - 48px (3rem)</h1>
<h2>H2 - 36px (2.25rem)</h2>
<h3>H3 - 30px (1.875rem)</h3>
<h4>H4 - 24px (1.5rem)</h4>
<h5>H5 - 20px (1.25rem)</h5>
<h6>H6 - 18px (1.125rem)</h6>
```

## 🔌 Utility Classes

### Layout
```html
<div class="flex items-center justify-between">
  Flex container with centered items and space between
</div>

<div class="flex-col gap-4">
  Flex column with gap
</div>
```

### Spacing
```html
<div class="mt-4 mb-8">Margin top 16px, bottom 32px</div>
<div class="p-6">Padding 24px all sides</div>
```

### Text Alignment
```html
<div class="text-center">Centered text</div>
<div class="text-left">Left-aligned text</div>
<div class="text-right">Right-aligned text</div>
```

## 🌐 Responsive Design

The design system is mobile-first and responsive:

- Grids automatically collapse to single column on mobile (<768px)
- Typography scales appropriately
- Spacing adjusts for smaller screens

## 🎨 Customization

### Overriding CSS Variables

Customize the design system by overriding CSS custom properties:

```css
:root {
  --conda-primary: #YOUR_COLOR;
  --conda-secondary: #YOUR_COLOR;
  /* Override any variable */
}
```

### Creating Custom Components

Extend the design system with your own components:

```css
.my-custom-component {
  background: var(--conda-primary);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
}
```

## ♿ Accessibility

The CONDA design system follows WCAG 2.1 Level AA guidelines:

- ✅ Color contrast ratios meet AA standards
- ✅ Focus states clearly visible
- ✅ Semantic HTML structure
- ✅ ARIA labels where appropriate
- ✅ Keyboard navigation supported

### Testing Accessibility

```bash
# Use Lighthouse in Chrome DevTools
# Or install axe DevTools extension
```

## 🚀 Performance

### Optimization Tips

1. **CSS is already minified-ready** - No external dependencies
2. **SVG logos are optimized** - Small file sizes
3. **No JavaScript required** - Pure CSS animations
4. **Web fonts loaded efficiently** - Preconnect hints included

### Production Deployment

```bash
# Minify CSS (optional)
npx cssnano src/styles/conda-design-system.css public/styles.min.css

# Optimize SVGs
npx svgo src/assets/*.svg

# Deploy to static hosting
# Netlify, Vercel, GitHub Pages, etc.
```

## 🐛 Troubleshooting

### Common Issues

**1. Fonts not loading**
- Ensure Google Fonts link is in `<head>`
- Check browser console for CORS errors

**2. Animations not working**
- Verify CSS file is properly linked
- Check for conflicting CSS rules

**3. SVG logos not displaying**
- Verify file paths are correct
- Ensure SVG files are in `src/assets/`

## 📚 Additional Resources

- [Design System Documentation](./DESIGN_SYSTEM.md)
- [Component Library](./COMPONENTS.md)
- [Style Guide](./STYLE_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please:

1. Follow the existing code style
2. Test across browsers (Chrome, Firefox, Safari, Edge)
3. Ensure accessibility standards are met
4. Document new components or changes

## 📄 License

MIT License - Feel free to use in your projects!

---

**Built with 💚 by the CONDA Team**

For questions or support, visit [CONDA Community](https://conda.community)
