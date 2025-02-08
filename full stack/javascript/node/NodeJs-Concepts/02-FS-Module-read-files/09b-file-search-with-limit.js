const fs = require("fs");

const findAnyFile = (startPath, folderName, ext, deep = 10) => {
  let deepCount = 0;
  const foundFiles = [];
  const dirPath = `${startPath}${folderName}`;

  // RECURSION :
  function findFiles(folder, parentFolder = null) {
    if (deepCount > deep) return;
    // console.log(folder, deepCount);

    if (!fs.existsSync(folder)) {
      console.log("dir: ", folder, "not found");
      return;
    }
    // FILES Filter==========>
    const files = fs.readdirSync(`${folder}`);
    const filteredFiles = files.filter(file => {
      const fileSplited = file.split(".");
      const currExt = fileSplited[fileSplited.length - 1].toLowerCase();

      //  -------------
      // getting to check if folder or file
      const isFolder = fs.lstatSync(folder + '/' +file ).isDirectory();
      if (isFolder) {
        if (folder !== parentFolder) {
          deepCount++;
        }
        return findFiles(folder + "/" + file, folder);
      } else {
        if (currExt === ext) foundFiles.push(file);
      }
    });
  }
  findFiles(dirPath, ext);
  return foundFiles;
};

const files = findAnyFile("/", "Users", "docx", 50);
console.log("========\n", files, files.length);
