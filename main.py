import numpy as np

def readData(filepath: str) -> np.ndarray:
    """
        Read data from a ".txt" file and return an indexed array.
        
        Parameters:
        - `filepath: str` - path to the data file
        
        Returns:
        - `np.ndarray` - an indexed array where every element consists of:
        `[0]` - element's index
        `[1]` - R
        `[2]` - P
        `[3]` - Q
    """
    with open(filepath) as file:
        data = file.readlines()
    
    # remove newlines and split data items
    data = [l.strip().split(" ") for l in data]
    # get number of elements from data - first line of the file
    nItems = int(data[0][0])
    data = np.asarray(data[1:], dtype=np.int64) # convert str to int
    indexes = np.arange(0, nItems).reshape(nItems, 1)
    data = np.hstack((indexes, data))
    
    return data

def getCmax(data):
    # initial state
    t, cmax = 0, 0

    for i in range(len(data)):
        _, r, p, q = data[i]
        s = max(t, r)
        t = s + p
        cmax = max(cmax, t + q)
    
    print(cmax)

def main():
    filepath = "data/data4.txt"
    data = readData(filepath)
    print(data)
    getCmax(data)
 

if __name__ == "__main__":
    main()