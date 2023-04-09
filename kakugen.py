from os import getpid
from kakugrid import KakuroGrid
from kakufile import FileGrid
import argparse

if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(description="Generate kakuro puzzles")

    parser.add_argument("-v","--verbose",action='store_true',help="verbose mode - show logs")
    parser.add_argument("-s","--size",help="Grid size",nargs='?', type=int, default=10)
    parser.add_argument("-g","--grids",help="Number of Grid",nargs='?', const=1, type=int, default=1)
    parser.add_argument("-d","--directory",help="directory where puzzles are located")
    
    args = parser.parse_args()

    dir = args.directory
    
    if not dir:
        dir = "grids"
    dir = dir.replace("/","")

    size = args.size
    grids = args.grids

    gengrids = list()
    filegrid = FileGrid()
    k = 0
    for i in range(grids):
        kakuro = KakuroGrid(size,maxattempts=10,bcells=0.25)
        
        if kakuro.fill():
            print("grid created")
            filegrid.createNewFile()
            problem = kakuro.serialize_problem()
            solution = kakuro.serialize_solution()
            filegrid.write(problem)
            filegrid.writeSolution(solution)
        else:
            print("KO")