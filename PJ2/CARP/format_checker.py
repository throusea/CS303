import argparse
import ast
from typing import List, Tuple

RouteList = List[List[Tuple[int, int]]]

def parse_output(output: List[str]) -> (RouteList, int):
    res: RouteList = []
    output, cost = output[0], output[1]
    output = output.removeprefix('s ').replace('),(', ')|(')
    output = list(filter(lambda x: x != "", output.split(',0,0,')))
    output = [x.removeprefix('0,').removesuffix(',0\n').split('|') for x in output]
    for route in output:
        res.append([])
        for i, pair in enumerate(route):
            res[-1].append(ast.literal_eval(pair.removesuffix(',')))
    return res, int(cost.removeprefix('q '))

if __name__ == '__main__':
    try:
        carp_output = parse_output(open("output").readlines())
        print("Congratulation!")
    except:
        print("Nope!")