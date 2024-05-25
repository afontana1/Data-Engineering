const service = require("./07-questions.emit"); // const emitter = new events.EventEmitter();

const questions = ["Ready? ", "Set ", "Go "];

const answerEvent = service.collectAnswers(questions);

// you can have more than 1 action
// for each emit type/string
answerEvent.on("answer", answer => {
  if (answer.toLowerCase() === "exit" || answer.toLowerCase() === "e") {
    process.exit();
  } else console.log("your answer is: ", answer);
});

answerEvent.on("answer", answer => {
  if (answer === "yes") console.log("good");
});

answerEvent.on("done", answers => {
  console.log("==================");
  console.log("Thank you for your answers");
  console.log(answers);
});
answerEvent.on("done", answers => {
  process.exit();
});
