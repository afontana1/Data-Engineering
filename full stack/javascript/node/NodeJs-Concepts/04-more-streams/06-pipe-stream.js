const fs = require("fs");
const fileName = "./assets/surfing_waves.mp4";

const readStream = fs.createReadStream(fileName);
const writeStream = fs.createWriteStream("./06----copy.mp4");

readStream
  .pipe("writeStream")
  .on("error", err => {
    console.error("error occurred", err.message);
  })
