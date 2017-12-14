import copy, util, random

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

    def __init__(self, randomness=1):
        self.faces = {}
        self.faces['U'] = self.SOLVED_CUBE[0]
        self.faces['L'] = self.SOLVED_CUBE[1]
        self.faces['F'] = self.SOLVED_CUBE[2]
        self.faces['R'] = self.SOLVED_CUBE[3]
        self.faces['B'] = self.SOLVED_CUBE[4]
        self.faces['D'] = self.SOLVED_CUBE[5]

        self.corners = [(('F', 0),('L', 2),('U', 6)), # front top left
                        (('F', 2),('R', 0),('U', 8)), # f-t-r
                        (('F', 6),('L', 8),('D', 0)), # f-b-l
                        (('F', 8),('R', 6),('D', 2)), # f-b-r
                        (('B', 0),('R', 2),('U', 2)), # b-t-l
                        (('B', 2),('L', 0),('U', 0)), # b-t-r
                        (('B', 6),('R', 8),('D', 8)), # b-d-l
                        (('B', 8),('L', 6),('D', 6))] # b-d-r

        self.edges =   [# front
                        (('F', 1),('U', 7)),
                        (('F', 3),('L', 5)),
                        (('F', 5),('R', 3)),
                        (('F', 7),('D', 1)),
                        # back
                        (('B', 1),('U', 1)),
                        (('B', 3),('R', 5)),
                        (('B', 5),('L', 3)),
                        (('B', 7),('D', 7)),
                        # center
                        (('L', 1),('U', 3)),
                        (('L', 7),('D', 3)),
                        (('R', 1),('U', 5)),
                        (('R', 7),('D', 5))]

        self.lastRotation = None
        self.randomize(randomness)

    def randomize(self, randomness):
        possibleMoves = ['L', 'R', 'F', 'B', 'U', 'D']
        moves = []
        print
        print 'Shuffling cube...'
        for i in range(randomness):
            move = random.choice(possibleMoves)
            reverse = random.choice([True, False])
            self.rotate(move, reverse)
            if reverse is True: move += '\''
            moves.append(move)
        print 'Moves: [', ', '.join(moves), ']'
        print

    def rotate(self, face, reverse=False):
        self.lastRotation = (face, reverse)
        faceCopy = list(self.faces[face])

        # hard coding positions on face before and after rotation
        # TODO mathematically calculate position changes
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

        if order is not None: # we rotated a top or bottom face
            for i, face in enumerate(faces):
                for j in order:
                    nextIndex = (i+1)%4
                    if reverse is False:
                        self.faces[face][j] = facesCopy[faces[nextIndex]][j]
                    else:
                        self.faces[faces[nextIndex]][j] = facesCopy[face][j]
        else: # we rotated a side face
            # hard coding positions on adjacent faces before and after rotation
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

    def bottomIsSolved(self):
        # check bottom faces
        uniqueValues = set(self.faces['D'])
        if len(uniqueValues) > 1: return False

        # check bottow row of side faces
        center = 4
        sides = ['L', 'F', 'R', 'B']
        for side in sides:
            face = self.faces[side]
            for pos in range(6, 9):
                if face[pos] != face[center]: return False
        return True

    def bottomTIsSolved(self):
        # check bottom faces
        d = self.faces['D']
        uniqueValues = set([d[1], d[3], d[5], d[7]])
        if len(uniqueValues) > 1: return False

        # check bottow row of side faces
        center = 4
        sides = ['L', 'F', 'R', 'B']
        for side in sides:
            face = self.faces[side]
            if face[7] != face[center]: return False
        return True

    def cost(self):
        cost = 0
        for face in self.faces:
            uniqueValues = set(self.faces[face])
            cost += len(uniqueValues)**2
        return cost

    def cost2(self):
        cost = 0
        center = 4
        for face in self.faces.values():
            for cubie in face:
                if cubie == face[center]: continue
                if abs(cubie - face[center]) == 5 or abs(cubie - face[center]) == 2:
                    cost += 2
                else:
                    cost += 1
        return cost**2

    def __str__(self):
        string = ''
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            string += '\n%s: ' % face
            for value in self.faces[face]:
                string += '%s, ' % value
        return string
