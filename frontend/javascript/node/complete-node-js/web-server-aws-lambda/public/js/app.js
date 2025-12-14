console.log('Client side javascript file is loaded!')

const weatherForm = document.querySelector('form')
const searchElement = document.querySelector('input')
const messageOne = document.querySelector('#message-1')
const messageTwo = document.querySelector('#message-2')

weatherForm.addEventListener('submit', (e) => {
    e.preventDefault()

    const location = searchElement.value

    messageOne.textContent = 'Loading...'
    messageTwo.textContent = ''

    fetch('http://localhost:3000/weather?address=' + location).then( (response) => {
        response.json().then( (data) => {
            if (data.error) {
                messageOne.textContent = data.error;
                messageTwo.textContent = ''
            } else {
                messageOne.textContent = data.address
                messageTwo.textContent = data.forecast
            }
        })
    })
})