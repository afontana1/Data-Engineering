// See this for more explanation of symbol object
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol

let array = [2,3,4,5];
console.log(typeof array[Symbol.iterator])
let it = array[Symbol.iterator](); //this is like calling the __next__ function in python
console.log(it);
console.log(it.next())
console.log(it.next())
console.log(it.next())
console.log(it.next())
console.log(it.next())

// You can change the inner workings of the built in __iter__ method for an array

array[Symbol.iterator] = function() {
    let nextValue = 10;
    return {
        next: function() {
            nextValue++;
            return {
                done: nextValue > 15 ? true : false,
                value: nextValue
            }
        }
    }
}
// now since we have modified the internal method __iter__, we can implement our own logic like above
// you can see that we have modified the internal implementation of the Array iterator method
for (let element of array) {
    console.log(element);
}

// You can use the pattern above to create your own iterator within a custom object

let person = {
    name: "AJ",
    hobbies: ["sex","drugs"],
    [Symbol.iterator]: function() { // this is how we make our object iterable
        let i = 0;
        let hobbies = this.hobbies;
        return {
            next: function() {
                let value = hobbies[i];
                i++;
                return{
                    done: i > hobbies.length ? true: false,
                    value: value
                };
            }
        };
    }
};

for (let hobby of person) {
    console.log(hobby);
}

const regexp1 = /foo/;
// console.log('/foo/'.startsWith(regexp1));
// Expected output (Chrome): Error: First argument to String.prototype.startsWith must not be a regular expression
// Expected output (Firefox): Error: Invalid type: first can't be a Regular Expression
// Expected output (Safari): Error: Argument to String.prototype.startsWith cannot be a RegExp

regexp1[Symbol.match] = false;

console.log('/foo/'.startsWith(regexp1));
// Expected output: true

console.log('/baz/'.endsWith(regexp1));
// Expected output: false


class Dog {
    constructor(name) {
        this.name = name
        this.owners = ["AJ","JOE","MAMA"]
    }

    * get_owners(){
        for (let i = 0; i <= this.owners.length ; i++){
            try {
                yield this.owners[i]
            } catch (e) {
                console.log(e);
            }
        }
    }
}

let woobie = new Dog("woobie");
let owner_gen = woobie.get_owners();
console.log(owner_gen.next());
console.log(owner_gen.next());
console.log(owner_gen.next());
console.log(owner_gen.next());