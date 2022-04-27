import matplotlib.pyplot as plt
import numpy as np
import imageio
import random

class Klotski_board :
    #class attributes :
        #self.board -> the actual disposition of the pieces. A self.height * self.width array containing ints that refers to the different pieces
        #self.visited -> a list of board that have been seen during the exploration to solve the puzzle
        #self.visited_largeur -> same but usefull for width exploration
        #self.iteration -> the maximal depth encountered when looking for the solution
        #self.solved -> the list of board that path from the initial position to the solution if there is one
        #self.two_pieces/self.two_pieces -> list of pieces of length 2/3 used for the piece_attribute function to accelerate exploration
        #self.num_pieces -> number of pieces other than the red car

    #other :
        #the red car is identified by the number 0 and the empty spaces by the number -1 the other cars by int starting at 1
        #the rush hour exit is located at [0, 2]

    #initialize a clear board
    def __init__(self, width = 6, height = 6):
        self.width = width
        self.height = height
        self.board = np.zeros([self.height, self.width])
        self.visited=[]
        self.visited_largeur = []
        self.iteration = 0
        self.solved = []
        self.two_pieces = []
        self.three_pieces = []
    
    #initialize a board from a line such as the ones created in the save function
    def init_line(self, line):
        self.width = 6
        self.height = 6
        b = line.split()
        a = 0
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.board[i, j] = float(b[a])
                a+=1
        self.initial_board = self.board.copy()
        self.num_pieces = int(np.max(self.board))

    #initial known positions for test
    def standard(self) :
        self.board[0, 0] = 1
        self.board[0, 1] = -1
        self.board[0, 2] = -1
        self.board[0, 3] = 2

        self.board[1, 0] = 3
        self.board[1, 1] = 4
        self.board[1, 2] = 5
        self.board[1, 3] = 6

        self.board[2, 0] = 3
        self.board[2, 1] = 7
        self.board[2, 2] = 7
        self.board[2, 3] = 6

        self.board[3, 0] = 8
        self.board[3, 3] = 9

        self.board[4, 0] = 8
        self.board[4, 3] = 9
        self.num_pieces = 9

    def standard2(self) :
        self.board[0, 0] = 1
        self.board[0, 1] = 2
        self.board[0, 2] = 3
        self.board[0, 3] = 4

        self.board[1, 0] = 6
        self.board[1, 1] = -1
        self.board[1, 2] = 3
        self.board[1, 3] = 7

        self.board[2, 0] = 6
        self.board[2, 1] = 8
        self.board[2, 2] = 8
        self.board[2, 3] = 7

        self.board[3, 0] = 9
        self.board[3, 3] = 5

        self.board[4, 0] = 9
        self.board[4, 3] = -1
        self.num_pieces = 9

    def rush_hour(self) :
        self.board[0, 0] = 1
        self.board[0, 1] = 2
        self.board[0, 2] = -1
        self.board[0, 3] = 3
        self.board[0, 4] = 4
        self.board[0, 5] = 4

        self.board[1, 0] = 1
        self.board[1, 1] = 2
        self.board[1, 2] = -1
        self.board[1, 3] = 3
        self.board[1, 4] = -1
        self.board[1, 5] = -1

        self.board[2, 0] = 1
        self.board[2, 1] = 5
        self.board[2, 2] = 5
        self.board[2, 3] = 5
        self.board[2, 4] = 6
        self.board[2, 5] = 7

        self.board[3, 0] = 8
        self.board[3, 1] = 8
        self.board[3, 2] = 0
        self.board[3, 3] = -1
        self.board[3, 4] = 6
        self.board[3, 5] = 7

        self.board[4, 0] = -1
        self.board[4, 1] = -1
        self.board[4, 2] = 0
        self.board[4, 3] = 9
        self.board[4, 4] = 9
        self.board[4, 5] = 7

        self.board[5, 0] = -1
        self.board[5, 1] = 10
        self.board[5, 2] = 10
        self.board[5, 3] = -1
        self.board[5, 4] = 11
        self.board[5, 5] = 11

        self.num_pieces = 11
        self.two_pieces = [0, 2, 3, 4, 6, 8, 9, 10, 11]
        self.three_pieces = [1, 5, 7]

    #create a random starting board
    def generate_random(self):
        self.board.fill(-1)
        rnd = random.randint(1, 5)
        self.board[rnd, 2] = 0
        self.board[rnd-1, 2] = 0
        current_piece = 1
        for i in range(0, self.width):
            for j in range(0, self.height) :
                if (self.board[i, j] == -1) :
                    rnd = random.randint(0, 2)
                    if (rnd == 1) :
                        rnd2 = random.randint(0, 1)
                        if(rnd2 == 0 and i+1<self.width and self.board[i+1, j] == -1):
                            self.board[i, j] = current_piece
                            self.board[i+1, j] = current_piece
                            self.two_pieces.append(current_piece)
                            current_piece += 1
                        elif(rnd2 == 1 and j+1<self.height and self.board[i, j+1] == -1):
                            self.board[i, j] = current_piece
                            self.board[i, j+1] = current_piece
                            self.two_pieces.append(current_piece)
                            current_piece += 1
                    elif(rnd == 2) :
                        rnd2 = random.randint(0, 1)
                        if(rnd2 == 0 and i+2<self.width and self.board[i+1, j] == -1 and self.board[i+2, j] == -1):
                            self.board[i, j] = current_piece
                            self.board[i+1, j] = current_piece
                            self.board[i+2, j] = current_piece
                            self.three_pieces.append(current_piece)
                            current_piece += 1
                        elif(rnd2 == 1 and j+2<self.height and self.board[i, j+1] == -1 and self.board[i, j+2] == -1):
                            self.board[i, j] = current_piece
                            self.board[i, j+1] = current_piece
                            self.board[i, j+2]
                            self.three_pieces.append(current_piece)
                            current_piece += 1
        self.num_pieces = current_piece - 1
        self.initial_board = self.board.copy()

    #write a line with the initial board and a bool for solvability
    def save(self, path) :
        file = open(path, "a")
        bool, i = self.solve_largeur()
        for board in self.visited :
            for i in range(0, self.width):
                for j in range(0, self.height) :
                    file.write(str(board[i, j]))
                    file.write(" ")
            file.write(str(bool))
            file.write("\n")

    #return the pieces types to accelerate comparison when exploring possible combinations
    def piece_attribute(self, piece) :
        if(piece in self.two_pieces):
            return 2
        elif(piece in self.three_pieces):
            return 3
        else :
            return piece

    #used for a better rendering
    def color_pieces(self, piece) :
        if(piece == -1):
            return [0.5, 0.5, 0.5]
        if(piece == 0):
            return [1, 0, 0]
        if(piece == 1):
            return [0.8, 0.8, 0]
        if(piece == 2):
            return [0.3, 0.2, 0]
        if(piece == 3):
            return [0.8, 0.4, 0.5]
        if(piece == 4):
            return [0, 0.8, 0.2]
        if(piece == 5):
            return [1, 0.2, 1]
        if(piece == 6):
            return [0, 1, 0]
        if(piece == 7):
            return [0.4, 0.8, 0.3]
        if(piece == 8):
            return [0, 0.8, 0.8]
        if(piece == 9):
            return [0.4, 0.4, 0.7]
        if(piece == 10):
            return [0.1, 0.1, 0.3]
        if(piece == 11):
            return [1, 1, 1]
        if(piece == 12):
            return [0, 0, 0]
        if(piece == 13):
            return [0.4, 0, 0.6]
        if(piece == 14):
            return [0.9, 0.5, 0.5]
        if(piece == 15):
            return [0.3, 1, 1]
        if(piece == 16):
            return [1, 0.2, 0.2]
        if(piece == 17):
            return [0, 0.7, 1]
        if(piece == 18):
            return [1, 0.3, 1]
        if(piece == 19):
            return [0, 0, 1]

    #used to get a better board when showing
    def colorized(self, board) :
        color = np.zeros([self.width, self.height, 3])
        for i in range(0, self.width):
            for j in range(0, self.height):
                for k in range(0, 3):
                    color[i, j, k] = self.color_pieces(board[i, j])[k]
        return color

    #chek if the actual board has alredy been visited in the depth exploration
    def contains_profondeur(self) :
        if(len(self.visited) == 0):
            return False
        att = self.attribute_board()
        return (self.visited == att).all(1).all(1).any()

    #chek if the actual board has alredy been visited in the width exploration
    def contains_largeur(self) :
        if(len(self.visited_largeur) == 0):
            return False
        att = self.attribute_board()
        return (self.visited_largeur == att).all(1).all(1).any()

    #return the possible moves of a given piece. return a list of 4 bool one for each direction
    def can_move_piece(self, piece) :
        position = []
        moves = []
        for i in range (0, self.height):
            for j in range(0, self.width):
                if(self.board[i, j] == piece):
                    position.append([i, j])
        if(len(position) == 0):
            return []
        else :
            m0 = True
            m1 = True
            m2 = True
            m3 = True
            if(len(position)>1):
                if(position[0][0] == position[1][0]) :
                    m0 = False
                    m2 = False
                else :
                    m1 = False
                    m3 = False
            for [i, j] in position :
                if(i == 0) :
                    m0 = False
                elif(self.board[i - 1, j] != -1 and self.board[i - 1, j] != piece) :
                    m0 = False
                if(j == 0) :
                    m1 = False
                elif(self.board[i, j - 1] != -1 and self.board[i, j - 1] != piece) :
                    m1 = False
                if(i == self.height - 1) :
                    m2 = False
                elif(self.board[i + 1, j] != -1 and self.board[i + 1, j] != piece) :
                    m2 = False
                if(j == self.width - 1) :
                    m3 = False
                elif(self.board[i, j + 1] != -1 and self.board[i, j + 1] != piece) :
                    m3 = False
            if(m0):
                moves.append(0)
            if(m1):
                moves.append(1)
            if(m2):
                moves.append(2)
            if(m3):
                moves.append(3)
            return moves

    #return all the possible moves on the board as a list of [piece, [up, right, down, left]]
    def can_move_board(self) :
        next_moves = []
        for i in range(0, self.num_pieces+1) :
            temp = self.can_move_piece(i)
            if(len(temp)>0) :
                 next_moves.append([i, temp.copy()])
        return next_moves

    #updates the board with the given move (no verification if the move is legal)
    def move(self, piece, direction) :
        position = []
        for i in range (0, self.height):
            for j in range(0, self.width):
                if(self.board[i, j] == piece):
                    position.append([i, j])
                    self.board[i, j] = -1
        for [i, j] in position :
            if(direction == 0):
                self.board[i - 1, j] = piece
            if(direction == 1):
                self.board[i, j - 1] = piece
            if(direction == 2):
                self.board[i + 1, j] = piece
            if(direction == 3):
                self.board[i, j + 1] = piece
    
    #creates a twin board with pieces attributes to accelerate comparison when exploring possible combinations
    def attribute_board(self) :
        att = np.zeros([self.height, self.width])
        for i in range(0, self.height) :
            for j in range(0, self.width):
                att[i, j] = self.piece_attribute(self.board[i, j])
        return att

    #return if the actual position is a winning one
    def finish(self) :
        return (self.board[0, 2] == 0 and self.board[1, 2] == 0)

    #try to solve the problem using depth exploration
    def solve_profondeur(self, depth = 0) :
        self.iteration= max(depth, self.iteration)
        if(self.finish()) :
            self.solved.append(self.board.copy())
            return True
        elif self.contains_profondeur() or depth >350 :
            return False
        else :
            self.visited.append(self.attribute_board())
            for piece, moves in self.can_move_board() :
                for direction in moves :
                    self.move(piece, direction)
                    bool = self.solve_profondeur(depth + 1)
                    if(bool) :
                        self.move(piece, (direction + 2)%4)
                        self.solved.append(self.board.copy())
                        return True
                    else :
                        self.move(piece, (direction + 2)%4)
        return False

    #try to solve the problem using width exploration
    def solve_largeur(self, next_boards = [0]) :
        self.iteration+=1
        print("iteration : ", self.iteration, " got to compute : ", len(next_boards), " boards to go...")
        new_boards = []
        heirs = {}
        if(len(self.visited) == 0) :
            self.visited.append(self.board.copy())
        if(self.finish()) :
            self.solved.append(self.board)
            return True, len(self.solved)
        if(len(next_boards) == 0):
            return False, 0
        else :
            for index in next_boards :
                self.board = self.visited[index].copy()
                for piece, moves in self.can_move_board() :
                    for direction in moves :
                        self.move(piece, direction)
                        if self.finish() :
                            self.solved.append(self.board)
                            self.move(piece, (direction + 2)%4)
                            return True, index
                        if not self.contains_largeur() :
                            self.visited.append(self.board.copy())
                            self.visited_largeur.append(self.attribute_board())
                            new_boards.append(len(self.visited) - 1)
                            heirs[len(self.visited) - 1] = index
                        self.move(piece, (direction + 2)%4)
            bool, ind = self.solve_largeur(new_boards.copy())
            if bool :
                k.solved.append(self.visited[heirs.get(ind)])
            else :
                return False, 0
            return bool, heirs[ind]

k = Klotski_board()
#k.standard2()
#k.rush_hour()
k.generate_random()
plt.imshow(k.colorized(k.board))
plt.show()
k.save("data_base.txt")

for iter in range(0, 50) :
    k.__init__()
    k.generate_random()
    k.save("data_base_cluster.txt")
    print("\n")
    print("iteration ", iter)
    print("\n")
#print(k.solve_largeur())
#print(k.iteration)
#for B in k.solved :
#    plt.imshow(B)
#    plt.show()
#k.move(1, 3)
#print(k.can_move_board())

#for i in range(0, len(k.solved)) :
#    plt.imshow(k.colorized(k.solved[len(k.solved) - 1 - i]))
#    plt.savefig('GIF/klotski_'+str(i)+'.png')

#with imageio.get_writer('mygif.gif', mode='I') as writer:
#    for i in range(0, len(k.solved)):
#        image = imageio.imread('GIF/klotski_'+str(i)+'.png')
#        writer.append_data(image)


#plt.imshow(k.board)
#plt.show()