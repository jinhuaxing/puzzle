#!/usr/bin/node
const print = process.stdout.write.bind(process.stdout);

function _FT(op, left, right) { 
  return {op, left, right}; 
}

function op_prio(op) {
  if (op === '*' || op === '/') {
    return 2;
  } else if (op === '+' || op === '-') {
    return 1;
  } else {
    throw "Not an OpTree";
  }
}

function _print_child(parent, child) {
  if (typeof child === 'object') {
    const parenthesis  = op_prio(parent.op) > op_prio(child.op);
    if (parenthesis) {
      print("(");
    }
    print_optree(child);
    if (parenthesis) {
      print(")");
    }
  } else {
    print(child.toString());
  }
}    

function print_optree(root) {
  if (typeof root === 'number') {
    print(root.toString());
  } else if (typeof root === 'object') {
    _print_child(root, root.left);
    print(root.op);
    _print_child(root, root.right);
  } else {
    throw "Error _FT";
  }
}

function solve(numbers, target) {
  if (numbers.length === 1) {
    if (numbers[0] === target) {
      return numbers[0];
    } else {
      return null;
    }
  }

  for (let i = 0; i < numbers.length; i++) {
    const n = numbers[i];
    const sub_numbers = numbers.slice(0, i).concat(numbers.slice(i+1, numbers.length));    
    // target = n + sub_target
    let sub_target = target - n;
    let t = solve(sub_numbers, sub_target);
    if (t) return _FT("+", n, t);
    
    // target = sub_target - n  
    sub_target = target + n;  
    t = solve(sub_numbers, sub_target);
    if (t) return _FT("-", t, n);

    // target = n - sub_target
    sub_target = n - target;  
    t = solve(sub_numbers, sub_target);
    if (t) return _FT("-", n, t);
      
    // target = n * sub_target
    if (target % n === 0) {
      sub_target = target / n;
      t = solve(sub_numbers, sub_target);
      if (t) return _FT("*", n, t);
    }
    // target = n / sub_target
    if (target !== 0 && n % target === 0) {
      sub_target = n / target;
      t = solve(sub_numbers, sub_target);
      if (t) return _FT("/", n, t);
    }
    // target = sub_target / n
    sub_target = n * target
    t = solve(sub_numbers, sub_target)
    if (t) return _FT("/", t, n);
  }
  return null;
}

const s1 = solve([3, 4, 6, 1], 24);
if (s1) {
  print_optree(s1);
} else {
  console.log('FAILED');
}
