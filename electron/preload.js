const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  wled: {
    toggle: (on) => ipcRenderer.invoke('wled:toggle', on),
    setBrightness: (brightness) => ipcRenderer.invoke('wled:setBrightness', brightness),
    setColor: (hexColor) => ipcRenderer.invoke('wled:setColor', hexColor),
    ping: () => ipcRenderer.invoke('wled:ping')
  },
  twinkle: {
    setBrightness: (brightness) => ipcRenderer.invoke('twinkle:setBrightness', brightness),
    ping: () => ipcRenderer.invoke('twinkle:ping')
  },
  data: {
    read: (type) => ipcRenderer.invoke('data:read', type),
    write: (type, data) => ipcRenderer.invoke('data:write', type, data)
  },
  onLuxUpdate: (callback) => {
    const subscription = (event, luxValue) => callback(luxValue);
    ipcRenderer.on('lux-update', subscription);
    return () => ipcRenderer.removeListener('lux-update', subscription);
  }
});
