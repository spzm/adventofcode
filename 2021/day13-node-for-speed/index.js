import fs from 'fs/promises';
import { argv, exit } from 'process';

const path = argv[2];

if (!path) {
  console.error('No file name provided');
  exit();
}

const nodeTypes = {
  START: value => value === 'start',
  END: value => value === 'end',
  BIG_CAVE: value => /[A-Z]+/.test(value),
  SMALL_CAVE: value => !nodeTypes.START(value) && !nodeTypes.END(value) && /[a-z]+/.test(value)
}

async function processFile(path) {
  let dataString;

  try {
    dataString = await fs.readFile(path, 'utf8');
  } catch(err) {
    console.error('Cannot read file', err);
  }

  const strings = dataString.split('\n');
  const dataSplitIndex = strings.findIndex(value => value === '');
  const coordinateStrings = strings.slice(0, dataSplitIndex);
  const foldStrings = strings.slice(dataSplitIndex + 1, strings.length);

  const coordinates = coordinateStrings.map(str => str.split(',').map(value => + value));
  const folds = foldStrings.map(str => {
    let splitData = str.replace('fold along ', '').split('=')
    return [splitData[0], +splitData[1]];
  });

  return [coordinates, folds];
}

function findMaxCoords(coordinates) {
  let maxX = 0;
  let maxY = 0;

  for (let [x, y] of coordinates) {
    if (x > maxX) maxX = x;
    if (y > maxY) maxY = y;
  }

  return [maxX, maxY];
}

function foldVertical(field, foldLine) {
  const newField = [];
  for (let i = 0; i < field.length; i++) {
    if (!newField[i]) newField[i] = [];
    for (let j = 0; j < foldLine; j++) {
      newField[i][j] = field[i][j] | field[i][foldLine + (foldLine - j)];
    }
  }

  return newField;
}

function foldHorizontal(field, foldLine) {
  const newField = [];
  for (let i = 0; i < foldLine; i++) {
    if (!newField[i]) newField[i] = [];
    for (let j = 0; j < field[0].length; j++) {
      newField[i][j] = field[i][j] | field[foldLine + (foldLine - i)][j];
    }
  }

  return newField;
}

function getFilledFiled(maxX, maxY) {
  const field = [];

  for (let i = 0; i <= maxX; i++) {
    if (!field[i]) field[i] = [];
    for (let j = 0; j <= maxY; j++) {
      field[i][j] = 0;
    }
  }

  return field;
}


function findPassagePaths(coordinates, folds) {
  const [maxX, maxY] = findMaxCoords(coordinates);

  let field = getFilledFiled(maxX, maxY);

  for (let [x, y] of coordinates) {
    field[x][y] = 1;
  }

  for (const [foldAxis, foldValue] of folds) {
    if (foldAxis === 'y') {
      field = foldVertical(field, foldValue);
    } else {
      field = foldHorizontal(field, foldValue);
    }
  }

  let counter = 0;
  for (let line of field) {
    for (let col of line) {
      if (col === 1) {
        counter++;
      }
    }
  }

  return [field, counter];
}

function printField(field) {
  for (let j = 0; j < field[0].length; j++) {
    for (let i = 0; i < field.length; i++) {
      process.stdout.write(`${field[i][j] ? '#' : ' '} `);
    }

    process.stdout.write("\n");
  }
}

console.log(`Processing results for path: ${path}`);

const [connectionsMap, folds] = await processFile(path);

const [,singleFoldCount] = findPassagePaths(connectionsMap, [folds[0]]);
const [resultField] = findPassagePaths(connectionsMap, folds);

console.log(`Single fold points active: ${singleFoldCount}`);
printField(resultField);