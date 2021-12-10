#!/usr/bin/bash

# https://dotnet.microsoft.com/en-us/download/dotnet/6.0

(
  cd solution
  dotnet run ../example.txt
)

echo ""

(
  cd solution
  dotnet run ../data.txt
)