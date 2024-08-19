const express = require('express');
const httpProxy = require('http-proxy');
const ProxyChain = require('proxy-chain');

const app = express();
const proxy = httpProxy.createProxyServer({});

const proxyUrl = 'http://your-proxy-provider-url'; // Replace with the actual proxy provider's URL
const port = 3000;

app.use(async (req, res) => {
  try {
    // Get a new proxy URL for each request
    const newProxyUrl = await ProxyChain.anonymizeProxy(proxyUrl);

    console.log(`Routing request through proxy: ${newProxyUrl}`);

    // Proxy the request to the destination using the new proxy
    proxy.web(req, res, {
      target: req.url,
      changeOrigin: true,
      headers: { host: newProxyUrl.host },
      agent: newProxyUrl.protocol === 'https:' ? httpsGlobalAgent : httpGlobalAgent,
    });
  } catch (error) {
    console.error(`Error while processing request: ${error.message}`);
    res.status(500).send('Internal Server Error');
  }
});

app.listen(port, () => {
  console.log(`Rotating Proxy Server listening on port ${port}`);
});
