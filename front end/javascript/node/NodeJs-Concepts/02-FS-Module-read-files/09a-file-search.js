const fs = require("fs");

const findAnyFile = (folderName, ext) => {
  const found = [];
  const dirPath = `${folderName}`;
  findFiles(dirPath, ext);

  // RECURSION :
  function findFiles(folder) {
    if (!fs.existsSync(folder)) {
      console.log("dir: ", folder, "not found");
      return;
    }
    const files = fs.readdirSync(`${folder}`);
    // FILES Filter==========>
    const filteredFiles = files.filter(file => {
      const fileSplited = file.split(".");
      const currExt = fileSplited[fileSplited.length - 1].toLowerCase();
      //  -------------
      // getting to check if folder or file
      const isFolder = fs.lstatSync(folder + "/" + file).isDirectory();
      if (isFolder) {
        return findFiles(folder + "/" + file);
      } else {
        if (currExt === ext) found.push(file);
      }
    });
  }
  return found;
};

const files = findAnyFile("/Users", "docx");
console.log("========\n", files, files.length);
