const fs = require("fs");
const dirName = "new folder (11)";
const newDirName = "new folder (22)";

// create file if not exsist:
if (!fs.existsSync(dirName)) {
  fs.mkdirSync(dirName);
}

setTimeout(() => {
  // ========= 
  // rename:
  fs.rename(dirName, newDirName, err => {
    if (err) throw err;
    else console.log("====\n  file renamed  \n====");
  });

}, 300);

setTimeout(() => {
  // ========= 
  // remove :
  fs.rmdir(newDirName, err => {
    if (err) throw err;
    else console.log("folder deleted");
  });

}, 1000);
