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

  return dataString.split(',').map(value => Number.parseInt(value, 10));
}

function leastFuel(crabs) {
  const sortedCrabs = crabs.sort((a, b) => a - b);

  const median = Math.floor((sortedCrabs.length / 2));
  const left = sortedCrabs.slice(0, median);
  const leftSum = left.reduce((acc, val) => acc + val, 0);
  const right = sortedCrabs.slice(median + 1, sortedCrabs.length);
  const rightSum = right.reduce((acc, val) => acc + val, 0);

  return Math.abs(leftSum - (left.length * sortedCrabs[median])) + Math.abs(rightSum - (right.length * sortedCrabs[median]));
}

function getFuelTravelValue(n) {
  return n + ((n - 1) / 2) * n;
}

function leastFuelWithStepValue(crabs) {
  const max = Math.max(...crabs);
  let min;

  for (let i = 0; i < max; i++) {
    const fuel = crabs.reduce((acc, value) => acc + getFuelTravelValue(Math.abs(value - i)), 0)

    if (!min || fuel < min.value) {
      min = {
        index: i,
        value: fuel
      }
    }
  }

  return min.value;
}

console.log(`Processing results for path: ${path}`);

const inputData = await processFile(path);
console.log(`Fuel for crabs with zero movement cost: ${leastFuel(inputData.map(v => v))}`);
console.log(`Fuel for crabs with progressive movement cost: ${leastFuelWithStepValue(inputData)}`);