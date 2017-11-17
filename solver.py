import util
import cube
import copy

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
                newCube.rotate(face, reverse=reverse)
                action = face
                cost = newCube.cost()
                if reverse is True: action += "\'"
                results.append((action, newCube, cost))
        return results

    def stateCost(self):
        return 1


def solve(query):
    ucs = util.UniformCostSearch(verbose=1)
    ucs.solve(RubiksProblem(query))
    return 'Solution: ' + ', '.join(ucs.actions)

if __name__ == '__main__':
    cube = cube.generateCube()
    solution = solve(cube)
    print solution
