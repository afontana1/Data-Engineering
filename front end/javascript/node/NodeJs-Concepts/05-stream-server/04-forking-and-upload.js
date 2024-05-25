// imports :
const { createServer } = require("http");
const { promisify } = require("util");
const fs = require("fs"); // use for stat and readStream
// the file
const fileInfo = promisify(fs.stat);
const video = "../assets/surfing_waves.mp4";

// THE REGULAR STAFF
const resWithVid = async (req, res) => {
  const { size } = await fileInfo(video);
  const { range } = req.headers;
  // range req ::
  if (range) {
    // we get 'bytes= start - end', so we cut it :
    let [start, end] = range.replace(/bytes/, "").split("-");
    console.log(start, "start");

    start = parseInt(start, 10) || 0; // base 10
    end = end ? parseInt(end, 10) : size - 1;
    res.writeHead(206, {
      // 206 = partial content
      "Content-Range": `bytes ${start} - ${end} / ${size}`,
      "Accept-Ranges": "bytes",
      "content-Length": end - start + 1,
      "content-Type": "video/mp4"
    });
    fs.createReadStream(video, { start, end }).pipe(res);
  }
  // not range request
  else {
    res.writeHead(200, { "content-Type": "video/mp4", "content-Length": size });
    fs.createReadStream(video).pipe(res);
  }
};

//// ::::::::::::::::::
// NEW
// CREATE UPLOAD :::
createServer((req, res) => {
  console.log(req.method);
  if (req.method === "POST") {
    req.pipe(res);
    req.pipe(fs.createWriteStream("../assets/upload.txt"));
  } else if (req.url === "/video") {
    resWithVid(req, res);
  } else {
    // HOME PAGE : url === '/'
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(`
    </br></br></br></br></br>
          <form enctype="multipart/form-data" method="POST" action="/" style="display:flex; align-items:center; justify-content: center; text-align: center">
            <input type="file" name="upload-file" />
            <button> Upload File </button>
          </form>
          `);
  }
}).listen(3000, () => console.log(`server is running at port 3000`));
