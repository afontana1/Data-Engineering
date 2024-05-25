// Variable declaration
let age = 27;
console.log(age);
const AGES = [2,28,29];
console.log(AGES)
AGES.push(25);
console.log(AGES)
const OBJ = {
    "age": 3
};
console.log(OBJ.age)
OBJ.age = 4
console.log(OBJ)

// Functions
function fn1(a,b) {
    let firstName = "aj";
    let lastName = "fontana";
    let text = `Welcome ${firstName}, ${lastName}!`;
    console.log(text)
    console.log(`${a} + ${b}!`)
    return a+b
};

var fn2 = (a,b) => {
    console.log("Hi")
    return fn1(a,b)
};
var fn3 = (a,b) => fn2(a,b);
console.log(fn3(3,4));

// Arrow functions and "this". Arrow functions
// keep the context from which they are called

var func = () => {
    return this
};
console.log(func())

// default arguments
function is_equal(number = 10,compare = 10) {
    return number == compare
};
console.log(is_equal());

// Object Literals

let name = "aj"; 
age = 29;

let obj = {
    "name":"aj",
    "age": 29
};
console.log(obj)

let obj2 = {
    name,
    age
};
console.log(obj2); //inherits from scope above, assigns keys as variable name

let a = 2;
let b = 2;
let agefield = "agefield";

let obj3 = {
    "sum": fn3(a,b),
    "isequal": is_equal(a,b),
    sum_squared() {
        this.results.squared = this.sum*2
        return this.squared
    },
    "cubed"() {
        this.results.results_cubed = this.sum*3
        return this.sum*3
    },
    "results": {
        "results_cubed" : ""
    },
    [agefield]:29
};

obj3.sum_squared();
console.log(obj3);
obj3["cubed"](); //you have to access it with brackets if its a named function like this
console.log(obj3);

// Rest operator
// Pass three dots in function signature
// Allows functionality like *args and **kwargs in python
// convert all positional arguments into an array

let numbers = [1,2,3,4,5];

function sum_up(...nums) {
    console.log(nums)
    let result = 0;
    for (let i = 0; i < nums.length; i++){
        result += nums[i]
    }
    return result
}
console.log(sum_up(1,2,3,4,5))

// spread operator
// does the opposite of rest
// unpacks list of elements into positional arguments
console.log(Math.max(...numbers))

// For Of loop
let test_results = [1,2,3,4,5,6];
for (let result of test_results){
    console.log(result)
}