#include <stdio.h>
#include <stdlib.h>


int calculateConsumption(int bitValues[], int length, int totalSize) {
  int gammaRate = 0;
  int epsilonRate = 0;

  int i;
  for (i = 0; i < length; i++) {
    int bit = 1 << (length - 1 - i);

    if (bitValues[i] > totalSize / 2) {
      gammaRate |= bit;
      continue;
    }

    epsilonRate |= bit;
  }

  return gammaRate * epsilonRate;
}


int main(int argc, char** argv) {
  FILE *fp;
  char* line = NULL;
  size_t len = 0;

  char* path = argv[1];
  int length = atoi(argv[2]);

  if (!path) {
    printf("No file name provided");
    exit(EXIT_FAILURE);
  }


  fp = fopen(path, "r");
  if (fp == NULL) {
    printf("Can't open file %s", path);
    exit(EXIT_FAILURE);
  }

  int bitValues[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
  int i;
  int lines = 0;

  while (getline(&line, &len, fp) != -1) {
    for (i = 0; i < length; i++) {
      if (line[i] == '1') {
        bitValues[i]++;
      }
    }
    lines++;
  }
  
  int consumption = calculateConsumption(bitValues, length, lines);
  printf("Processing results for path: %s\n", path);
  printf("Total Consumption: %d\n", consumption);

  fclose(fp);

  return EXIT_SUCCESS; 
}