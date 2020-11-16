# This class keeps track of the blanks and walls in a map.
#   It also keeps track of the number of rows and columns.
class Map:
    def __init__(self, mapTxt, config):
        # These are sets so that it can quickly check if a coordinate is in it.
        self.blanks = set()
        self.walls = set()

        self.makeMap(mapTxt)

    def makeMap(self, mapTxt):
        lines = mapTxt.split('\n')
        cols, rows = lines[0].split(' ')
        self.cols = int(cols)
        self.rows = int(rows)

        i = 1
        while i < len(lines):
            for j in range(len(lines[i])):
                curPiece = lines[i][j]
                if curPiece == '~':
                    self.blanks.add((i-1, j)) # Subtract 1 from i because i started at 1
                else:
                    self.walls.add((i-1, j)) # Subtract 1 from i because i started at 1

            i += 1
