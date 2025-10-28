# CONDA Desktop Application

Cross-platform desktop application for the CONDA Design System.

## Features

- 🖥️ Native desktop app for Windows, macOS, and Linux
- 🎨 Complete design system showcase
- 🧩 20+ interactive components
- 🎮 Built-in code playground
- 🌈 Visual theme editor
- 📚 Comprehensive documentation

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# In another terminal, run Electron
npm run electron:dev
```

## Building

```bash
# Build for current platform
npm run build
npm run electron:build

# Build for all platforms
npm run build:all
```

## Project Structure

```
conda-desktop/
├── src/
│   ├── main/           # Electron main process
│   ├── preload/        # Preload scripts
│   └── renderer/       # React app
│       ├── components/
│       ├── pages/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
├── public/
│   └── index.html
├── build/              # App icons
├── package.json
└── vite.config.js
```

## Technology Stack

- **Electron**: Cross-platform desktop framework
- **React**: UI library
- **React Router**: Client-side routing
- **Vite**: Build tool and dev server
- **electron-builder**: Installer creation

