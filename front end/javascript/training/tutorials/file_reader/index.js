const fs = require("fs");
const http = require("https");
const stream = require('stream');
const util = require("util");
const path = require('path');

const pipeline = util.promisify(stream.pipeline);



let fileName = "BigBoy.txt";
let url = "https://norvig.com/big.txt"

const file = fs.createWriteStream(fileName);
const newFile = fs.createReadStream(fileName);
file.on("error", err => console.log(err));

function get_stream () {

    http.get(url).on("response", function(res) {
        let downloaded = 0;
        res.on("data", function(chunk) {
            let readyForMore = file.write(chunk);
            if (!readyForMore) {
                // pause readstream until drain event comes
                res.pause();
                file.once('drain', () => {
                    res.resume();
                });
            }
            downloaded += chunk.length;
            process.stdout.write(`Downloaded ${(downloaded / 1000000).toFixed(2)} MB of ${fileName}\r`);
        }).on("end", function() {
            file.end(); console.log(`${fileName} downloaded successfully.`);
        }).on("error", err => console.log(err));
    });
}


async function get(url) {
    try {
        const response = (await fetch(url)).text();
        await pipeline(
            response,
            file
        )
    } catch(error) {
        console.log(error)
    }
};

// get(url);
// immediately pipe to another file
// var readerStream = fs.createReadStream(fileName);
// var writerStream = fs.createWriteStream('outputfile.txt');
// readerStream.pipe(writerStream);

// alternatively with node-fetch
// fetch(url)
//   .then(
//     res =>
//       new Promise((resolve, reject) => {
//         const dest = fs.createWriteStream("stuff.txt");
//         res.body.pipe(dest);
//         res.body.on("end", () => resolve("it worked"));
//         dest.on("error", reject);
//       })
//   )
//   .then(x => console.log(x));

// create directory and write files to it

const directoryPath = path.join(__dirname, '');
let stuff = fs.readdirSync(directoryPath, (e) => console.log(e)).filter((fname) => !fname.endsWith(".js"));
if (!fs.existsSync('./files')) {
    fs.mkdir("./files", (err) => {
        if (err) throw err;
        console.error("It exists fucker")
    })
}


function write(file){
    try {
        fs.rename(file, `./files/${file}`, (err) => console.log(err));
        console.log('File moved successfully');
    } catch (error) {
        console.error(error);
    }
};

function write_all(files) {
    for (f of files) {
        write(f);
    }
}

//write_all(stuff);