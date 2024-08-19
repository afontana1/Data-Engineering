// imports :
const { createServer } = require("http");
const { promisify } = require("util");
const fs = require("fs"); // use for stat and readStream
// the file
const fileInfo = promisify(fs.stat);
const video = "../assets/surfing_waves.mp4";

createServer(async (req, res) => {
  const { size } = await fileInfo(video);
  const { range } = req.headers;
  // range req ::
  if (range) {
    // we get 'bytes= start - end', so we cut it :
    let [start, end] = range.replace(/bytes/, "").split("-");
    start = parseInt(start, 10); // base 10
    end = end ? parseInt(end, 10) : size - 1;
    res.writeHead(206, {
      // 206 = partial content
      "Content-Range": `bytes ${start} - ${end} / ${size}`,
      "Accept-Ranges": "bytes",
      "content-Type": "video/mp4",
      "content-Length": end - start + 1
    });
  }
  // not range request
  else {
    res.writeHead(200, { "content-Type": "video/mp4", "content-Length": size });
  }
  fs.createReadStream(video, {start, end}).pipe(res);
}).listen(3000, () => console.log(`server is running at port 3000`));
