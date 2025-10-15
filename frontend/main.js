const { app, BrowserWindow } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    title: 'LUNA',
    icon: 'assets/luna.ico',
    webPreferences: {
      nodeIntegration: false
    }
  });
  win.loadURL('http://127.0.0.1:5000');
}

app.whenReady().then(createWindow);
