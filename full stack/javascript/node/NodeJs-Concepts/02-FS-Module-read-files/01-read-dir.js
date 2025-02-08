const fs = require ('fs')

console.log('\n==================');
console.log('reading SYNC files took:');
console.time();
const files = fs.readdirSync('./text-files')
console.timeEnd()
// end reading

console.log('\n');
console.log('files: ',files);
console.log('==================');

// ===================
// ==== ASYNC ====  //
console.log('ASYNC:');
console.time();
fs.readdir('/', (err,images) =>{
    if (err) console.error(err.message)
    console.log('images: ',images);
    console.timeEnd()
    console.log('done reading files');
})
console.log('complete reading ?? - no, just async');

