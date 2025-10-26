const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Platform info
  getPlatform: () => ipcRenderer.invoke('get-platform'),
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // Window controls
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  maximizeWindow: () => ipcRenderer.invoke('maximize-window'),
  closeWindow: () => ipcRenderer.invoke('close-window'),
  
  // File system operations (placeholder for future features)
  readFile: (path) => ipcRenderer.invoke('read-file', path),
  writeFile: (path, data) => ipcRenderer.invoke('write-file', path, data),
  
  // Theme persistence
  getStoredTheme: () => ipcRenderer.invoke('get-stored-theme'),
  setStoredTheme: (theme) => ipcRenderer.invoke('set-stored-theme', theme)
});

console.log('🔒 Preload script loaded - Context isolation enabled');
