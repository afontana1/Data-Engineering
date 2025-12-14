const stuff = require('./modules.cjs');

const express = require('express');
const cors = require('cors');
const path = require('path');
const ss = require('simple-statistics')

const app = express();

const PATH_TO_DIR = path.join(__dirname);

app.use(cors());
app.use(express.urlencoded({ 
    extended: true,
    limit: 10000,
    parameterLimit: 2,
}))
app.use(express.static(__dirname));

app.get('/',function(req,res) {
    res.sendFile(PATH_TO_DIR + '/index.html');
  });

app.post('/submit_name', function(req,res) {
    console.log(req.body)
})

app.get('/get_status', function(req,res) {
 
    const fileName = 'Hello.txt';
    res.download(PATH_TO_DIR + "/" + fileName, function (err) {
        if (err) {
            next(err);
        } else {
            console.log('Sent:', fileName);
        }
    });
});

app.post('/generate_data',function(req,res) {
    // Create Random Points
    const numPoints = req.body.datagen;
    data = stuff.create_data(numPoints)
    console.log(data)
    res.json({"data":data});
})

app.get('/get_file',function(req,res) {
     
    // Download function provided by express
    const fileName = 'Hello.txt';
    res.download(PATH_TO_DIR + "/" + fileName, function(err) {
        if(err) {
            console.log(err);
        }
    })
})

app.listen(3000);