const fs = require("fs");
const files = fs.readdirSync("./");

// changing from md to txt
// :::::::::::::::::::::::
const find = files.find(file => file.substr(-2) === 'md' || file.substr(-3) === 'txt');
const oldExt =  find.substr(-1) === 'd' ? 'md' : 'txt'
const newExt =  find.substr(-1) === 'd' ? 'txt' : 'md'

const newFileName = find.replace(oldExt,newExt)

fs.rename(find, newFileName, err => {
    console.log('\n --> changing',oldExt,' to ' , newExt);
    if (err) throw err
    else console.log('file name changed \n');
})
