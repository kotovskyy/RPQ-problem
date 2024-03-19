import time
import numpy as np

class Task:
    def __init__(self, id, r, p, q) -> None:
        self.id = id
        self.r = r
        self.p = p
        self.q = q
    
    def __repr__(self):
        return f"{self.id} {self.r} {self.p} {self.q}"

def readData(filepath: str):
    """
        Read data from a ".txt" file and return an indexed array.
        
        Parameters:
        - `filepath: str` - path to the data file
        
        Returns:
        - array of `Task` objects
    """
    with open(filepath) as file:
        data = file.readlines()
    
    # remove newlines and split data items
    data = [l.strip().split(" ") for l in data]
    # get number of elements from data - first line of the file
    nItems = int(data[0][0])
    data = np.asarray(data[1:], dtype=np.int64) # convert str to int
    indices = np.arange(0, nItems).reshape(nItems, 1)
    data = np.hstack((indices, data))
    items = []
    for d in data:
        items.append(Task(d[0], d[1], d[2], d[3]))
    
    return items

def getCmax(data: np.ndarray) -> int:
    """
        Calculate the total amount of time `C_max` needed to complete the tasks.
        
        Parameters:
        - `data: np.ndarray` - data array
        
        Returns:
        - `int` - total amount of time needed
    """
    t, cmax = 0, 0

    for i in range(len(data)):
        r, p, q = (data[i].r, data[i].p, data[i].q)
        s = max(t, r)
        t = s + p
        cmax = max(cmax, t + q)
    
    return cmax

def sortR(data):
    d = data.copy()
    d.sort(key=lambda x: x.r)
    return d

def Schrage(data):
    dataR = sortR(data)
    ready = []
    t = 0
    order = []
    
    while dataR or ready:
        while dataR and dataR[0].r <= t:
            ready.append(dataR.pop(0))

        if not ready:
            t = dataR[0].r
            continue

        max_q_task = max(ready, key=lambda x: x.q+x.p)
        ready.remove(max_q_task)
        order.append(max_q_task.id)


        t += max_q_task.p
    
    return order

def permutations(data):
    # perform Schrage algorithm on the data
    data = data.copy()
    schrageOrder = Schrage(data)
    data = np.asarray(data.copy())
    data = data[schrageOrder]
    
    # get initial Cmax value
    cmax = getCmax(data)

    # number of tasks in dataset
    N = len(data)
    # for every task `i` in dataset
    # swap it with task `k` and get `newCmax`
    # if `newCmax < cmax` -> keep the changes and update `cmax` value
    # else swap tasks back
    for i in range(N):
        for k in range(N):
            data[i], data[k] = data[k], data[i]
            newCmax = getCmax(data)
            if (newCmax < cmax):
                cmax = newCmax
            else:
                data[i], data[k] = data[k], data[i]
    
    return data

def testSolution():
    rootpath = "data/"
    filenames = ["data1.txt", "data2.txt",
                 "data3.txt", "data4.txt"]
    
    CmaxSUM = 0
    for i, name in enumerate(filenames):
        data = readData(rootpath+name)
        start = time.time()
        data = permutations(data)
        end = time.time()
        cmax = getCmax(data)
        CmaxSUM += cmax
        print(f"Cmax_{i+1} = {cmax}, Time_{i+1} = {end - start:.5} s")
        
    print(f"Total Cmax = {CmaxSUM}")

def testSingleFile(filename):
    data = readData(filename)
    data = permutations(data)
    order = [str(x.id+1) for x in data]
    print(" ".join(order))
    print(f"CMAX = {getCmax(data)}")
                
def main():
    start = time.time()
    testSolution()
    end = time.time()
    print(f"Total time: {end - start:.5} s")


if __name__ == "__main__":
    main()
    