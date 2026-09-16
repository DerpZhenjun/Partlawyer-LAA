const { contextBridge } = require('electron')

contextBridge.exposeInMainWorld('labourLawyerDesktop', Object.freeze({
  platform: process.platform,
  desktop: true,
  version: '1.0.0',
}))
