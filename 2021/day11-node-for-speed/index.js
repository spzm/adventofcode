import fs from 'fs/promises';
import { argv, exit } from 'process';

const path = argv[2];

if (!path) {
  console.error('No file name provided');
  exit();
}

async function processFile(path) {
  let dataString;

  try {
    dataString = await fs.readFile(path, 'utf8');
  } catch(err) {
    console.error('Cannot read file', err);
  }

  const strings = dataString.split('\n');
  const splittedStrings = strings.map(str => str.split('').map(value => +value));

  return splittedStrings
}


function process(values) {
  let totalFlashes = 0;

  function update(i, j, diff = 1) {
    if (i < 0 || j < 0 || i >= values[0].length || j >= values.length) {
      return;
    }

    if (values[i][j] === 0) return;

    values[i][j] += diff; 

    if (values[i][j] > 9) {
      totalFlashes++;
      values[i][j] = 0;

      for (let v1 of [1, 0, -1]) {
        for (let v2 of [1, 0, -1]) {
          update(i + v1, j + v2);
        }
      }
    }
  }

  function iterateThroughAll(action) {
    for (let i = 0; i < height; i++) {
      for (let j = 0; j < width; j++) {
        if (action(i, j) === false) break;
      }
    }
  }

  let finalStep = 0;
  let iteration100Result = 0;

  const height = values.length;
  const width = values[0].length

  let counter = 0;
  while(true) {
    counter++;

    iterateThroughAll((i, j) => values[i][j]++);
    iterateThroughAll((i, j) => update(i, j, 0));

    let value = values[0][0];
    let equal = true;
    iterateThroughAll((i, j) => {
      if (values[i][j] !== value) {
        equal = false;
      }
      return equal;
    });

    if (counter === 100) {
      iteration100Result = totalFlashes;
    }

    if (equal) {
      finalStep = counter;
      break;
    }
  }

  return [iteration100Result, finalStep];
}

console.log(`Processing results for path: ${path}`);

const inputData = await processFile(path);

const [flashLights, firstSynchronousStep] = process(inputData);

console.log(`Flashlights on 100 step: ${flashLights}`);
console.log(`First synchronous step: ${firstSynchronousStep}`);
