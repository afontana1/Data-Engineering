const events = require("events");
const emitter = new events.EventEmitter();

// defining the event :
emitter.on("myEvent", (message, user = "system", ...args) => {
  // rest: add space between rest of the words
  const rest = args.join(" ");
  console.log(`${user}: ${message} \n \t ${rest}`);
});

// you can choose what name you want for the event ours is --> myEvent <--
emitter.emit("myEvent", "Hello World");
emitter.emit("myEvent", "Hi", "John");
emitter.emit("myEvent", "wow ", "me", "Hi", "you", "what", "going", "on?");

process.stdin.on("data", data => {
  const input = data.toString().trim();
  if (input.toLowerCase() === "exit" || input.toLowerCase() === "e") {
    emitter.emit("myEvent", "goodBye");
    process.exit();
  }
  emitter.emit("myEvent", input, "terminal");
});

// you can have more than 1 listeners for an event
