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
  const splittedStrings = strings.map(str => str.split(' \| ').filter(v => v).map(v => v.split(' ')));

  return splittedStrings.map(lines => lines.map(part => part.map(str => str.split('').sort().join(''))));
}

function processSimpleDigits(parts) {
  let counter = 0;
  for (let digitStrings of parts) {
    const outputValues = digitStrings[1];

    for (let string of outputValues) {
      const l = string.length;
      if (l == 8 || l == 7 || l == 4 || l == 3 || l == 2) {
        counter++;
      } 
    }
  }
  return counter;
}

const simpleDigitsLengthMap = {
  2: 1,
  3: 7,
  4: 4,
  7: 8
}

function processFullDigits(parts) {
  let counter = 0;
  for (let digitStrings of parts) {
    const [inputValues, outputValues] = digitStrings;

    const valueMap = {};
    const complexDigits = [];
    const digits = [];
    for (let digitString of inputValues) {
      const l = digitString.length;

      if (l == 8 || l == 7 || l == 4 || l == 3 || l == 2) {
        valueMap[digitString] = simpleDigitsLengthMap[l];
        digits[simpleDigitsLengthMap[l]] = digitString.split('');
      } else {
        complexDigits.push(digitString);
      }
    }
   
    const lastComplex = [];
    for (let digitString of complexDigits) {
      const l = digitString.length;
      if (l == 6) {
        if (!digits[1].every(digit => digitString.includes(digit))) {
          valueMap[digitString] = 6;
          digits[6] = digitString.split('');
        } else if (digits[4].every(digit => digitString.includes(digit))) {
          valueMap[digitString] = 9;
        } else {
          valueMap[digitString] = 0;
        }
      } else if (l == 5) {
        if (digits[1].every(digit => digitString.includes(digit))) {
          valueMap[digitString] = 3;
        } else {
          lastComplex.push(digitString);
        }
      }
    }

    let segmentC = digits[1].find(symbol => !digits[6].includes(symbol));

    for (let digitString of lastComplex) {
      const l = digitString.length;
      if (l == 5) {
        if (digitString.includes(segmentC)) {
          valueMap[digitString] = 2;
        } else {
          valueMap[digitString] = 5;
        }
      }
    }

    for (let i = 0; i < outputValues.length; i++) {
      counter += valueMap[outputValues[i]] * (10 ** (outputValues.length - i - 1));
    }
  }

  return counter;
}

console.log(`Processing results for path: ${path}`);

const inputData = await processFile(path);
console.log(`Simple digits count: ${processSimpleDigits(inputData)}`);
console.log(`Digits sum calculation: ${processFullDigits(inputData)}`);
