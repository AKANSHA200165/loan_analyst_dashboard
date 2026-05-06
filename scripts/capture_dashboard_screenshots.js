const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const projectRoot = path.resolve(__dirname, "..");
const dashboardPath = path.join(projectRoot, "Power-BI-Dashboard", "loan_risk_dashboard.html");
const screenshotsDir = path.join(projectRoot, "screenshots");
const edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const port = 9223;

const captures = [
  { file: "dashboard_overview.png", scrollY: 0 },
  { file: "dashboard_charts.png", scrollY: 520 },
  { file: "dashboard_business_insights.png", scrollY: 1080 },
];

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getJson(url) {
  const response = await fetch(url);
  return response.json();
}

function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    const pending = new Map();
    let id = 1;

    ws.addEventListener("open", () => {
      resolve({
        send(method, params = {}) {
          const messageId = id++;
          ws.send(JSON.stringify({ id: messageId, method, params }));
          return new Promise((res, rej) => {
            pending.set(messageId, { res, rej });
          });
        },
        close() {
          ws.close();
        },
      });
    });

    ws.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (!message.id || !pending.has(message.id)) return;
      const { res, rej } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) {
        rej(new Error(message.error.message));
      } else {
        res(message.result);
      }
    });

    ws.addEventListener("error", reject);
  });
}

async function main() {
  fs.mkdirSync(screenshotsDir, { recursive: true });

  const browser = spawn(edgePath, [
    "--headless=new",
    "--disable-gpu",
    `--remote-debugging-port=${port}`,
    "--window-size=1645,900",
    `file:///${dashboardPath.replace(/\\/g, "/")}`,
  ]);

  try {
    await delay(1500);

    const pages = await getJson(`http://127.0.0.1:${port}/json`);
    const page = pages.find((item) => item.type === "page");
    if (!page) throw new Error("No browser page found for screenshot capture.");

    const client = await connect(page.webSocketDebuggerUrl);
    await client.send("Page.enable");
    await client.send("Runtime.evaluate", { expression: "document.fonts.ready" });

    for (const capture of captures) {
      await client.send("Runtime.evaluate", {
        expression: `window.scrollTo(0, ${capture.scrollY});`,
      });
      await delay(350);

      const result = await client.send("Page.captureScreenshot", {
        format: "png",
        fromSurface: true,
      });

      fs.writeFileSync(path.join(screenshotsDir, capture.file), Buffer.from(result.data, "base64"));
      console.log(`Saved ${capture.file}`);
    }

    client.close();
  } finally {
    browser.kill();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});

