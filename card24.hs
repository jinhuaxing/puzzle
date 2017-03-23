data OpTree = Leaf Int
            | Branch Char OpTree OpTree 
            deriving (Show)

opPrio :: Char -> Int
opPrio '+' = 1
opPrio '-' = 1
opPrio '*' = 2
opPrio '/' = 2

showOpTree :: OpTree->String
showOpTree (Leaf x) = show x
showOpTree (Branch op left right) = showChild op left ++ [op] ++ showChild op right
showChild pop child = case child of
    Leaf x -> show x
    Branch op _ _  -> 
          if opPrio pop > opPrio op
          then "(" ++ showOpTree child ++ ")"
          else showOpTree child

solve :: [Int]->Int->Maybe OpTree
solve [x] target = if x == target then Just (Leaf x) else Nothing
solve xs target = solve1 (pickOne xs) target
 
pickOne :: [x]->[(x, [x])]
pickOne xs = pickOne1 (length xs - 1) xs
  where pickOne1 0 (x:xss) = [(x, xss)]
        pickOne1 n xss = (xss!!n, xs1 ++ tail xy1):pickOne1 (n-1) xss
              where (xs1, xy1) = splitAt n xss
              
solve1 :: [(Int, [Int])]->Int->Maybe OpTree
solve1 [] _ = Nothing
solve1 ((n, numbers):xs) target = case subSolve n numbers txs of
             Nothing -> solve1 xs target
             x -> x
             where txs = tryList n target
                  
tryList :: Int->Int->[(Char, Int, Bool)]
tryList n target =
    let xs1 = [('+', target - n, True),
               ('-', target + n, False),
               ('-', n - target, True),
               ('/', n * target, False)]
        xs2 = if target `mod` n == 0 then ('*', target `div` n, True):xs1 else xs1
        xs3 = if target /= 0 && n `mod` target == 0 then ('/', n `div` target, True):xs2 else xs2
    in xs3

subSolve :: Int->[Int]->[(Char, Int, Bool)]->Maybe OpTree
subSolve _ _ [] = Nothing
subSolve n subNumbers ((op, subTarget, leafLeft):xs1) = 
    case solve subNumbers subTarget of
        Nothing -> subSolve n subNumbers xs1
        Just t -> case leafLeft of 
            True -> Just (Branch op (Leaf n) t)
            False -> Just (Branch op t (Leaf n))
main = do
  case opTree of 
    Nothing -> putStrLn "FAILED"
    Just t -> putStrLn $ showOpTree t
  where opTree = solve [4,3,5,1] 24