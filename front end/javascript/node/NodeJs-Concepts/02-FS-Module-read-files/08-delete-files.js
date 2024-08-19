const fs = require("fs");
const dirName = "./new folder 11111";

// REMOVE FILE
const removeFile = () =>
  fs.readdirSync(dirName).forEach(file => {
    fs.unlinkSync(`${dirName}/${file}`);
    console.log(`the file ${file} removed`);
  });

// REMOVE FOLDER
const removeFolder = () =>
  fs.rmdir(dirName, err => {
    if (err) throw err.message;
    else console.log(`folder ${dirName} removed`);
  });

// create folder if not exsist:
const creteFileAndFolder = () => {
  if (!fs.existsSync(dirName)) {
    fs.mkdirSync(dirName);
    console.log("folder created");
    [1, 2].forEach(i => {
      fs.writeFileSync(`${dirName}/bla${i}.txt`, "bla bla bla");
      console.log(`file bla${i}.txt} created`);
    });
  }
};

const init = () => {
    console.log("====\nStarting ...");
  creteFileAndFolder();

  setTimeout(() => {
    console.log("removing file ...");
    removeFile();
  }, 1500);

  setTimeout(() => {
    console.log("removing folder ...");
    removeFolder();
  }, 2500);
};
init();
