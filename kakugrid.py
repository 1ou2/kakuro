from curses.ascii import isdigit
import random

class KakuroGrid:
    def __init__(self, size=10,fpath=None,bcells=0.3,maxattempts=5):

        if fpath is not None:
            self.load(fpath)
        else:
            # size of the grid
            self.N = size
            # % of blacks cells (full black or with clues) in the grid
            self.blackcells = bcells
            # when trying to fill the grid number of attempts to try
            self.maxattempts = maxattempts

            self.grid = [[None for _ in range(self.N)] for _ in range(self.N)]
            self.vgrid = [[None for _ in range(self.N)] for _ in range(self.N)]
            self.hgrid = [[None for _ in range(self.N)] for _ in range(self.N)]

            # set top row and left column to black cells
            for i in range(self.N):
                self.set_value(0,i,"B/B")
                self.set_value(i,0,"B/B")

    def get_value(self,r,c):
        return self.grid[r][c]
    
    def isClue(self,r,c):
        return not str(self.grid[r][c]).isdigit()
    
    def formatline(self,row):
        line = ""
        for e in row:
            if e == "B/B":
                line = line + "B" + " "
            elif str(e).startswith("V") or str(e).startswith("H"):
                line = line + e[1:] + " "
            else:
                line = line + "." + " "
        return line
    
    # returns a string containing the kakuro problem
    def serialize_problem(self):
        pb = "(solve "+ str(self.N)+"\n"
        
        for i,row in enumerate(self.hgrid):
            # skip first row that contains only a line of "B"
            if i == 0:
                continue
            line = self.formatline(row)
            # last line
            if i == self.N-1:
                line = line +"/"
            pb = pb + line+"/\n"
            pb = pb + "\n"
        for c in range(1,self.N):
            row = list()
            for r in range(self.N):
                row.append(self.vgrid[r][c])
        
            # remove first element that contains a "B"
            #row = row[1:]
            line = self.formatline(row)
            #last line
            if c == self.N -1:
                line = line +"/"
            pb = pb + line+"/\n"

        pb = pb + ")\n\n"
        return pb       

    def serialize_solution(self):
        sol = ""
        for r in range(self.N):
            row = ""
            for c in range(self.N):
                row = row + "{:>8}".format(self.grid[r][c])
            sol = sol + row + "\n"     
        sol = sol + "\n\n"
        return sol

    # write kakuro grid and solution to file
    # 2 files are created:
    #  - filename : the problem
    #  - sol-filename : the solution
    #   
    def write(self,filename):
        with open(filename,'w') as fpb:
            fpb.write("(solve "+ str(self.N)+"\n")
            
            for i,row in enumerate(self.hgrid):
                # skip first row that contains only a line of "B"
                if i == 0:
                    continue
                line = self.formatline(row)
                # last line
                if i == self.N-1:
                    line = line +"/"
                fpb.write(line+"/\n")
            fpb.write("\n")
            for c in range(1,self.N):
                row = list()
                for r in range(self.N):
                    row.append(self.vgrid[r][c])
            
                # remove first element that contains a "B"
                #row = row[1:]
                line = self.formatline(row)
                #last line
                if c == self.N -1:
                    line = line +"/"
                fpb.write(line+"/\n")

            fpb.write(")\n\n")
            
        with open("sol-"+filename,"w") as fsol:
            for r in range(self.N):
                row = ""
                for c in range(self.N):
                    row = row + "{:>8}".format(self.grid[r][c])
                fsol.write(row+"\n")     
            fsol.write("\n\n")

    def load(self,filename):
        with open(filename,'r') as fpb:
            lines = fpb.readlines()
            # first line is "(solve XXX" where XXX is the size of the grid
            size = lines[0].split()[1]
            self.N = int(size)
            isHorizontal = True
            r = 0
            c = 0
            for line in lines[1:]:
                # end of the grid
                if line.strip() == ")":
                    break
                if line.strip().endswith("/"):
                    l1 = line.replace("/","")
                    l2 = l1.replace(".","B/B")
                    vals = l2.split()
                    for c, v in enumerate(vals):
                        if isdigit(v):
                            v = int(v)
                        self.grid[r][c] = v
                    r = r+1
                # first section is the horizontal zone
                # this zone ends with a double slash
                # from there we will be parsing the vertical zone
                if line.strip().endswith("//"):
                    isHorizontal = False


    def set_value(self,r,c,val):
        
        if str(val).isdigit() or val == "B/B":
            self.grid[r][c] = val
            self.vgrid[r][c] = val
            self.hgrid[r][c] = val

        else:
            if val.startswith("V"):
                self.vgrid[r][c] = val
                # grid contains Horizontal / Vertical clue
                if "/" in str(self.grid[r][c]):
                    clues = self.grid[r][c].split("/")
                    self.grid[r][c] = clues[0] + "/" + val
                else:
                    self.grid[r][c] = "B/" + val
                
            if val.startswith("H"):
                self.hgrid[r][c] = val
                # grid contains Horizontal / Vertical clue
                if "/" in str(self.grid[r][c]):
                    clues = self.grid[r][c].split("/")
                    self.grid[r][c] = val + "/" + clues[1]
                else:
                    self.grid[r][c] = val + "/B"


    def fill_grid(self):
        # fill in the rest of the grid
        for i in range(1, self.N):
            for j in range(1, self.N):
                valid_values = set(range(1, 10)) - {self.grid[i][j-1], self.grid[i-1][j]} if i > 0 or j > 0 else set(range(1, 10))
                val = random.choice(list(valid_values))
                self.set_value(i,j,val)

    def fill_black(self):
        for i in range(1, self.N):
            for j in range(1, self.N):
                if random.random() < self.blackcells:
                    self.set_value(i,j,"B/B")

    # Add clues to the grid
    #  - V12: Vertical 12 - means a sum of 12 in vertical
    #  - H13: Horizontal 13 
    #
    # returns True if ok
    # returns False if the clues cannot be filled           
    def fill_clues(self):
        for c in range(self.N):
            total = 0
            nb_elem = 0
            # fill vertical clues
            for r in range(self.N):
                if self.isClue(r,c):
                    # next row is a digit
                    if r < self.N -1 and not self.isClue(r+1,c):
                        for k in range(r+1,self.N):
                            if not self.isClue(k,c):
                                total = total + self.grid[k][c]
                                nb_elem = nb_elem +1
                            # either this cell is a clue or the last cell
                            # set the value of the clue
                            if self.isClue(k,c) or k == self.N -1:
                                if nb_elem > 1:
                                    self.set_value(r,c,"V"+str(total))
                                total = 0
                                break

        # fill horizontal clues
        for r in range(self.N):
            total = 0
            nb_elem = 0
            for c in range(self.N):
                if self.isClue(r,c):
                    # next row is a digit
                    if c < self.N -1 and not self.isClue(r,c+1):
                        for k in range(c+1,self.N):
                            if not self.isClue(r,k):
                                total = total + self.grid[r][k]
                                nb_elem = nb_elem +1
                            # either this cell is a clue or the last cell
                            # set the value of the clue
                            if self.isClue(r,k) or k == self.N -1:
                                if nb_elem > 1:
                                    self.set_value(r,c,"H"+str(total))                            
                                total = 0                                
                                break

        return True

    
    def check_zone(self,vals,nb_elem):
        if nb_elem == 1:
            return True
        
        if nb_elem > 9:
            raise Exception("Too many values, a zone cannot contain more than 9 cells")
        
        if nb_elem != len(vals):
            return False

        return True

    # change the digits in a zone so that it respects a zone constraints
    # all digits in a zone must be different
    def change_zone(self,nb_elem,r,c,isVertical=False,isHorizontal=False):
        assert(isVertical != isHorizontal)
        assert(nb_elem <= 9)    
        
        # one element, nothing to change, it is not a zone
        if nb_elem == 1:
            return True
        
        # values used in this zone
        zvals = set()
        for i in range(nb_elem):
            # vertical zone starting at cell (r,c) -> (r+1,c) (r+2,c) .... 
            if isVertical:
                hvals = set()
                # what are the elements at left of (r+i,c) -> (r+i,c-1), (r+i,c-2), ...
                if c > 1:
                    for k in range(c):
                        cleft = c -k-1
                        if not self.isClue(r+i+1,cleft):
                            hvals.add(self.get_value(r+i+1,cleft))
                        else:
                            break
                if c < self.N -1:
                    for cright in range(c+1,self.N):
                        if not self.isClue(r+i+1,cright):
                            hvals.add(self.get_value(r+i+1,cright))
                        else:
                            break
                possiblevals = set([1,2,3,4,5,6,7,8,9]) - hvals -zvals
                if len(possiblevals) == 0:
                    return False
                else:
                    val = random.choice(list(possiblevals))
                    zvals.add(val)
                    self.set_value(r+i+1,c,val)
            if isHorizontal:
                vvals = set()
                # what are the elements at the top of (r,c+1) -> (r-1,c+i), (r-2,c+i), ...
                if r > 1:
                    for k in range(r):
                        rtop = r -k-1
                        if not self.isClue(rtop,c+i+1):
                            vvals.add(self.get_value(rtop,c+i+1))
                        else:
                            break
                if r < self.N -1:
                    for rbottom in range(r+1,self.N):
                        if not self.isClue(rbottom,c+i+1):
                            vvals.add(self.get_value(rbottom,c+i+1))
                        else:
                            break
                possiblevals = set([1,2,3,4,5,6,7,8,9]) - vvals -zvals
                if len(possiblevals) == 0:
                    return False
                else:
                    val = random.choice(list(possiblevals))
                    zvals.add(val)
                    self.set_value(r,c+i+1,val)
                        
        return True
                
    
    
    def change_isolated(self):
        for r in range(self.N):
            for c in range(self.N):
                # check that this digit is not isolated
                # it should have a digit next to him 
                if not self.isClue(r,c):
                    isolated = True
                    if r > 0 and not self.isClue(r-1,c):
                        isolated = False
                    if r < self.N - 1 and not self.isClue(r+1,c):
                        isolated = False
                    if c > 0 and not self.isClue(r,c-1):
                        isolated = False
                    if c < self.N - 1 and not self.isClue(r,c+1):
                        isolated = False
                    if isolated:
                        #print("Cell isolated " + str(r) + " - " + str(c))
                        self.set_value(r,c,"B/B")


    # TODO : rewrite 
    # either split verify and correct code , or return code true (nothing changed), and use exception if grid cannot be filled
    # here after horizontal_verify, the digits are changed and vertical must be checked again !
    # if verticalverify and horizontal verify are o
    def check_grid(self):
        maxattempts = self.maxattempts
        nochange = False
        while maxattempts >0:
            maxattempts = maxattempts - 1
            if nochange == True:
                break

            nochange = True
            # vertical clues
            for c in range(self.N):
                nb_elem = 0
                vals = set()
                for r in range(self.N):
                    if self.isClue(r,c):
                        # next row is a digit
                        if r < self.N -1 and not self.isClue(r+1,c):
                            for k in range(r+1,self.N):
                                if not self.isClue(k,c):
                                    nb_elem = nb_elem +1
                                    vals.add(self.grid[k][c])
                                # either this cell is a clue or the last cell
                                # set the value of the clue
                                if self.isClue(k,c) or k == self.N -1:     
                                    if not self.check_zone(vals,nb_elem):
                                        self.change_zone(nb_elem,r,c,isVertical=True)
                                        nochange = False
                                    nb_elem = 0
                                    vals = set()
                                    break

            # fill horizontal clues
            for r in range(self.N):
                nb_elem = 0
                vals = set()
                for c in range(self.N):
                    if self.isClue(r,c):
                        # next row is a digit
                        if c < self.N -1 and not self.isClue(r,c+1):
                            for k in range(c+1,self.N):
                                if not self.isClue(r,k):
                                    nb_elem = nb_elem +1
                                    vals.add(self.grid[r][k])
                                # either this cell is a clue or the last cell
                                # set the value of the clue
                                if self.isClue(r,k) or k == self.N -1:
                                    if not self.check_zone(vals,nb_elem):
                                        self.change_zone(nb_elem,r,c,isHorizontal=True)
                                        nochange = False                          
                                    nb_elem = 0
                                    vals = set()
                                    break

        return nochange

    


                        
    def print_one_grid(self,g):
        for r in range(self.N):
            row = ""
            for c in range(self.N):
                row = row + "{:>8}".format(g[r][c])
            print(row)     
        print("\n\n")

    def print_grids(self):
        self.print_one_grid(self.grid)
        #self.print_one_grid(self.vgrid)
        #self.print_one_grid(self.hgrid)

    def fill(self):
        self.fill_grid()
        self.fill_black()
        self.change_isolated()
        if self.check_grid():
            self.fill_clues()
            return True
        else:
            return False

if __name__ == '__main__':
    kakuro = KakuroGrid(10)
    print(" -- 1")
    kakuro.fill_grid()
    #kakuro.print_grids()

    #print(" -- 2")
    kakuro.fill_black()
    #kakuro.print_grids()

    print(" -- 3")
    kakuro.change_isolated()
    #kakuro.print_grids()


    print(" -- 4 " )
    isOK = kakuro.check_grid()
    print(" isOK : " , isOK)
    #kakuro.print_grids()

    print(" -- 5 " )
    kakuro.fill_clues()
    kakuro.print_grids()


    #kakuro.write("test.clp")

