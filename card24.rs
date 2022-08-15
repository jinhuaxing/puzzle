type Tree = Box<Node>;

#[derive(Debug, Clone)]
enum Node {
    Leaf(i32),
    NonLeaf {
        op: char,
        value: i32,
        left: Box<Node>,
        right: Box<Node>,
    },
}

impl Node {
    fn get_value(&self) -> i32 {
        match *self {
            Node::Leaf(value) => value,
            Node::NonLeaf { value, .. } => value,
        }
    }
}

fn new_leaf(value: i32) -> Tree {
    Box::new(Node::Leaf(value))
}

fn new_nonleaf(op: char, value: i32, left: Tree, right: Tree) -> Tree {
    Box::new(Node::NonLeaf {
        op,
        value,
        left,
        right,
    })
}

fn solve(numbers: &Vec<i32>, target: i32) {
    if let Some(tree) = solve1(numbers, target)
        .or(solve2(
            numbers[0], numbers[1], numbers[2], numbers[3], target,
        ))
        .or(solve2(
            numbers[0], numbers[2], numbers[1], numbers[3], target,
        ))
        .or(solve2(
            numbers[0], numbers[3], numbers[1], numbers[2], target,
        ))
    {
        print_tree(&tree);
    } else {
        println!("No solution!");
    }
}

fn print_tree(tree: &Tree) {
    match **tree {
        Node::Leaf(value) => {
            print!("{}", value);
        }
        Node::NonLeaf {
            op,
            value: _,
            ref left,
            ref right,
        } => {
            print!("(");
            print_tree(left);
            print!("{}", op);
            print_tree(right);
            print!(")");
        }
    }
}

fn solve1(vec: &Vec<i32>, target: i32) -> Option<Tree> {
    if vec.len() == 1 {
        if vec[0] == target {
            return Some(new_leaf(vec[0]));
        } else {
            return None;
        }
    }

    for (i, n) in vec.iter().enumerate() {
        let mut sub_numbers = Vec::new();
        sub_numbers.extend_from_slice(&vec[..i]);
        sub_numbers.extend_from_slice(&vec[i + 1..]);

        let nl = new_leaf(*n);

        // target = n + sub_target
        if let Some(t) = solve1(&sub_numbers, target - n) {
            return Some(new_nonleaf('+', target, nl, t));
        }

        //target = sub_target - n
        if let Some(t) = solve1(&sub_numbers, target + n) {
            return Some(new_nonleaf('-', target, t, nl));
        }

        //target = n - sub_target
        if let Some(t) = solve1(&sub_numbers, n - target) {
            return Some(new_nonleaf('-', target, nl, t));
        }

        //target = n * sub_target
        if target % n == 0 {
            if let Some(t) = solve1(&sub_numbers, target / n) {
                return Some(new_nonleaf('*', target, nl, t));
            }
        }

        //target = n / sub_target
        if target != 0 && n % target == 0 {
            if let Some(t) = solve1(&sub_numbers, n / target) {
                return Some(new_nonleaf('/', target, nl, t));
            }
        }

        //target = sub_target / n
        if let Some(t) = solve1(&sub_numbers, n * target) {
            return Some(new_nonleaf('/', target, t, nl));
        }
    }
    None
}

fn solve2(one: i32, two: i32, three: i32, four: i32, target: i32) -> Option<Tree> {
    let t1 = build_trees(&new_leaf(one), &new_leaf(two));
    let t2 = build_trees(&new_leaf(three), &new_leaf(four));
    for tt1 in &t1 {
        for tt2 in &t2 {
            for tt in &build_trees(tt1, tt2) {
                if tt.get_value() == target && tt1.get_value() > 0 && tt2.get_value() > 0 {
                    return Some(tt.clone());
                }
            }
        }
    }
    None
}
fn build_trees(left: &Tree, right: &Tree) -> Vec<Tree> {
    let mut trees = Vec::new();

    let lv = left.get_value();
    let rv = right.get_value();

    trees.push(new_nonleaf('+', lv + rv, left.clone(), right.clone()));
    trees.push(new_nonleaf('-', lv - rv, left.clone(), right.clone()));

    if lv != rv {
        trees.push(new_nonleaf('-', rv - lv, right.clone(), left.clone()));
    }
    trees.push(new_nonleaf('*', lv * rv, left.clone(), right.clone()));

    if rv != 0 && lv % rv == 0 {
        trees.push(new_nonleaf('/', lv / rv, left.clone(), right.clone()));
    }

    if lv != rv && lv != 0 && rv % lv == 0 {
        trees.push(new_nonleaf('/', rv / lv, right.clone(), left.clone()));
    }

    trees
}

fn main() {
    solve(&vec![4, 5, 9, 1], 24);
}
