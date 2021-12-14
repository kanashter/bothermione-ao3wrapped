const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  window = new BrowserWindow({
    width: 1280,
    height: 800,
    frame: true,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  window.loadFile("public/index.html");
};

let window = null;

const fileLoc = __dirname + "\\ao3_flaskserver\\ao3.exe";
var subpy = require("child_process").execFile(fileLoc);

app.whenReady().then(createWindow);
app.on("window-all-closed", () => app.quit());
