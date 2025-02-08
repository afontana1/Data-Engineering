const { createWriteStream } = require("fs");

const ws = createWriteStream("06----pipe-txt.txt");

console.log(summery());

// from user input into a file:
process.stdin.pipe(ws);

/// SUMMERY :
// Pipe give us power
// to pipe data from any readable stream
// to any writeable stream

function summery() {
  return `
    // Pipe give us power 
    // to pipe data from any readable stream
    // to any writeable stream
    // Write on Terminal and file will be created (Ctrl+C to stop)
    `;
}
