let person = {
    name: "aj"
};

let handler = {
    get: function(target, name) {
        return name in target ? target[name] : false
    },
    set: function(target,property,value) { //notice how this is like a decorator in python
        if (value.length >= 2) {
            Reflect.set(target,property,value)
        }
    }
};

// the proxy acts as a wrapper
// it contains logic that is ran to validate some business logic
// proxies act as extra layers between some target service and the request
// this is called a "trap" in javascript jargon
var proxy = new Proxy(person, handler);

console.log(proxy.name)
console.log(proxy.height)
proxy.name = "A" // this wont set, will not validate
console.log(proxy.name)

// We can attach the proxy to the person prototype
// you can set an indefinite amount of proxies to the object prototype
var newproxy = new Proxy({}, handler);
Reflect.setPrototypeOf(person, newproxy)
console.log(person.hobbies); //this wont do anything obviously because it doesnt validate the get criteria
// proxies appear to be like decoraters, extensible functionality to base code

// You can also wrap functions in proxies

function log(message) {
    console.log(message);
}

console.log(log("hey"))

let handler_2 = {
    apply: function(target, message, argumentsList){
        if (argumentsList.length == 1) {
            return Reflect.apply(target,message,argumentsList)
        }else{
            console.log("Check arguments")
        }
    }
}

let proxy_2 = new Proxy(log,handler_2) // this acts as a wrapper
proxy_2("Hello",10); // throws else console statement

// you can also revoke proxies, without adjusting your code

let animal = {
    name: "Jerry"
};

let animal_handler = {
    get: function(target,property) {
        return Reflect.get(target,property);
    }
};

let {animal_proxy, revoke} = Proxy.revocable(animal,animal_handler);

revoke();
console.log(animal_proxy.name)