const readline = require ('readline')
const rl = readline.createInterface ({
    input: process.stdin,
    output: process.stdout
})

const questions = [ 'what is your name ', 'where  are you live ', 'what are you doing for your living ']


const cellectAnswers = (questions, done) => {
    const answers =  []
    const [firstQ] = questions // distructer the array at [0]
    
    // answer questions : 
    const answerAQuestion = answer => {
        answers.push(answer)
        if (answers.length < questions.length) {
            rl.question(questions[answers.length] , answerAQuestion)
        } else done(answers)
    } 

    // Starting the proccess 
    rl.question(firstQ, answerAQuestion)
}

cellectAnswers(questions , answers => {
    console.log('==================');
    console.log('Thank you for your answers');
    console.log(answers);
    process.exit()
})