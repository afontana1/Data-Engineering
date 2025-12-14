// imports : 
const { createServer } = require("http");
const fs = require("fs"); // use for stat and readStream
const {promisify } = require('util')
// the file
const fileInfo = promisify(fs.stat)
const video = "../assets/surfing_waves.mp4";


createServer(async(req, res) => {
   const {size} = await fileInfo(video)
  res.writeHead(200, { "content-Type": "video/mp4" , 'content-Length' : size});
  fs.createReadStream(video).pipe(res);
}).listen(3000, () =>
  console.log(`server is running at port 3000`)
);


