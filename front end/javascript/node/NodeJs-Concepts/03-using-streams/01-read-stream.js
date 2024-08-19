// WE CAN READ FILES CHUNK BY CHUNK
const fs = require("fs");
// getting staff ready :
const folderPath = "./sample-stream";
const fileName = "text.txt";
createFolderAndFile();
// ::::::::::::::::::::::::::::
// ::::::::::: MAIN ::::::::::::::::::
const readStream = fs.createReadStream(`${folderPath}/${fileName}`, "UTF-8");
let count = 1;
let copyTxt;
// ON -> for every chunck added
readStream.on("data", data => {
  console.log(`Chunck ${count} : ${data.length - 1} characters`);
  count++;
  copyTxt += data;
});

// ONCE -> 
readStream.once("data", data => {
  console.log("this is the first byte of data : ", data);
});

// END
readStream.on("end", () => {
  console.log("finish reading file");
  console.log(`I read ${(copyTxt.length - 1).toLocaleString()} characters of text`);
});





// extra for prevent errors :
// ::::::::::::::::::::::::::::
function createFolderAndFile() {
  const lorem = require("./lorem.js");
  const txt = lorem.txt;
  if (!fs.existsSync(folderPath)) fs.mkdirSync(folderPath);
  if (!fs.existsSync(`${folderPath}/${fileName}`)) {
    fs.writeFileSync(`${folderPath}/${fileName}`, new Date() + txt, err => {
      if (!err) {
        throw console.error("we have Error: ", err.message);
      }
    });
  }
}
