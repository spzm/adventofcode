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

  const splittedString = dataString.split('').map(value => parseInt(value, 16).toString(2).padStart(4, '0')).join('');

  return splittedString
}

const packageProcessingMap = {
  0: values => values.reduce((acc, value) => acc + value, 0),
  1: values => values.reduce((acc, value) => value * acc, 1),
  2: values => Math.min(...values),
  3: values => Math.max(...values),
  5: values => values[0] > values[1] ? 1 : 0,
  6: values => values[0] < values[1] ? 1 : 0,
  7: values => values[0] === values[1] ? 1 : 0,
}

function calculateLiteralValue(binaryString, index) {
  let isLastPackage = false;
  let literalAccumulator = '';

  while (!isLastPackage) {
    if (binaryString[index] === '0') {
      isLastPackage = true;
    }
    index++;

    literalAccumulator += binaryString.slice(index, index + 4);
    index += 4;
  }

  return [parseBinary(literalAccumulator), index];
}

function parseBinary(value) {
  return parseInt(value, 2); 
}

function readPacket(binaryString, index) {
  const packet = {
    version: parseBinary(binaryString.slice(index, index + 3)),
    type:  parseBinary(binaryString.slice(index + 3, index + 6)),
    subPackets: []
  };

  let subIndex = index + 6;

  if (packet.type === 4) {
    const [sum, index] = calculateLiteralValue(binaryString, subIndex);
    packet.totalSum = sum;
    packet.versionsSum = packet.version;

    return [packet, index];
  }

  packet.operatorPacket = parseBinary(binaryString[subIndex]);
  const LOW_OPERATOR_LENGTH = 15;
  const HIGH_OPERATOR_LENGTH = 11;
  const lengthBits = packet.operatorPacket ? HIGH_OPERATOR_LENGTH : LOW_OPERATOR_LENGTH;
  subIndex++;

  const length = parseBinary(binaryString.slice(subIndex, subIndex + lengthBits));
  subIndex += lengthBits;

  if (!packet.operatorPacket) {
    let index = subIndex;

    while (index < subIndex + length) {
      const [pack, deltaIndex] = readPacket(binaryString.slice(index, subIndex + length), 0);
      packet.subPackets.push(pack);
      index += deltaIndex;
    }

    subIndex += length;
  } else {
    let index = subIndex;

    for (let i = 0; i < length; i++) {
      const [pack, deltaIndex] = readPacket(binaryString.slice(index, binaryString.length), 0);
      packet.subPackets.push(pack);
      index += deltaIndex;
    }

    subIndex = index;
  }

  if (packageProcessingMap[packet.type]) {
    const data = packet.subPackets.map(value => value.totalSum);
    packet.totalSum = packageProcessingMap[packet.type](data);
  }
  packet.versionsSum = packet.subPackets.reduce((acc, pack) => acc + pack.versionsSum, 0) + packet.version;

  return [packet, subIndex];
}

console.log(`Processing results for path: ${path}`);


const binaryString = await processFile(path);

const [packet] = readPacket(binaryString, 0);

console.log('Packages versions sum2: ', packet.versionsSum);
console.log('Packages sum: ', packet.totalSum);
