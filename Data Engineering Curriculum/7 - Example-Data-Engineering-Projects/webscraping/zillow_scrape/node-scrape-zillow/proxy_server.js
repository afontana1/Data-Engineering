const express = require('express');
const httpProxy = require('http-proxy');

const app = express();
const proxy = httpProxy.createProxyServer();

const proxyList = [
  'http://proxy1:port',
  'http://proxy2:port',
  // Add more proxy URLs as needed
];

let currentProxyIndex = 0;

app.use((req, res) => {
  // Get the next proxy in the list
  const currentProxy = proxyList[currentProxyIndex];
  // Rotate to the next proxy for the next request
  currentProxyIndex = (currentProxyIndex + 1) % proxyList.length;

  console.log(`Routing request through proxy: ${currentProxy}`);

  // Proxy the request to the destination using the current proxy
  proxy.web(req, res, { target: req.url, changeOrigin: true, target: currentProxy });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Rotating Proxy Server listening on port ${port}`);
});
