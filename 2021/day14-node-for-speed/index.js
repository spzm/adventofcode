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
  const polymer = strings[0];
  const insertions = strings.slice(2, dataString.length - 1).map(str => str.split(' -> '));

  return [polymer, insertions];
}

function findMinMax(lettersMap) {
  let max;
  let min;
  for (let value of Object.values(lettersMap)) {
    if (max === undefined && min === undefined) {
      max = value;
      min = value
    }

    if (value > max) {
      max = value;
    }

    if (value < min) {
      min = value;
    }
  } 

  return [min, max];
}

function process(polymerString, insertions, iterations) {
  let polymerMap = {};
  const lettersMap = {};
  let acc = ''

  for (let symbol of polymerString) {
    acc += symbol;
    lettersMap[symbol] = lettersMap[symbol] ? lettersMap[symbol] + 1 : 1;

    if (acc.length == 2) {
      if (!polymerMap[acc]) {
        polymerMap[acc] = 1;
      } else {

        polymerMap[acc]++;
      }

      acc = acc[1];
    }
  }

  for (let i = 0; i < iterations; i++) {

    const iterateMap = {...polymerMap};
    for (let insertion of insertions) {
      const [newKey, insertValue] = insertion;

      if (iterateMap[newKey]) {
        const keys = [newKey[0] + insertValue, insertValue + newKey[1]];
        for (let key of keys) {
          polymerMap[key] = polymerMap[key] ? polymerMap[key] + iterateMap[newKey] : iterateMap[newKey];
        }

        lettersMap[insertValue] = lettersMap[insertValue] ? lettersMap[insertValue] + iterateMap[newKey] : iterateMap[newKey];
        polymerMap[newKey] -= iterateMap[newKey];
      }
    }
  }

  const [min, max] = findMinMax(lettersMap);

  return max - min;
}

console.log(`Processing results for path: ${path}`);

const inputData = await processFile(path);

console.log(`10 iterations: ${process(inputData[0], inputData[1], 10)}`);
console.log(`40 iterations: ${process(inputData[0], inputData[1], 40)}`);
