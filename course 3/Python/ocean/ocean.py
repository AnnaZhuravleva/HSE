#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import copy


class Ocean:

    def __init__(self, init_state):
        self.state = copy.deepcopy(init_state)
        self.rs = len(init_state)
        self.cs = len(init_state[0])

    def __str__(self):
        return '\n'.join([' '.join([str(i) for i in row])
                          for row in self.state])

    __repr__ = __str__

    def gen_next_quantum(self):
        def neighbours(x, i, j):
            n = [x[r][c] for r in range(i-1, i+2)
                 for c in range(j-1, j+2)
                 if 0 <= r < self.rs and 0 <= c < self.cs
                 and (r, c) != (i, j)]
            return [n.count(2), n.count(3)]

        def new_state(item, neighbours):
            new_item = 0
            if item == 1:
                new_item = 1
            if item == 0 and neighbours[0] == 3:
                new_item = 2
            if item == 2 and (neighbours[0] == 2 or neighbours[0] == 3):
                new_item = 2
            if item == 3 and (neighbours[1] == 2 or neighbours[1] == 3):
                new_item = 3
            return new_item

        next_quantum = []
        for i, v in enumerate(self.state):
            next_quantum.append([new_state(k, neighbours(self.state, i, j))
                                 for j, k in enumerate(v)])
        self.state = next_quantum
        return Ocean(init_state=next_quantum)


if __name__ == '__main__':
    n_quantums = int(sys.stdin.readline())
    n_rows, n_clms = [int(i) for i in sys.stdin.readline().split()]
    init_state = []
    for i in range(n_rows):
        line = [int(i) for i in sys.stdin.readline().split()]
        init_state.append(line)

    ocean = Ocean(init_state=init_state)
    for _ in range(n_quantums):
        ocean = ocean.gen_next_quantum()
    print(ocean)
