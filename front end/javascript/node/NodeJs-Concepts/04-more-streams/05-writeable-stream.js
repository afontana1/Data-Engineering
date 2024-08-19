// writeable stream for example: 
// process.stdIn , http, file system
const {createWriteStream, createReadStream} = require('fs')
const readStream = createReadStream('./assets/surfing_waves.mp4')
const writeStream = createWriteStream('./05----copy.mp4')

readStream.on('data', (chunk) => {
    writeStream.write(chunk)
})

readStream.on('error', err => {
    console.error('error occurred',err.message);
})

readStream.on('end', () => {
    writeStream.end()
})

// write stream listerners :
writeStream.on('close', () => {
    process.stdout.write('\nfile copied')
    process.stdout.write('\n========');
})
