const request = require('request')

const forecast = (lat, long, callback) => {
    const url = 'http://api.weatherstack.com/current?access_key=fa494bad69a0e7cf22cba7165cdee2e6&query=' + lat + ',' + long + '&units=f'

    request({ url, json: true}, (error, { body }) => {
        if(error) {
            callback('Unable to connect to weather service.', undefined)
        } else if (body.error) {
            callback('Unable to find location', undefined)
        } else {
            callback(undefined, 'It is currently ' + body.current.temperature +  ' degrees out. There is a ' + body.current.precip + '% chance of rain.') 
        }
    })
} 

module.exports = forecast