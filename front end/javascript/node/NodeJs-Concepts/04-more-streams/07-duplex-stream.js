// DUPLEX :
// gets the pipe on the middle and do something
//

const fs = require("fs");
const stream = require("stream");
const fileNames = {
  source: "./assets/surfing_waves.mp4",
  des: "./07----copy.mp4"
};

const readStream = fs.createReadStream(fileNames.source);
const writeStream = fs.createWriteStream(fileNames.des);


// DUPLEX (PassThrough) of Report
const report = new stream.PassThrough();
readStream.pipe(report).pipe(writeStream);

// function to show the report
let total = 0;
// on PassThrough ->
report.on("data", chunk => {
  total += chunk.length;
  console.log("bytes: ", total);
});
