// preload.js

// All the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.

// const { contextBridge, ipcRenderer } = require('electron');
// const path = require('path');

// contextBridge.exposeInMainWorld('electronAPI', {
//     path: path,
//     // require: require
// });
// Expose certain APIs to the renderer process

window.addEventListener('DOMContentLoaded', () => {
    const replaceText = (selector, text) => {
      const element = document.getElementById(selector)
      if (element) element.innerText = text
    }
  
    for (const dependency of ['chrome', 'node', 'electron']) {
      replaceText(`${dependency}-version`, process.versions[dependency])
    }
  })