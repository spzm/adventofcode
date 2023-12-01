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
  const splittedStrings = strings.map(str => {
    const [left, right] = str.split('-')
    return nodeTypes.START(right) ? [right, left] : [left, right];
  });

  const connectionsMap = {};

  splittedStrings.forEach(([left, right]) => {
    if (!connectionsMap[left]) {
      connectionsMap[left] = []; 
    }

    if (!connectionsMap[right]) {
      connectionsMap[right] = []; 
    }

    connectionsMap[left].push(right);
    connectionsMap[right].push(left);
  });

  return connectionsMap;
}


function findPassagePaths(connections, firstSmallVisitedTwice = false) {
  const queue = [];
  const paths = [];

  queue.push(['start', ['start'], {}, firstSmallVisitedTwice]);

  while (queue.length > 0) {
    let [currentNode, path, visited, firstSmallCave] = queue.pop();

    if (!connections[currentNode]) {
      continue
    }

    if (visited[currentNode]) {
      if (!firstSmallCave) {
        firstSmallCave = true;
      } else {
        continue;
      }
    }

    if (nodeTypes.END(currentNode)) {
      paths.push(path); 
      continue;
    }

    if (nodeTypes.SMALL_CAVE(currentNode)) {
      visited[currentNode] = true;
    }

    for (let right of connections[currentNode]) {
      if ((visited[right] && firstSmallCave) || !connections[right] || nodeTypes.START(right)) continue;

      queue.push([right, [...path, right], { ...visited }, firstSmallCave]);
    }
  }

  return paths.length;
}

console.log(`Processing results for path: ${path}`);

const connectionsMap = await processFile(path);

const possiblePaths = findPassagePaths(connectionsMap, true);
const possiblePathsWithFirstSmallTwice = findPassagePaths(connectionsMap);

console.log(`Possible paths: ${possiblePaths}`);
console.log(`Possible paths with small visited twice: ${possiblePathsWithFirstSmallTwice}`);
