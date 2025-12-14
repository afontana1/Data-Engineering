const fs = require("fs");

fs.mkdir("new folder (11)", err => {
  if (err) {
    console.error("\n ==== \n error code: ", err.code);
  } else {
    console.log("====\n folder created with mkdir command \n====");
  }
});
// rename & remove at 07 


/// ==================
// THE IMPORTANT STAFF HERE : mkdir & exsistSync
// simple case use :
//                 ***  fs.mkdir(dirName, err =>  like var createFolder
// you can check if exists with :
//                 *** fs.exsistSync(dirName)
/// ==================
