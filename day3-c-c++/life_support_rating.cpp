#include <fstream>
#include <functional>
#include <iostream>
#include <vector>

int calculateLifeValue(std::vector<std::string> lifeAccumulator, std::function<int(int, int)> compare, bool fill = 0) {
  unsigned int result = 0;

  std::vector<std::string> accumulator = lifeAccumulator;

  int length = accumulator[0].length();

  for (int i = 0; i < length; i++) {
    std::vector<std::string> startsWithOne;
    std::vector<std::string> startsWithZero;

    if (accumulator.size() == 1) {
      for (int j = i; j < length; j++) {
        int bit = accumulator[0][j] == '1' ? 1 : 0;
        result |= bit << (length - j - 1);
      }
      break;  
    }

    for (std::string value : accumulator) {
      if (value[i] == '1') {
        startsWithOne.push_back(value);
      } else {
        startsWithZero.push_back(value);
      }
    }

    int compareResult = compare(startsWithOne.size(), startsWithZero.size());

    if (compareResult == 0) {
      result |= fill << (length - i - 1);
      accumulator = fill == 1 ? startsWithOne : startsWithZero;
      continue;
    }
    if (compareResult > 0) {
      accumulator = startsWithOne;
      result |= 1 << (length - i - 1);    
      continue;
    }

    accumulator = startsWithZero;
  }

  return result;
}

int main(int argc, char** argv) {
  const int INPUT_LINE_SIZE = 12;

  char* path = argv[1];
  if (!path) {
    std::cerr << "No file name provided" << std::endl;
    return -1;
  }

  std::ifstream fileStream(path);

  std::string line;

  std::vector<std::string> accumulator;

  while (std::getline(fileStream, line)) {
    accumulator.push_back(line);
  }

  int oxygen = calculateLifeValue(accumulator, [](int a, int b) { return a - b; }, 1);
  int co2 = calculateLifeValue(accumulator, [](int a, int b) { return b - a; });

  std::cout << "Oxygen(bits): " << std::bitset<INPUT_LINE_SIZE>(oxygen) << "; CO2(bits): " << std::bitset<INPUT_LINE_SIZE>(co2) << std::endl;
  std::cout << "Oxygen: " << oxygen << "; CO2: " << co2 << std::endl;
  std::cout << "Life Support Rating: " << oxygen * co2 << std::endl;

  return 0;
}
