// find file extention within a specific name folder
searchFiles("/", "1", "txt");

function searchFiles(startPath, folderName, ext) {
  const fs = require("fs");
  const found = [];
  console.log(
    `starting ... looking for ${ext} files in folder named ${folderName}`
  );

  // RECURSION
  findIt(startPath);
  function findIt(path, folder = null) {
    // if we have folder and path is root it will be '/folder'
    // if we don't have folder and path is root (only once, on init)
    // path will be '/'
    const fullPath =
      path !== "/" ? path + "/" + folder : folder ? path + folder : path;

    if (folder) {
      // if not exsist :
      if (!fs.existsSync(`${fullPath}`)) {
        console.log("Folder or Path not exsist at :");
        console.log(`${fullPath}`);
        return;
      }
    }

    // if we have just root:  '/'
    const files = fs.readdirSync(fullPath);
    const filteredFiles = files.filter(file => {
      // skip system files
      if (file && (file.substring(0, 1) === "$" || file.match(/System/))) {
        return;
      }

      // fixPath -> in case we are in root folder (e.g: '/')
      const fixPath =
        fullPath === "/" ? fullPath + file : fullPath + "/" + file;

      const isFolder = fs.lstatSync(fixPath).isDirectory();
      if (isFolder) {
        return findIt(fullPath, file); // call recurtion
      } else {
        // if folder name not as required don't evaluate current file
        if (folder !== folderName) return;
        // else :
        const name = file.split(".");
        const currExt = name[name.length - 1].toLowerCase();
        if (currExt === ext) found.push(fixPath);
      }
    });
  }
  console.log("========\n", found, "\n", found.length, "files");
  return found;
}
