const { Readable } = require("stream");
// List of river systems longer than 1000 km
const peaks = [
  "White Nile",
  "Amazon",
  "Yangtze",
  "Mississippi",
  "Yenisei",
  "Yellow River",
  "Ob"
];

class StremFromArray extends Readable {
  constructor(array) {
    // in super we can use modes:
    // like { encoding: "UTF-8" } 
    // use cosole.log on this instance to see more
    super({ objectMode: true });
    this.array = array;
    this.index = 0;
  }

  _read() {
    if (this.index <= this.array.length) {
      const chunk = this.array[this.index];
      this.push(chunk);
      this.index++;
    } else {
      this.push(null);
    }
  }
}

const peakStream = new StremFromArray(peaks);
// last array is null so we use  chunck && ...
peakStream.on('data', (chunk) => chunk && console.log(chunk));

peakStream.on('end', () => console.log('done!'));

