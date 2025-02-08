// HERE WE WILL TAKE FLOW STREAM AND MOVE INTO NON FLOW MODE

const fs = require("fs");
const txtStream = fs.createReadStream("./sample.txt");
const videoStream = fs.createReadStream("./assets/surfing_waves.mp4");
// EACH TIME
// we will use 1 of the above to see the diffrance
const someStream = videoStream; //txtStream

someStream.on("data", chunk => {
  console.log(chunk.length);
  console.log("press to see more");
});

// we take stream into non flow mode :
someStream.pause();

process.stdin.on("data", input => {
  // for each ENTER stroke we
  // will stream new data :
  // -->
  someStream.read();
  // some function to resume() stream:
  doSomethingElse(input);
});

function doSomethingElse(input) {
  const key = input
    .toString()
    .toLowerCase()
    .trim();
  if (key === "finish" || key === "e" || key === "exit") {
    // -->
    // back to flow mode :
    someStream.resume();
  }
}
