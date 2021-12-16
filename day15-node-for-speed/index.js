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

  console.log(splittedStrings);

  return splittedStrings
}


function process(maze, start, end) {
  const [startX, startY] = start;
  const [endX, endY] = end;

  const queue = [];
  let minimalPathSum;
  const visited = {};

  queue.push([[startX, startY], null, 0])

  while (queue.length > 0) {
    let [[x, y], prev, sum] = queue.shift();

    if (!(x >=0 && y >= 0 && x <= endX && y <= endY)) {
      continue
    }
    
    if (prev) {
      const [prevX, prevY] = prev;
      if (visited[`${prevX},${prevY}`] && visited[`${prevX},${prevY}`] < sum - maze[x][y]) {
        continue;
      }
    }

    if (visited[`${x},${y}`] && visited[`${x},${y}`] <= sum) {
      continue;
    }
    
    if (x === endX && y === endY) {
      if (!minimalPathSum || sum < minimalPathSum) {
        minimalPathSum = sum;
        console.log('tmp sum', sum);
      }

      continue;
    }

    visited[`${x},${y}`] = sum;

    for (let [deltaI, deltaJ] of [[1, 0], [0, 1], [-1, 0], [0, -1]]) {
      const i = x + deltaI;
      const j = y + deltaJ;
      if (!(i >= 0 && j >= 0 && i <= endX && j <= endY) || (visited[`${x},${y}`] && visited[`${i},${j}`] <= sum)) continue;

      queue.push([[i, j], [x, y], sum + maze[i][j]]);
    }
  }

  return minimalPathSum;
}

function repeatMatrix(values, times) {
  let height = values.length;
  let width = values[0].length;
  for (let row = 0; row < times; row++) {
    for (let col = 0; col < times; col++) {
      if (row === 0 && col === 0) continue;
      const sourceRow = row > 0 ? row - 1 : row;
      const sourceCol = row > 0 ? col : col - 1;

      for (let i = 0; i < height; i++) {
        for (let j = 0; j < width; j++) {
          if (!values[height * row + i]) {
            values[height * row + i] = [];
          }
          const newValue = values[height * sourceRow + i][width * sourceCol + j] + 1;
          values[height * row + i][width * col + j] = newValue > 9 ? 1 : newValue;
        }
      }
    }
  }
  console.log(values);
  return values;
}

console.log(`Processing results for path: ${path}`);

const inputData = await processFile(path);
const extendedInputData = repeatMatrix(inputData, 5);
console.log(extendedInputData);

// const result = process(inputData, [0, 0], [inputData.length - 1, inputData[0].length - 1]);
const result2 = process(extendedInputData, [0, 0], [extendedInputData.length - 1, extendedInputData[0].length - 1]);

// console.log(`Result 1: ${result}`);
console.log(`Result 2: ${result2}`);
