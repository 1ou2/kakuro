import random

class Kakuro:
    def __init__(self, N):
        self.N = N
        self.blackcells = 0.3
        self.grid = [[None for _ in range(N)] for _ in range(N)]
        self.vgrid = [[None for _ in range(N)] for _ in range(N)]
        self.hgrid = [[None for _ in range(N)] for _ in range(N)]

        # set top row and left column to black cells
        for i in range(N):
            self.set_value(0,i,"B")
            self.set_value(i,0,"B")

    def set_value(self,r,c,val):
        self.grid[r][c] = val
        self.vgrid[r][c] = val
        self.hgrid[r][c] = val

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
                    self.set_value(i,j,"B")
                    
    
    def fill_vclue(self):
        for c in range(self.N):
            total = 0
            rindex = -1
            nb_elem = 0
            for r in range(self.N):
                if self.vgrid[r][c] == "B":
                    if total > 0 and nb_elem > 1:
                        self.vgrid[rindex][c] = "V" + str(total)
                    total = 0
                    rindex = r
                    nb_elem = 0
                else:
                    total = total + self.vgrid[r][c]
                    nb_elem = nb_elem +1
            if total > 0 and nb_elem > 1 and rindex < self.N -2:
                self.vgrid[rindex][c] = "V" + str(total)

    def vertical_verify(self,rindex,c,nb_elem,vals):
        if len(vals) > 0:
            # only one value, reset to a black cell
            if nb_elem == 1:
                self.set_value(rindex,c, "B")
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
                self.set_value(rindex,c, "V"+str(total))
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
                self.set_value(r,cindex, "H"+str(total))
        return True
    
    def check_vclue(self):
        for c in range(self.N):
            vals = set()
            rindex = 0
            nb_elem = 0
            vzone = False
            for r in range(self.N):
                if not vzone and str(self.vgrid[r][c]).startswith("V"):
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
                if not hzone and str(self.hgrid[r][c]).startswith("V"):
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
                        
                    elif str(self.hgrid[r][c]).startswith("V"):
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

    def fill_hclue(self):
        for r in range(self.N):
            total = 0
            cindex = -1
            nb_elem = 0
            for c in range(self.N):
                if self.hgrid[r][c] == "B":
                    if total > 0 and nb_elem > 1 :
                        self.hgrid[r][cindex] = "H" + str(total)
                    total = 0
                    cindex = c
                    nb_elem = 0
                else:
                    total = total + self.hgrid[r][c]
                    nb_elem = nb_elem +1
            if total > 0 and nb_elem > 1  and cindex < self.N -2:
                self.hgrid[r][cindex] = "V" + str(total)

    def getcluelen(self,index):
        vals = list()
        probability = 1
        # we assign a probability for each possible len
        # the shorter the len, the higher the probability
        for v in reversed(range(2, self.N-index)):
            for _ in range(probability):
                vals.append(v)
            probability = probability+1

        print(vals)
        return random.choice(vals)



    def add_vmark(self):
        k = 0
        # add vertical clues
        for i in range(1,self.N):
            if self.vgrid[k][i] == "B":
                while random.random() < 0.1 and k < self.N:
                    self.vgrid[k][i] = "B"
                    k = k+1
                # mark a vertical clue
                self.vgrid[k][i] = "V"
                sum_len = self.getcluelen(k)
                for x in range (k+1,k+1+sum_len):
                    self.vgrid[x][i] = "v"
                if x < self.N -1:
                    self.vgrid[x+1][i] = "B"
                k = 0

    def add_hmark(self):
        k = 0
        # add horizontal clues
        for i in range(1,self.N):
            if self.hgrid[i][k] == "B":
                while random.random() < 0.1 and k < self.N:
                    self.hgrid[i][k] = "B"
                    k = k+1
                # mark a vertical clue
                self.hgrid[i][k] = "H"
                sum_len = self.getcluelen(k)
                for x in range (k+1,k+1+sum_len):
                    self.hgrid[i][x] = "h"
                k = 0
        
        
    def add_clues(self):      
        # add vertical clues
        for i in range(1, self.N):
            for j in range(1, self.N-1):
                if self.grid[i][j] is not None and self.grid[i][j-1] == "B":
                    k = 2
                    while j + k < self.N and self.grid[i][j+k-1] is not None:
                        k += 1
                    if k > 2:
                        sum_clue = sum(int(self.grid[i][j+1:m]) for m in range(j+1, j+k))
                        self.grid[i][j+1:j+k] = [str(sum_clue)] * (k-1)
                        self.grid[i][j] = "V"
                        
        # add horizontal clues
        for i in range(1, self.N-1):
            for j in range(1, self.N):
                if self.grid[i][j] is not None and self.grid[i-1][j] == "B":
                    k = 2
                    while i + k < self.N and self.grid[i+k-1][j] is not None:
                        k += 1
                    if k > 2:
                        sum_clue = sum(int(self.grid[m][j]) for m in range(i+1, i+k))
                        for m in range(i+1, i+k):
                            self.grid[m][j] = str(sum_clue)
                        self.grid[i][j] = "H"
                        
    def print_one_grid(self,g):
        for r in range(self.N):
            row = ""
            for c in range(self.N):
                row = row + "{:>4}".format(g[r][c])
            print(row)     
        print("\n\n")

    def print_grids(self):
        self.print_one_grid(self.grid)
        self.print_one_grid(self.vgrid)
        self.print_one_grid(self.hgrid)

kakuro = Kakuro(14)
kakuro.fill_grid()
kakuro.fill_black()
kakuro.fill_vclue()
kakuro.check_vclue()
kakuro.fill_hclue()
kakuro.check_hclue()

#kakuro.add_vmark()
#kakuro.add_hmark()
kakuro.print_grids()
#kakuro.add_clues()
#kakuro.print_grid()
