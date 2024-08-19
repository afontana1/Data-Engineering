// imports : 
const { createServer } = require("http");
const fs = require("fs"); 
const {promisify } = require('util')
// the file
const video = "../assets/surfing_waves.mp4";


createServer(async(req, res) => {
  res.writeHead(200, { "content-Type": "video/mp4" });
  fs.createReadStream(video).pipe(res);
}).listen(3000, () =>
  console.log(`server is running at port 3000`)
);


