const functions = require('./modules.cjs');

console.log(functions)

class AJ extends functions.Person {
    constructor(name, lastname) {
        super(name);
        this.lastname = lastname
        this.true_age = 29
    };

    full_greeting() {
        console.log("Hello " + this.name + " " + this.lastname)
        return "Hello " + this.name + " " + this.lastname
    };

    print_age(value) {
        console.log(this.full_greeting() + "is " + value)
    };

    static guess_age(value) {
        return value == this.true_age;
    };
};

let aj = new AJ("AJ","Fontana");
aj.full_greeting();
aj.print_age(29)
console.log(AJ.guess_age(18))

class AjTwin extends AJ {
    constructor(twin_name, name, lastname) {
        super(name,lastname)
        this.twin_name = twin_name
        this._right_arm = "smaller"
    };

    get difference() {
        return this._right_arm.toUpperCase();
    };

    set difference(value) {
        this._right_arm = value;
    };
};

let ajtwin = new AjTwin("BJ","AJ","Fontana");
console.log(ajtwin)
console.log(ajtwin.difference)
ajtwin.difference = "bigger"
console.log(ajtwin.difference)