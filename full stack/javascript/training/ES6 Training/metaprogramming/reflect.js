
class Person {
    constructor(name){
        this.name = name
    }

    greet (){
        console.log("Hello " + this.name);
    }
};

function topObj() {
    this.age = 29
};

let person = Reflect.construct(Person,["AJ"], topObj) // passing in the third arg overrides the constructor
console.log(person)
console.log(person.__proto__ == Person.prototype)
console.log(person.__proto__ == topObj.prototype)

// get list of attributes, not the values of the properties, but the core property names
console.log(Reflect.ownKeys(person))


// you can also create properties dynamically

Reflect.defineProperty(person,'hobbies', {
    writable: true,
    value: ["sex and drugs"],
    configurable: true
});
console.log(Reflect.ownKeys(person))

// if you want to lock the object so it cant be extended or modified run the code below
Reflect.preventExtensions(person);
console.log(Reflect.isExtensible(person));

// see docs for more examples