const fs = require("fs");
const videoStream = fs.createReadStream("./assets/surfing_waves.mp4");

let chunkCount = 0;
videoStream.on("data", chunk => {
  console.log(`reading chunk number ${chunkCount} of the file...`);
  chunkCount++;
  if (chunkCount > 471) {
      console.log(`size : ${chunk.length}`);
    }
});

videoStream.on("end", () => {
  console.log("read stream finished");
});

videoStream.on("error", error => {
  console.log("error occured");
  console.error(error.message);
});
