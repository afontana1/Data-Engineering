// writeable stream for example: process.stdIn , http, file system

const fs = require('fs')

//                                 file will be created automatically:
const writeStream1 = fs.createWriteStream('./from-terminal.txt','UTF-8')

// Pipe into  
// ==============

// #1 : 
// uncomment for experimental :
// process.stdin.pipe(writeStream1)


// #2 :
//-> here from 1 file into other file
const writeStream2 = fs.createWriteStream('./file1.txt','UTF-8')

const readStream = fs.createReadStream('./file1-copy.txt','UTF-8')
readStream.pipe(writeStream2)



// writeable stream for example: 
// process.stdIn , http, file system
