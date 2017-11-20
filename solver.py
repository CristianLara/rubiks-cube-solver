import util, cube, copy, time, sys

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


def solve(query):
    ucs = util.UniformCostSearch(verbose=1)
    start = time.time()
    ucs.solve(RubiksProblem(query))
    end = time.time()
    return ', '.join(ucs.actions), (end - start)

if __name__ == '__main__':
    cube = cube.generateCube()
    solution, duration = solve(cube)
    print 'Took %f seconds to solve' % duration
    print 'Solution: [', solution, ']'
    print
