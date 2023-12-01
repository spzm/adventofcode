#!/usr/bin/bash

(
  cd solution
  stack build
  echo ""

  stack exec solution ../example.txt

  echo ""

  stack exec solution ../data.txt 
)