const fs = require("fs");
const fileName = "./file-for-append.txt";

if (!fs.existsSync(fileName)) createFile(fileName);
const now = new Date()
const content =  `
WE JUST ADDED THIS LINE
AT ${now}
`

fs.appendFile(fileName,content, (err) =>{
  if (err) throw err
  console.log('we wrote to a file');
  
})

// to align us with the current file stracture
function createFile(fileName) {
  const today = new Date()
  const headline = 'file for append'
  const content = `${headline.toLocaleUpperCase()}\ncreated at: \n ${today}\n\n`;
  fs.writeFileSync(fileName, content, err => {
    if (err) {
      throw console.error("we have Error: ", err.message);
    }
  });
}
