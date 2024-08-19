const events = require("events");
const emitter = new events.EventEmitter();
////////////////////////////////////////////
const readline = require("readline");
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
////////////////////////////////////////////

const collectAnswers = questions => {
  const answers = [];
  const [firstQ] = questions; // distructer the array at [0]

  // answer questions :
  const answerAQuestion = answer => {
    answers.push(answer);
    emitter.emit("answer", answer);

    if (answers.length < questions.length) {
      rl.question(questions[answers.length], answerAQuestion);
    } else emitter.emit("done", answers);
  };

  // Starting the proccess
  rl.question(firstQ, answerAQuestion);

  return emitter;
  // ^ otherwise we will not have it in the other file
};

module.exports = {
  collectAnswers
};
