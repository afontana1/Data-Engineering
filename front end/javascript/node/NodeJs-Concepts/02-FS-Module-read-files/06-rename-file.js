const fs = require("fs");
const oldFileName = "file-for-append.txt";
const newFileName = "file-name-changed.md";

fs.rename(oldFileName, newFileName, err => {
  if (err)
    console.error(
      "cannot write file \n error code: ",
      err.code,
      "\n error message: ",
      err.message
    );
  else
    console.log("file name has changed, \n correct folder file names are : ");
});

const files = fs.readdirSync("./");
const filterJsFiles = files.filter(file => file.substr(-2) !== "js");
console.log('files: \n ',filterJsFiles);

