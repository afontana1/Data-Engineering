/// ==================
// THE IMPORTANT STAFF HERE : mkdir & exsistSync
// simple case use :
//                 ***  fs.mkdir(dirName, err =>  like var createFolder
// you can check if exists with :
//                 *** fs.exsistSync(dirName)
/// ==================
/// ==================
// more deep use
// fs.mkdir
// CREATE FOLDER:
const dirName = "new folder";
const createFolder = dirName => {
  fs.mkdir(dirName, err => {
    if (err) {
      console.error("\n ==== \n error code: ", err.code);
      console.error("error message: ", err.message, "\n ====");

      // extra code
      // just becuase we can listen with readline
      setTimeout(() => {
        process.exit();
      }, 400);
      return;
    } else {
      console.log("====\n folder created with mkdir command \n====");
    }
  });
};

// =======================

const readline = require("readline");
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// =======================
// make a dealy :
setTimeout(() => {
    
    // fs.existsSync
    // CHECK IF FOLDER EXISTS :
    if (fs.existsSync(dirName)) {
    // ... bla bla bla
    console.log("=== \n this directory already exists");
    console.log("if we would create it you will get an error  \n===");

    // some logic to be able see errors
    setTimeout(() => {
      isCreateFolderAnyway();
    }, 1150);
  } else {
    // IF NOT EXISTS CREATE A FOLDER :
    createFolder(dirName);
  }

  function isCreateFolderAnyway() {
    rl.question("do you want to try ?", data => {
      const answer = data;
      if (answer === "y" || answer === "yes") createFolder(dirName);
      else process.exit();
    });
  }
}, 350);
