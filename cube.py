import copy
import util

class Cube:

    SOLVED_CUBE = [
        [ 0, 0, 0,
          0, 0, 0,
          0, 0, 0 ],

        [ 1, 1, 1,
          1, 1, 1,
          1, 1, 1 ],

        [ 2, 2, 2,
          2, 2, 2,
          2, 2, 2 ],

        [ 3, 3, 3,
          3, 3, 3,
          3, 3, 3 ],

        [ 4, 4, 4,
          4, 4, 4,
          4, 4, 4 ],

        [ 5, 5, 5,
          5, 5, 5,
          5, 5, 5 ]
    ]

    def __init__(self, faces=SOLVED_CUBE):
        self.faces = {}
        self.faces['U'] = faces[0]
        self.faces['L'] = faces[1]
        self.faces['F'] = faces[2]
        self.faces['R'] = faces[3]
        self.faces['B'] = faces[4]
        self.faces['D'] = faces[5]

    def rotate(self, face, reverse=False):
        faceCopy = list(self.faces[face])
        order = [(0,6), (1,3), (2,0), (3,7), (4,4), (5,1), (6,8), (7,5), (8,2)]
        # rotate the numbers on the face
        for a, b in order:
            if reverse is False:
                self.faces[face][a] = faceCopy[b]
            else:
                self.faces[face][b] = faceCopy[a]

        # rotate the numbers on adjacent faces
        if face == 'U':
            self.rotateAdjacent(['F', 'R', 'B', 'L'], reverse, order=[0, 1, 2])
        elif face == 'D':
            self.rotateAdjacent(['F', 'R', 'B', 'L'], reverse, order=[6, 7, 8])
        elif face == 'F':
            self.rotateAdjacent(['D', 'R', 'U', 'L'], reverse)
        elif face == 'R':
            self.rotateAdjacent(['D', 'B', 'U', 'F'], reverse)
        elif face == 'B':
            self.rotateAdjacent(['D', 'L', 'U', 'R'], reverse)
        elif face == 'L':
            self.rotateAdjacent(['D', 'F', 'U', 'B'], reverse)

    def rotateAdjacent(self, faces, reverse, order=None):
        facesCopy = copy.deepcopy(self.faces)

        if order is not None:
            for i, face in enumerate(faces):
                for j in order:
                    nextIndex = (i+1)%4
                    if reverse is False:
                        self.faces[face][j] = facesCopy[faces[nextIndex]][j]
                    else:
                        self.faces[faces[nextIndex]][j] = facesCopy[face][j]
        else:
            order = [[0, 1, 2], [6, 3, 0], [8, 7, 6], [2, 5, 8]]
            for i, face in enumerate(faces):
                for j in range(len(order[0])):
                    nextIndex = (i+1)%4
                    if reverse is False:
                        self.faces[face][order[i][j]] = facesCopy[faces[nextIndex]][order[nextIndex][j]]
                    else:
                        self.faces[faces[nextIndex]][order[nextIndex][j]] = facesCopy[face][order[i][j]]

    SOLUTION = set( tuple(i) for i in [ [i for j in range(9)] for i in range(6)] )

    def isSolved(self):
        faces = set(tuple(i) for i in self.faces.values())
        return faces == self.SOLUTION

    def cost(self):
        cost = 0
        for face in self.faces:
            uniqueValues = set(self.faces[face])
            cost += len(uniqueValues)**2
        return cost


def generateCube():
    cube = Cube()
    cube.rotate('F')
    cube.rotate('U')
    cube.rotate('R')
    cube.rotate('U')
    cube.rotate('R')
    cube.rotate('R')
    return cube
