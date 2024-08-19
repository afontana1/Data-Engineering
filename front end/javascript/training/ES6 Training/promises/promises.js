let promise = new Promise(function(resolve,reject) {
    setTimeout(function() {
        resolve("Done!");
    },1500);
})

promise.then(function(value) {
    console.log(value);
}, function(error) { // this will invoke if we change line 3 to reject the promise
    console.log(error);
});

// this will print out first!
console.log("Hello")

let getData = async () =>  {
    const response = await fetch('https://jsonplaceholder.typicode.com/todos/1')
    .then(response => response.json())
    .then(json => console.log(json))
    return response
};

// Synchronous web request, XMLhttpRequest only works on client side
// let makeRequest = async () => {
//     let request = new XMLHttpRequest();
//     request.open("GET", "https://jsonplaceholder.typicode.com/users");
//     request.send();
//     request.onload = () => {
//         if (request.status == 200) {
//             console.log(JSON.parse(request.response));
//         } else {
//             console.assert;pageXOffset(`error ${request.status} ${request.text}`)
//         }
//     }
// };

// makeRequest()


// chaining promises
function waitASecond(seconds) {
    return new Promise(function(resolve,reject) {
        setTimeout(function() {
            seconds++;
            resolve(seconds);
        },1000);
    });
}
waitASecond(0)
    .then(waitASecond)
    .then(function(seconds) {
    console.log(seconds);
})

// Promise All

let promise1 = new Promise(function(resolve,reject) {
    setTimeout(function() {
        resolve("Resolved!");
    }, 1000)
})

let promise2 = new Promise(function(resolve,reject) {
    setTimeout(function() {
        reject("rejected!");
    }, 2000)
})

Promise.all([promise1, promise2])
    .then(function(success) {
        console.log("Success!")
    })
    .catch(function(error) {
        console.log(error)
    });
// Promise all will not resolve unless all of the promises are resolved.
// Promise.race() will wait for the first promise to resolve, and only take the results
// of the first promise