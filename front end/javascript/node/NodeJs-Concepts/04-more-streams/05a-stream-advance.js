// we can think on STREAMS as Water and Buckets
// it is also the way most of the option and action called :
// like 'drained' for stop pressure and 'highWaterMark' for bytes limit

const { createWriteStream, createReadStream } = require("fs");
const readStream = createReadStream("./assets/surfing_waves.mp4");
const writeStream = createWriteStream("./05----copy.mp4", {
  highWaterMark: 162854645
});

readStream.on("data", chunk => {
  // WRITE IN STREAM :
  const result = writeStream.write(chunk);
  // handle errors :
  if (!result) {
    console.log("we have '*water pressure*', we can't stream");
    readStream.pause();
  }
});

readStream.on("drain", () => {
  console.log(" pressure realesed -  'dreined' ");
  readStream.resume();
});

readStream.on("error", err => {
  console.error("error occurred", err.message);
});

readStream.on("end", () => {
  writeStream.end();
});

// write stream listerners :
writeStream.on("close", () => {
  process.stdout.write("\nfile copied");
  process.stdout.write("\n========");
});
