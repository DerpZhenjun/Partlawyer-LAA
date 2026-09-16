const { app, BrowserWindow, shell } = require('electron')
const fs = require('node:fs')
const http = require('node:http')
const path = require('node:path')

const isDev = !app.isPackaged
let staticServer

function startStaticServer() {
  const webRoot = path.resolve(process.resourcesPath, 'web')
  const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg' }
  return new Promise((resolve, reject) => {
    staticServer = http.createServer((req, res) => {
      const pathname = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname)
      const requested = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '')
      let filePath = path.resolve(webRoot, requested)
      if (!filePath.startsWith(webRoot)) { res.writeHead(403); return res.end('Forbidden') }
      if (!path.extname(filePath) || !fs.existsSync(filePath)) filePath = path.join(webRoot, 'index.html')
      fs.readFile(filePath, (error, data) => {
        if (error) { res.writeHead(404); return res.end('Not found') }
        res.writeHead(200, { 'Content-Type': mime[path.extname(filePath)] || 'application/octet-stream', 'X-Content-Type-Options': 'nosniff', 'Cache-Control': path.extname(filePath) === '.html' ? 'no-cache' : 'public, max-age=31536000, immutable' })
        res.end(data)
      })
    })
    staticServer.once('error', reject)
    staticServer.listen(0, '127.0.0.1', () => resolve(`http://127.0.0.1:${staticServer.address().port}`))
  })
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1080,
    minHeight: 700,
    show: false,
    backgroundColor: '#f3f6f9',
    title: 'LabourLawyer · 劳动仲裁文书助手',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  })

  win.once('ready-to-show', () => win.show())
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:/.test(url)) shell.openExternal(url)
    return { action: 'deny' }
  })
  if (isDev) {
    const devUrl = process.env.LABOURLAWYER_DEV_URL || 'http://127.0.0.1:5173'
    win.webContents.on('will-navigate', (event, url) => { if (!url.startsWith(devUrl)) event.preventDefault() })
    await win.loadURL(devUrl)
  } else {
    const appUrl = staticServer ? `http://127.0.0.1:${staticServer.address().port}` : await startStaticServer()
    win.webContents.on('will-navigate', (event, url) => { if (!url.startsWith(appUrl)) event.preventDefault() })
    await win.loadURL(appUrl)
  }
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow() })
})
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
app.on('before-quit', () => staticServer?.close())
