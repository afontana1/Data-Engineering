const fs = require('fs');
const http =  require('http');
const filePath = './assets/surfing_waves.mp4';


// IF WE WOULD DO THIS KIND OF THING WITHOUT A STREAM 
// IT WILL BE SLOW AND USE ALOT OF MEMORY 
// 2 TYPE OF MEMORY: SCAVAGE AND MIKE, MIKE IS FOR LONG RUNS AND IT IS SLOW
// SCAVAGE IS FAST
http.createServer((req, res) => {

    res.writeHeader(200, { 'Content-Type': 'video/mp4' });
    fs.createReadStream(filePath)
        .pipe(res)
        .on('error', console.error);

}).listen(3000, () => console.log('stream - http://localhost:3000'));
