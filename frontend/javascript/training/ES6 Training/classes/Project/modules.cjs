let value = 500;


class Person {
    constructor(name){
        this.name = name
    }
    greet() {
        console.log("Hello " + this.name);
    }
}

let person = new Person("AJ");
person.greet();

function create_data(nsamples) {
    var x = [];
    var y = [];
    var n = nsamples;
    var x_mean = 0;
    var y_mean = 0;
    var term1 = 0;
    var term2 = 0;
    var noise_factor = 100;
    var noise = 0;
    // create x and y values
    for (var i = 0; i < n; i++) {
        noise = noise_factor * Math.random();
        noise *= Math.round(Math.random()) == 1 ? 1 : -1;
        y.push(i / 5 + noise);
        x.push(i + 1);
        x_mean += x[i]
        y_mean += y[i]
    }
    // calculate mean x and y
    x_mean /= n;
    y_mean /= n;

    // calculate coefficients
    var xr = 0;
    var yr = 0;
    for (i = 0; i < x.length; i++) {
        xr = x[i] - x_mean;
        yr = y[i] - y_mean;
        term1 += xr * yr;
        term2 += xr * xr;

    }
    var b1 = term1 / term2;
    var b0 = y_mean - (b1 * x_mean);
    // perform regression 

    let yhat = [];
    // fit line using coeffs
    for (i = 0; i < x.length; i++) {
        yhat.push(b0 + (x[i] * b1));
    }

    var data = [];
    for (i = 0; i < y.length; i++) {
        data.push({
            "yhat": yhat[i],
            "y": y[i],
            "x": x[i]
        })
    }
    return (data);
}

// console.log(create_data(1000))

// bundle up all the functions and data you want to export for ES6
// const functions = {
//     Person,
//     value,
//     create_data
// }

module.exports = {
    "create_data":create_data,
    "Person":Person
}