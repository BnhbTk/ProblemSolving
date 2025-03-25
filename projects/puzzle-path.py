from __future__ import annotations
import copy
import hashlib


class Grid:
    def __init__(self,board:list[list[int]]):
        """This is the constructor of a puzzle. It takes a matrix to initialize the board

        Args:
            board (list[list[int]]): the initial board
        """
        self.board=copy.deepcopy(board)
        self.parent=None
        self.depth=0
        hash(self)
    
    def set_row_col(self,row:int,col:int):
        """This methods sets the starting point

        Args:
            row (int): row of the starting point
            col (int): column of the starting point
        """
        self.row=row
        self.col=col
        self.board[row][col]=2
    
    def __stringify_grid(grid) -> str:
        """This is a utility function to produce a pretty representation of the board

        Args:
            grid (_type_): a board

        Returns:
            str: a pretty representation of the grid
        """
        chars=" ~#"
        return "\n".join(["".join([f"[{chars[c]}]" for c in row]) for row in grid])

    def __str__(self) -> str:
        """Utility function to have a string representation of the puzzle

        Returns:
            str: the string representation
        """
        return Grid.__stringify_grid(self.board)
    
    def __hash__(self) -> int:
        """Computes the hash code of the puzzle in order to accelerate puzzle comparison. This methods uses
        the MD5 function to compute a hash code.

        Returns:
            int: the hash code
        """
        s="".join(["".join([f"{c}" for c in row]) for row in self.board])
        self.__hash_code=int.from_bytes(hashlib.md5(s.encode()).digest(),"little")
        return self.__hash_code
    
    def __eq__(self, value:Grid) -> bool:
        """Tests whether two grids are equal.

        Args:
            value (Grid): the grid to be compared to

        Returns:
            bool: the result of the comparison
        """
        return self.__hash_code==value.__hash_code
    
    def clone(self,row:int,col:int) -> Grid:
        """Creates a copy of the current puzzle and set the current position to (row,col)

        Args:
            row (int): the row of the new position
            col (int): the column of the new position

        Returns:
            Grid: _description_
        """
        v=Grid(self.board)
        v.set_row_col(row,col)
        hash(v)
        v.parent=self
        v.depth=self.depth+1
        return v
    
    def is_goal(self) -> bool:
        """Tests if the current puzzle is the goal (it does not contains 1)

        Returns:
            bool: True if if is the goal, False otherwise
        """
        for row in self.board:
            if 1 in row:
                return False
        return True
    
    def actions(self) -> list[Grid]:
        """This function generates possible actions from the current puzzle. Each element in the return list is new puzzle

        Returns:
            list[Grid]: the list of the new puzzles
        """
        tries=[]
        if self.row>0 and self.board[self.row-1][self.col]==1:
            tries.append((self.row-1,self.col))
        if self.row<len(self.board)-1 and self.board[self.row+1][self.col]==1:
            tries.append((self.row+1,self.col))
        if self.col>0 and self.board[self.row][self.col-1]==1:
            tries.append((self.row,self.col-1))
        if self.col<len(self.board[0])-1 and self.board[self.row][self.col+1]==1:
            tries.append((self.row,self.col+1))
        
        res=[]
        for row1,col1 in tries:
            v=self.clone(row1,col1)
            res.append(v)
        return res
    
    def solve_breadth(self):
        """Solve the problem with a Breadth First Algorithm
        """
        # TODO
        ...
    
    def solve_depth(self):
        """Solve the problem with a Depth First Algorithm
        """
        # TODO
        ...
    
    def solve_random(self):
        """Solve the problem with a Random Algorithm (based on the Open/Closed algorithm)
        """
        # TODO
        ...

    
    def solve_heur(self):
        """Solve the problem with a Heuristic Algorithm according to what has been explained in the statements
        """
        # TODO
        ...
    

def solve_rec(world,row:int,col:int,nb:int,n:int) -> int:
    """This function solves the problem with a backtracking recursive algorithm. It should be used to compute
    the values p_k (as explained in the statements). p_k=n-solve_rec(world,x,y,0,n), such as n is the initial number
    of 1s in the world variable.
    <br>
    To use this function, you should prepare a k*k matrix (called world here) around the current position (x,y) from the puzzle (k=3 or 5). You should
    count the number of 1s in the world (let it be n) then compute the value n-solve_rec(world,x,y,0,n).

    Args:
        world (_type_): a matrix of size k*k to be built
        row (int): the row of the current position
        col (int): the column of the current position
        nb (int): initial number of green cells (should be 0 at the first call)
        n (int): the total number of 1s in the world (the k*k matrix)

    Returns:
        int: the maximum number of blue cells that can be covered
    """
    if nb==n:
        return n
    tries=[]
    if row>0 and world[row-1][col]==1:
        tries.append((row-1,col))
    if row<len(world)-1 and world[row+1][col]==1:
        tries.append((row+1,col))
    if col>0 and world[row][col-1]==1:
        tries.append((row,col-1))
    if col<len(world[0])-1 and world[row][col+1]==1:
        tries.append((row,col+1))
    mx=nb
    for row1,col1 in tries:
        world[row1][col1]=2
        sol=solve_rec(world,row1,col1,nb+1,n)
        world[row1][col1]=1
        if mx<sol:
            mx=sol
        if mx==n:
            return n
        
    return mx



if __name__=="__main__":
    benchmark1=[[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]
    benchmark2=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]]
    benchmark3=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1], [0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1], [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]]
    benchmark4=[[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0], [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    benchmark5=[[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0], [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0], [0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
    benchmark7=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]
    benchmark8=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


    gr=Grid(benchmark1)

    #for all benchmarks, the starting point is (3,3)
    gr.set_row_col(3,3)

    a=gr.solve_depth()
    # a=gr.solve_depth()
    # a=gr.solve_heur()

