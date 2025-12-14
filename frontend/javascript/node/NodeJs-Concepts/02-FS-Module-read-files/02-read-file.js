const fs = require("fs");
const text = fs.readFileSync("./text-files/note.txt", "utf-8");

// SYNC File Read
console.log("\n----> SYNC file read : ", text, '\n');

// ASYNC File Read
fs.readFile("./text-files/text.md", "utf-8", (err, mdFile) => {
  if (err) {
    console.error("an error of ", err.message);
    process.exit()
  }
  console.log("\n----> ASYNC file read : ", mdFile);
  console.log("now it done [from the call back]");
  console.log("\n");
});

console.log(" some log in the end of the JS file.\n does the file done ?");
