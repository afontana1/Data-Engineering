const { Transform } = require("stream");

// USE Transform to build Class
class ReplaceText extends Transform {
  constructor(char) {
    super();
    this.newChar = char;
  }

  _transform(chunk, encoding, cb) {
    const changed = chunk.toString().replace(/[a-z]|[A-Z]/g, this.newChar);
    this.push(changed);
    cb();
  }
  //
  // _flush(cb) {
  //   this.push();
  //   cb();
  // }
}

const mainChar = 'z'
const charStream = new ReplaceText(mainChar);
// Pipes :
console.log(`\nYour types will be converted into ${mainChar}`);
process.stdin.pipe(charStream).pipe(process.stdout);
