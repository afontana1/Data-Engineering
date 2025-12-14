const fs = require('fs')

const theTxt = `
### A new file created with nodejs
    we used core module - 'fs'

## now we now :
    fs.readdir - read a folder content
    fs.readFile - read file content
    fs.writeFile - write fule

    /* all above have sync option and regular */
`;
const path = './text-files/new-notes.md';
fs.writeFile(path,theTxt.trim(), (err) => {
    if (err) {
        console.error('we have Error: ',err.message);
        throw Error
    } 
    console.log('====== \n file saved \n ======');
});