function Particle() {
    this.x = 100
    this.y = 100
    // this.show = function() {
    //     point(this.x, this.y)
    // };
};

Particle.prototype.show = function () {
    console.log(this.x, this.y);
} // this assigns the function to the prototype, so it does not need to be in the constructor


let p1 = new Particle();

console.log(p1.__proto__)
console.log(p1.show())

// note that all of this above is whats being done when we use the class keyword

class User {
    constructor(email, name){
        this.email = email;
        this.name = name;
        this.score = 0;
    }
    login(){
        console.log(this.email, 'just logged in');
        return this;
    }
    logout(){
        console.log(this.email, 'just logged out');
        return this;
    }
    updateScore(){
        this.score++;
        console.log(this.email, 'score is now', this.score);
        return this;
    }
}

class Admin extends User {
    deleteUser(user){
        users = users.filter(u => {
            return u.email != user.email
        });
    }
}

var userOne = new User('joe@hotmail.com', 'joe');
var userTwo = new User('mama@hotmail.com', 'mama');
var admin = new Admin('idk@hotmail.com', 'hello');

userOne.login().updateScore().updateScore().logout();
console.log(userOne);

var users = [userOne, userTwo, admin];
userTwo.deleteUser(userOne); // won't work
console.log(users);

// notice that we are not connecting the methods directly to the object
function User(email, name){
    this.email = email;
    this.name = name;
    this.online = false;
}

User.prototype.login = function(){
    this.online = true;
    console.log(this.email, 'has logged in');
};

User.prototype.logout = function(){
    this.online = false;
    console.log(this.email, 'has logged out');
};

function Admin(...args){
    User.apply(this, args);
}

Admin.prototype = Object.create(User.prototype);

Admin.prototype.deleteUser = function(u){
    users = users.filter(user => {
        return user.email != u.email;
    });
};

var userOne = new User('joe@hotmail.com', 'joe');
var userTwo = new User('idk@hotmail.com', 'hello');
var admin = new Admin('idk@hotmail.com', 'hello');

console.log(userOne);
userTwo.login();
var users = [userOne, userTwo, admin];