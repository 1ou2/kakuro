from kakugrid import KakuroGrid
import os
import glob

class FileGrid():
    def __init__(self,griddir="grids") -> None:
        self.GID_SIZE =4
        # extension used for grid files
        self.gridext = ".clp"
        self.prefix= "k-"
        self.griddir = griddir
        if self.griddir and not os.path.exists(self.griddir):
            os.makedirs(self.griddir)
        self.gridpath = ""        

    def createNewFile(self):
        gid = self.createGridID()
        self.gridpath = os.path.abspath(self.griddir+"/"+self.prefix+gid+ self.gridext)
        return self.gridpath

    def getGridPath(self):
        return self.gridpath

    def getExtension(self):
        return self.gridext
        
    def getGrid(self,puzzleid):
        if puzzleid.isdigit():
            pid = str(puzzleid)
            while len(pid) < self.GID_SIZE:
                pid = "0"+pid
            
            items = os.listdir(self.griddir)
            filename = ""
            for f in items:
                if f.endswith(str(pid)+self.gridext):
                    filename = f
                    break
            if not filename:
                raise Exception("Cannot find grid ", pid)
            # remove extension and store filename
            #self.filename = filename[:-4]
            filepath = os.path.join(self.griddir+"/",filename)
        else:
            filepath = puzzleid

        self.gridpath = filepath        
        return KakuroGrid(fpath=filepath)

    # Generate a new GRID ID that is unique
    # returns a string 
    #         e.g. "0045"
    def createGridID(self):
       
        # grid ID is a 4 digit numbers e.g. 0012 
        if self.griddir and not os.path.exists(self.griddir):
            os.makedirs(self.griddir)
        items = os.listdir(self.griddir)
        items.sort(reverse=True)
        if items:
            # end contains gid + extension (either .sol or .txt)
            endlen = self.GID_SIZE+len(self.gridext)
            end = items[0][:endlen]
            lastgid = int(end[self.GID_SIZE:])
        else:
            lastgid = 0
        gid = str(lastgid +1)
        # pad with 0
        while len(gid) < self.GID_SIZE:
            gid = "0" + gid
        return gid

    def getAllGrids(self):
        path =  self.griddir+"/*"+ self.gridext
        files = sorted(glob.glob(path, recursive=False))
        return files

    def getGridID(self,gridpath):
        # get filename without extension
        extlen = len(self.gridext)
        gridname = os.path.basename(gridpath)[:-extlen]
        # check if files ends with a digit like 0045
        id = gridname[-self.GID_SIZE:]
        if not id.isdigit():
            return gridname
        else:
            return id

    def write(self,lines,filename=""):
        if filename:
            filepath = os.path.abspath(self.griddir+"/"+filename)
        else:
            filepath = self.gridpath
        with(open(filepath,"w")) as f:
            f.write(lines)

    def writeSolution(self,solution):
        assert(self.gridpath)
        extlen = len(self.gridext)
        gridname = os.path.basename(self.gridpath)[:-extlen]
        filepath = os.path.abspath(self.griddir+"/"+gridname+".sol")
        with(open(filepath,"w")) as f:
            f.write(solution)
        