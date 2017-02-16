from collections import namedtuple
from enum import Enum

OpTree = namedtuple("OpTree", "op left right")


def solve(numbers, target):
  print 'Solving', target, numbers
  if len(numbers) == 1:
    if numbers[0] == target:
      return numbers[0]
    else:
      return None
      
  for i, n in enumerate(numbers):
    n = numbers[i]
    sub_numbers = numbers[0:i] + numbers[i+1:]
    
    # target = n + sub_target
    sub_target = target - n
    t = solve(sub_numbers, sub_target)
    if t is not None:
      return OpTree("+", n, t)
    
    # target = sub_target - n  
    sub_target = target + n  
    t = solve(sub_numbers, sub_target)
    if t is not None:
      return OpTree("-", t, n)

    # target = n - sub_target
    sub_target = n - target  
    t = solve(sub_numbers, sub_target)
    if t is not None:
      return OpTree("-", n, t)    
      
    # target = n * sub_target
    if target % n == 0:
      sub_target = target / n
      t = solve(sub_numbers, sub_target)
      if t is not None:
        return OpTree("*", n, t)  
        
    # target = n / sub_target
    if n % target == 0:
      sub_target = n / target
      t = solve(sub_numbers, sub_target)
      if t is not None:
        return OpTree("/", n, t)  
        
    # target = sub_target / n
    sub_target = n * target
    t = solve(sub_numbers, sub_target)
    if t is not None:
      return OpTree("/", t, n) 
   
  return None
  
def op_prio(op):
  if op == '*' or op == '/':
    return 2
  elif op == '+' or op == '-':
    return 1
  else:
    raise Exception("Not an Op")
  
def _print_child(parent, child):
  if type(child) ==  OpTree:
    if op_prio(parent.op) > op_prio(child.op):
      print "(",
    print_optree(child)
    if op_prio(parent.op) > op_prio(child.op):
      print ")",
  else:
    print child,
      
def print_optree(root):
  if type(root) == int:
    print root,
  elif type(root) == OpTree:
    _print_child(root, root.left)
    print root.op, 
    _print_child(root, root.right)
  else:
    raise Exception("Error OpTree")
    
s1 = solve([1, 2, 5, 8], 24)
if s1 is None:
  print 'FAILED'
else:
  print_optree(s1)
