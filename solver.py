import util, copy, time, sys
from cube import Cube

class RubiksProblem:
    def __init__(self, cube):
        self.cube = cube
        self.faces = ['L', 'R', 'F', 'B', 'U', 'D']

    def startState(self):
        return self.cube

    def isEnd(self, cube):
        return cube.isSolved()

    def succAndCost(self, cube):
        results = []
        for face in self.faces:
            for reverse in [False, True]:
                newCube = copy.deepcopy(cube)
                newCube.rotate(face, reverse)
                action = face
                cost = newCube.cost()
                if reverse is True: action += "\'"
                results.append((action, newCube, cost))
        return results

class RubiksProblem2:
    def __init__(self, cube):
        self.cube = cube
        self.faces = ['L', 'R', 'F', 'B', 'U', 'D']

    def startState(self):
        return self.cube

    def isEnd(self, cube):
        return cube.isSolved()

    def succAndCost(self, cube):
        results = []
        for face in self.faces:
            for reverse in [False, True]:
                newCube = copy.deepcopy(cube)
                newCube.rotate(face, reverse)
                action = face
                cost = newCube.cost2()
                if reverse is True: action += "\'"
                results.append((action, newCube, cost))
        return results


def solve(cube):
    ucs = util.UniformCostSearch(verbose=1)
    start = time.time()
    ucs.solve(RubiksProblem(cube))
    end = time.time()
    return ', '.join(ucs.actions), (end - start)

def solve2(cube):
    ucs = util.UniformCostSearch(verbose=1)
    start = time.time()
    ucs.solve(RubiksProblem2(cube))
    end = time.time()
    return ', '.join(ucs.actions), (end - start)

if __name__ == '__main__':
    cube = Cube(5)
    # print cube

    solution, duration = solve(cube)
    print 'Took %f seconds to solve full cube #1' % duration
    print 'Solution: [', solution, ']'
    print

    solution, duration = solve2(cube)
    print 'Took %f seconds to solve full cube #2' % duration
    print 'Solution: [', solution, ']'
    print
