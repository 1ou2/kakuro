import random

class Kakuro:
    def __init__(self, N):
        self.N = N
        self.blackcells = 0.35
        self.grid = [[None for _ in range(N)] for _ in range(N)]
        self.vgrid = [[None for _ in range(N)] for _ in range(N)]
        self.hgrid = [[None for _ in range(N)] for _ in range(N)]

        # set top row and left column to black cells
        for i in range(N):
            self.set_value(0,i,"B/B")
            self.set_value(i,0,"B/B")

    def isClue(self,r,c):
        return not str(self.grid[r][c]).isdigit()
    
    def formatline(self, i,row):
        line = ""
        for e in row:
            if e == "B":
                line = line + e + " "
            elif str(e).startswith("V") or str(e).startswith("H"):
                line = line + e[1:] + " "
            else:
                line = line + "." + " "

        # last line
        if i == self.N -1:
            line = line + "/"

        return line
    

    # write kakuro grid and solution to file
    # 2 files are created:
    #  - filename : the problem
    #  - sol-filename : the solution
    #   
    def write(self,filename):
        with open(filename,'w') as fpb:
            fpb.write("(solve "+ str(self.N)+"\n")
            with open("sol-"+filename,"w") as fsol:
                for i,row in enumerate(self.hgrid):
                    # skip first row that contains only a line of "B"
                    if i == 0:
                        continue
                    line = self.formatline(i,row)
                    fpb.write(line+"/\n")
                    line = ' '.join([str(a) for a in row])
                    if i == self.N -1:
                        line = line + " //\n"
                    else:
                        line = line + " /\n"
                    fsol.write(line)

                fpb.write("\n")
                fsol.write("\n")
                for i,row in enumerate(self.vgrid):
                    # remove first element that contains a "B"
                    row = row[1:]
                    line = self.formatline(i,row)
                    fpb.write(line+"/\n")
                    line = ' '.join([str(a) for a in row])
                    if i == self.N -1:
                        line = line + " //\n"
                    else:
                        line = line + " /\n"
                    fsol.write(line)
                fpb.write(")\n\n")

    def load(self,filename):
        with open(filename,'r') as fpb:
            lines = fpb.readlines()

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

    
                
                
    def vertical_verify(self,rindex,c,nb_elem,vals):
        if len(vals) > 0:
            # only one value, reset to a black cell
            if nb_elem == 1:
                self.set_value(rindex,c, "B/B")
            # zone is too large
            if nb_elem > 9:
                return False
            # we have a digit repeated in this zone
            # it is forbidden by the rules
            if nb_elem != len(vals):
                # generate new distincts elements
                s = set()
                total = 0
                while len(s) < nb_elem:
                    s.add(random.randint(1,9))
                
                for i,v in enumerate(list(s)):
                    total = total + v
                    self.set_value(rindex+i+1,c, v)
                self.set_value(rindex,c,"V" + str(total))
        return True
    
    def horizontal_verify(self,r,cindex,nb_elem,vals):
        if len(vals) > 0:
            # only one value, reset to a black cell
            if nb_elem == 1:
                self.set_value(r,cindex, "B")
            # zone is too large
            if nb_elem > 9:
                return False
            # we have a digit repeated in this zone
            # it is forbidden by the rules
            if nb_elem != len(vals):
                # generate new distincts elements
                s = set()
                total = 0
                while len(s) < nb_elem:
                    s.add(random.randint(1,9))
                
                for i,v in enumerate(list(s)):
                    total = total + v
                    self.set_value(r,cindex+i+1, v)
                self.set_value(r,cindex,"H" + str(total))
        return True
    
    def check_isolated(self):
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
                        print("Cell isolated " + str(r) + " - " + str(c))
                        self.set_value(r,c,"B/B")


    # TODO : rewrite 
    # either split verify and correct code , or return code true (nothing changed), and use exception if grid cannot be filled
    # here after horizontal_verify, the digits are changed and vertical must be checked again !
    # if verticalverify and horizontal verify are o
    def check_grid(self):
        for c in range(self.N):
            nb_elem = 0
            vals = set()
            # fill vertical clues
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
                                if not self.vertical_verify(r,c,nb_elem,vals):
                                    return False
                                total = 0
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
                                if not self.horizontal_verify(r,c,nb_elem,vals):                                    
                                    return False                                
                                nb_elem = 0
                                vals = set()
                                break

        return True

    def check_vclue(self):
        for c in range(self.N):
            vals = set()
            rindex = 0
            nb_elem = 0
            vzone = False
            for r in range(self.N):
                if not vzone and self.isClue(r,c):
                    vzone = True
                    rindex = r
                    vals = set()
                    nb_elem = 0
                if vzone:

                    if str(self.vgrid[r][c]).startswith("B"):
                        if not self.vertical_verify(rindex,c,nb_elem,vals):
                            return False
                        vzone = False
                        rindex = 0
                        vals = set()
                        nb_elem = 0
                        
                    elif str(self.vgrid[r][c]).startswith("V"):
                        if not self.vertical_verify(rindex,c,nb_elem,vals):
                            return False
                        vzone = True
                        rindex = r
                        vals = set()
                        nb_elem = 0
                    else:
                        vals.add(self.vgrid[r][c])
                        nb_elem = nb_elem + 1
            
            if not self.vertical_verify(rindex,c,nb_elem,vals):
                return False

        return True

    def check_hclue(self):
        for r in range(self.N):
            vals = set()
            cindex = 0
            nb_elem = 0
            hzone = False
            for c in range(self.N):
                if not hzone and str(self.hgrid[r][c]).startswith("H"):
                    hzone = True
                    cindex = c
                    vals = set()
                    nb_elem = 0
                if hzone:

                    if str(self.hgrid[r][c]).startswith("B"):
                        if not self.horizontal_verify(r,cindex,nb_elem,vals):
                            return False
                        hzone = False
                        cindex = 0
                        vals = set()
                        nb_elem = 0
                        
                    elif str(self.hgrid[r][c]).startswith("H"):
                        if not self.horizontal_verify(r,cindex,nb_elem,vals):
                            return False
                        hzone = True
                        cindex = c
                        vals = set()
                        nb_elem = 0
                    else:
                        vals.add(self.hgrid[r][c])
                        nb_elem = nb_elem + 1
            
            if not self.horizontal_verify(r,cindex,nb_elem,vals):
                return False

        return True

                        
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

kakuro = Kakuro(10)
print(" -- 1")
kakuro.fill_grid()
kakuro.print_grids()

print(" -- 2")
kakuro.fill_black()
kakuro.print_grids()

print(" -- 3 " )
kakuro.check_grid()
kakuro.print_grids()

isOK = kakuro.check_grid()
print(" -- 4 " , isOK)
kakuro.print_grids()

print(" -- 5 " )
kakuro.fill_clues()
kakuro.print_grids()



exit()
maxattempts = 5
while maxattempts > 0:
    maxattempts = maxattempts-1
    vcheck = kakuro.check_vclue()
    hcheck = kakuro.check_hclue()
    if hcheck and vcheck:
        break

kakuro.write("test.clp")
kakuro.print_grids()

print("max attempts " + str(maxattempts))
if vcheck and hcheck:
    print("\nGrid OK ++++\n")
else:
    print("\nGrid KO ----\n")
