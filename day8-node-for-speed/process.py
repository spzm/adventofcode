import sys

def count_decreases_average(file_name: str, window: int):
  file = open(file_name, 'r')
  previous_lines = [int(file.readline()) for x in range(window)]
  decreases = 0

  while True:
    line = file.readline()
    if not line:
      break

    lines = previous_lines[1:]
    lines.append(int(line))

    if sum(lines) > sum(previous_lines):
      decreases += 1
    
    previous_lines = lines
  
  return decreases


if __name__ == "__main__":
  path = sys.argv[1]
  if path == None:
    print('No file name provided')
    sys.exit()
  
  print('Processing results for path: {}'.format(path))
  print('Depth increasing times: {}'.format(count_decreases_average(path, 1)))
  print('3-measurement sliding window: {}\n'.format(count_decreases_average(path, 3)))


