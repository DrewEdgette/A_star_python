col = 50
row = col

w = 0
h = 0

grid = []
openSet = []
closedSet = []
path = []

# f(n) = g(n) + h(n) : heuristic = h

def heuristic(a,b):
    d = dist(a.i,a.j,b.i,b.j)
    return d


# spot object for every point in the grid

class Spot:
    global w,h,row,col
    def __init__(self,i,j,f,g,h):
        self.i = i
        self.j = j
        self.f = f
        self.g = g
        self.h = h
        self.neighbors = []
        self.previous = 0
        self.wall = False
        
        if random(1) < 0.4:
            self.wall = True
        
        
    # colors in the spot
        
    def show(self,colr):
        fill(colr)
        if self.wall:
            fill(0)
        stroke(0)
        rect(self.i*w, self.j*h, w, h)
        
        
        
    # creates a list of neighboring spots around the current spot
        
    def addNeighbors(self,grid):
        i = self.i
        j = self.j
        
        if i < (col - 1):
            self.neighbors.append(grid[i+1][j])
        if i > 0:
            self.neighbors.append(grid[i-1][j])
        if j < (row - 1):
            self.neighbors.append(grid[i][j+1])
        if j > 0:
            self.neighbors.append(grid[i][j-1])
        if i > 0 and j > 0:
            self.neighbors.append(grid[i-1][j-1])
        if i < (col-1) and j > 0:
            self.neighbors.append(grid[i+1][j-1])
        if i > 0 and j < (row-1):
            self.neighbors.append(grid[i-1][j+1])
        if i < (col-1) and j < (row-1):
            self.neighbors.append(grid[i+1][j+1])
        
        

def setup():
    global openSet,closedSet,w,h,grid,col,row,starting,ending
    size(800,800)
    
    w = width/col
    h = height/row
    
    # creates the grid and adds neighbors for each spot
    
    grid = [[Spot(i,j,0,0,0) for j in range(col)] for i in range(row)]
    
    for i in grid:
        for j in i:
            j.addNeighbors(grid)
    
    
            
            
    # where do we start and where do we end? in this case we start at top left and end at bottom right
    
    starting = grid[0][0]
    ending = grid[col - 1][row - 1]
    
    starting.wall = False
    ending.wall = False
    
    openSet.append(starting)
    
    
    
    
    
# the main loop
    
def draw():
    global grid,openSet,closedSet,starting,ending,path,solution
    
    # if there is something in openSet, start doing A*
    
    if len(openSet) > 0:
        
        # look for the spot in openSet with the lowest f score. (based on f(n) = g(n) + h(n))
    
        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i
        current = openSet[winner]



        # if the current spot is the end, then stop
        
        if current == ending:
            print("done")
            noLoop()
            
        # if we're not at the end yet, take a look at the spot's current neighbors to see which one has the best g value
            
        neighbors = current.neighbors
        for i in neighbors:
            neighbor = i
            
            if neighbor not in closedSet and not neighbor.wall:
                tempG = current.g + 1
                
                newPath = False
                if neighbor in openSet:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                    openSet.append(neighbor)
                
                if newPath:
                    neighbor.h = heuristic(neighbor,ending)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current
        
        # once we're done with the current spot, take it out of openSet and put it into closedSet
                        
        openSet.remove(current)
        closedSet.append(current)
            
    # if there are no more spots in openSet, there is no solution, so stop
    
    else:
        print("no solution")
        noLoop()
        return
    
    

    
    background(255)
    
    # make the grid white and then make the closedSet red and the openSet green
    
    for i in grid:
        for j in i:
            j.show(color(255))
            
    for i in closedSet:
        i.show(color(255,0,0))
        
    for i in openSet:
        i.show(color(0,255,0))
        
    # previous keeps track of what node the current one came from. We need to look at the path all the way back to the start so we can display it.

    path = []
    temp = current
    path.append(temp)
    while temp.previous:
        path.append(temp.previous)
        temp = temp.previous


    # show the optimal path as a blue line    
    
    for i in path:
        i.show(color(0,0,255))
       
