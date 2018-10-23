import numpy as np
import random as rnd

def hill_climbing():
    s = [5, 6, 2, 3, 1, 4]
    r = [0,0,0,0,0,0]
    t = [1, 2, 3, 4, 5, 6]

    while np.all(s != t):
        
        x = rnd.choice(s)
        p = s.index(x)
        print(x)
        
        y = rnd.choice(s)
        q = s.index(y)
        print(y)
        
        r = s[:]
    
        s[p], s[q] = s[q], s[p]
            
        correct = 0
        currentcorrect = 0
        for i in range(6):
            if s[i] == t[i]:
                 correct = correct + 1
                 print ("hi", correct)
            if r[i] == t[i]:
                 currentcorrect = currentcorrect + 1
                 print ("hey", currentcorrect)
        if currentcorrect > correct:
             s = r[:]

    print(s)
    print(r)
