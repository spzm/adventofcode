import { readLines } from 'https://deno.land/std/io/mod.ts';


type Action = 'up' | 'down' | 'forward';

type Move = {
  action: Action;
  distance: number; 
}

type Position = {
  position: number;
  depth: number;
}

const moveLineRegex = /((?:up)|(?:forward)|(?:down)) (\d.*)/i;

function checkAction(actionString: string): Action | null {
  return actionString === 'up' || actionString === 'down' || actionString === 'forward' ? actionString : null;
}

async function parseMoveFile(filepath: string): Promise<Move[]> | never {
  const file = await Deno.open(filepath, { read: true });
  const moveList: Move[] = [];

  for await (const line of readLines(file)) {
    const result = moveLineRegex.exec(line);

    if (!result) continue;
    const action = checkAction(result[1]); 
    const distance = Number.parseInt(result[2], 10);

    if (!action || Number.isNaN(distance)) continue;

    moveList.push({
      action,
      distance: Number.parseInt(result[2], 10)
    })
  }


  return moveList;
}

function calculateSimplePosition(moveList: Array<Move>): Position {
  let depth = 0;
  let position = 0;

  const actionChanges = {
    'up': (move: Move) => {
      depth = depth > move.distance ? depth - move.distance : 0;
    },
    'down': (move: Move) => {
      depth += move.distance;
    },
    'forward': (move: Move) => {
      position += move.distance;
    }
  };

  for (const move of moveList) {
    actionChanges[move.action](move);
  }

  return {
    position,
    depth
  };
}

function calculatePosition(moveList: Array<Move>): Position {
  let depth = 0;
  let position = 0;
  let aim = 0;

  const actionChanges = {
    'up': (move: Move) => {
      aim -= move.distance;
    },
    'down': (move: Move) => {
      aim += move.distance;
    },
    'forward': (move: Move) => {
      position += move.distance;
      depth += aim * move.distance;
    }
  };

  for (const move of moveList) {
    actionChanges[move.action](move);
  }

  return {
    position,
    depth
  };
}

async function main() {
  const path = Deno.args[0];
  if (!path) {
    console.error('No input name provided')
    return -1;
  }

  const data = await parseMoveFile(path);

  const simplePosition = calculateSimplePosition(data);
  const position = calculatePosition(data);
  
  console.log('Processing results for path: ', path)
  console.log('Simple Position: ', simplePosition.position * simplePosition.depth);
  console.log('Real Position: ', position.position * position.depth, '\n');
}

main();