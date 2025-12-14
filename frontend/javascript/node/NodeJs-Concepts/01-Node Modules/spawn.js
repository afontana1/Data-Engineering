
// USE TO DO ASYNC SERVICE TO SYNC SERVICE 
const cp = require('child_process')
const questionApp = cp.spawn('node', ['03-readline.js'])

// answering the questions
questionApp.stdin.write('Me')
questionApp.stdin.write('Here')
questionApp.stdin.write('Dev')


questionApp.stdout.on('data',data => {
    console.log('from the question app: ',data.toString());
})


questionApp.on('close', () => {
    console.log('app closing');
    
})