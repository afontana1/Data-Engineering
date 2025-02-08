const fs = require("fs");
const {PassThrough , Duplex} = require("stream");
// defines 
const fileNames = { source: "./assets/surfing_waves.mp4", des: "./07----copy.mp4" };
const readStream = fs.createReadStream(fileNames.source);
const writeStream = fs.createWriteStream(fileNames.des);
// ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
// ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

// DUPLEX :
// self class --- readable and writeable 
class Throttle extends Duplex {
  constructor(ms) {
    super();
    this.delay = ms;
  }

  _write(chunk, encodingF,cb) {
    this.push(chunk);
    setTimeout(cb, this.delay);
  }

  _read() {}

  _final() {
    this.push(null);
  }
}

// gets the pipe on the middle and do something
const report = new PassThrough();
const throttle = new Throttle(100);

// create STREAM
readStream
  .pipe(throttle)
  .pipe(report)
  .pipe(writeStream);


// function to show the report
  let total = 0;
report.on("data", chunk => {
  total += chunk.length;
  console.log("bytes: ", total);
});
