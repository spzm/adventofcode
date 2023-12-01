module Main where

import System.Environment(getArgs)
import Data.List(sort)
import Data.Maybe(fromJust)
import Data.Char(toUpper)
import System.Exit(exitWith, ExitCode(ExitFailure))

isOpenBracket :: Char -> Bool
isOpenBracket c = c `elem` "[{(<"

isClosedBracket :: Char -> Bool
isClosedBracket c = c `elem` "]})>"

findClosingCharacter character = fromJust $ lookup character $ zip "[{(<" "]})>"
validate stack character restOfString
  | null stack || character /= head stack   = [character]
  | otherwise               = findNotClosedBrackets' (tail stack) restOfString

findNotClosedBrackets :: String -> String
findNotClosedBrackets = findNotClosedBrackets' ""
findNotClosedBrackets' :: String -> String -> String
findNotClosedBrackets' stack [] = stack
findNotClosedBrackets' stack (character:restOfString)
  | isOpenBracket character     = findNotClosedBrackets' (findClosingCharacter character:stack) restOfString
  | isClosedBracket character   = validate stack character restOfString
  | otherwise                   = [character]

getIncorrectBracketValue :: String -> Int
getIncorrectBracketValue value
  | value == ")"  = 3
  | value == "]"  = 57
  | value == "}"  = 1197
  | value == ">"  = 25137
  | otherwise     = 0

getUnclosedBracketValue :: String -> Int
getUnclosedBracketValue value
  | value == ")"  = 1
  | value == "]"  = 2
  | value == "}"  = 3
  | value == ">"  = 4
  | otherwise     = 0

getCharacters :: Char -> String
getCharacters c = [c]

getUncompletedBracketValues :: String -> [Int]
getUncompletedBracketValues value
  | length value > 1    = map (getUnclosedBracketValue . getCharacters) value
  | otherwise           = []

getUncompletedBracketValue :: String -> Int
getUncompletedBracketValue bracketsLine = do
  let values = getUncompletedBracketValues bracketsLine
  foldl (\x acc -> x * 5 + acc) 0 values

middle :: [Int] -> [Int]
middle values = take (signum((l + 1) `mod` 2 + 1)) $ drop ((l - 1) `div` 2) values
  where l = length values


main :: IO ()
main = do
  args <- getArgs
  if null args
    then do
      putStrLn "No file name provided"
      exitWith(ExitFailure 1)
    else pure ()

  let path = head args
  putStrLn ("Processing results for path:  " ++ path)

  content <- readFile path
  let linesOfFile = lines content
  let result = sum (map (getIncorrectBracketValue . findNotClosedBrackets) linesOfFile)
  putStrLn ("Wrong strings result: " ++ show result)

  let listStr = map findNotClosedBrackets linesOfFile
  let allBracketsValues = map (getUncompletedBracketValue . findNotClosedBrackets) linesOfFile
  let uncompletedBracketsValues = sort (filter (> 0) allBracketsValues)
  putStrLn ("Uncompleted strings result: " ++ show (middle uncompletedBracketsValues))
