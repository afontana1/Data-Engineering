const path = require('path');
const express = require('express');
const hbs = require('hbs');
const serverless = require('serverless-http');
const geocode = require('./src/utils/geocode')
const forecast = require('./src/utils/forecast')

console.log(__dirname);
console.log(path.join(__dirname, '../public'));

const app = express();

// Define paths for Express config
const publicDirectoryPath = path.join(__dirname, './public');
const viewsPath = path.join(__dirname, "./templates/views");
const partialsPath = path.join(__dirname, "./templates/partials");

// Setup handlebars engine and views location 
app.set('view engine', 'hbs');
app.set('views', viewsPath);
hbs.registerPartials(partialsPath);

// Setup static directory to serve
app.use(express.static(publicDirectoryPath, {
    extensions: ['html']
}));

app.get('', (req, res) => {
    res.render('index', {
        title: 'Weather',
        name: 'Nadir Sidi'
    });
})

app.get('/about', (req, res) => {
    res.render('about', {
        title: 'About Me',
        name: 'Nadir Sidi'
    });
})

app.get('/help', (req, res) => {
    res.render('help', {
        title: "Help",
        name: "Nadir Sidi",
        message: "This is a help message"
    });
})

app.get('/weather', (req, res) => {
    if (!req.query.address) {
        return res.send({
            error: 'You must provide an address.'
        })
    }

    geocode(req.query.address, (error, {latitude, longitude, location} = {}) => {
        if (error) {
          return res.send({ error });
        }
    
        forecast(latitude, longitude, (error, forecastData) => {
            if (error) {
              return res.send({ error });
            }
    
            res.send({
                forecast: forecastData,
                location,
                address: req.query.address
            });
          })
    })
})

app.get('/products', (req, res) => {
    if (!req.query.search) {
        return res.send({
            error: 'You must provide a search term'
        })
    }

    res.send({
        products: []
    })
})

app.get('/help/*', (req, res) => {
    res.render('404', {
        title: "404",
        name: "Nadir Sidi",
        message: "Help article not found."
    });
})

app.get('*', (req, res)  => {
    res.render('404', {
        title: "404",
        name: "Nadir Sidi",
        message: "Page not found"
    });
})

// app.listen(3000, () => {
//     console.log('Server is up on port 3000...')
// })

module.exports.handler = serverless(app);
