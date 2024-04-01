from z3 import *

Die_A=[1,2,3,4,5,6]
Die_B=[1,2,3,4,5,6]
total_possibilities=0

def count_faces(Die_A):
    return len(Die_A)

def total_combinations(Die_A,Die_B):
    return len(Die_A)*len(Die_B)


def print_all_combinations(Die_A,Die_B):
    # Number of sides on each die
    sides = count_faces(Die_A)
   
    # Initialize a 6x6 matrix with empty tuples
    matrix=[]

    # Generate all possible combinations of two dice
    for i in Die_A:
        tmp=[]
        for j in Die_B:
            tmp.append((i,j))
        matrix.append(tmp)
   

    print("\n2) Total possible combinations of rolling 2 dice")
    # Print the matrix
    for row in matrix:
        print(row)


def print_probability_of_sum(Die_A,Die_B,total_combinations):
    # Initialize a dictionary to store the count of each sum
    sum_counts = {i: 0 for i in range(2, 13)}

    # Generate all possible combinations of two dice
    for i in Die_A:
        for j in Die_B:
            sum_counts[i+j]+=1


    probability={}
    # Calculate and print the probability of each sum occurring
    print("\n3) Probability of each sum:")
    for total, count in sum_counts.items():
        probability[total] = round(count / total_combinations,4)
        print(f"Sum {total}:"+ str(probability[total]))




def undoomed_dice(no_of_sides):
    SIDES = RealVal(no_of_sides)
    DieMax = 9
    p = {i : Int(f"p{i}") for i in range(DieMax)}
    q = {i : Int(f"q{i}") for i in range(DieMax)}


    s = Solver()

    #adding constraints to the value of face of each dice
    for i in range(DieMax):
        s.add(p[i]>=0)
        s.add(p[i]<=4)
        s.add(q[i]>=0)
        s.add(q[i]<=12)
       
    # Set probabilities value for possible sums 
    prob = {}
    for i in range(2,13):
        if i==2 or i==12:
            prob[i] = RealVal('1/36')
        elif i==3 or i==11:
            prob[i] = RealVal('1/18') 
        elif i==4 or i==10:
            prob[i] = RealVal('1/12')
        elif i==5 or i==9:
            prob[i] = RealVal('1/9')
        elif i==6 or i==8:
            prob[i] = RealVal('5/36')
        else:
            prob[i] = RealVal('1/6')


    sm = RealVal('0')

    #Adding constraints to number of possible sides in each dice
    for v in p.values():
        sm+=v
    s.add(sm==SIDES)

    sm = RealVal('0')
    for v in q.values():
        sm+=v
    s.add(sm==SIDES)

    #Adding constraint tha the probability value for sum of spots of dice
    print("4) ")
    for i in range(2,13):
        probi = 0
        for a in range(1, DieMax+1):
            for b in range(1, DieMax+1):
                if a+b==i:
                    probi += p[a-1]*q[b-1]/(SIDES**2)
        print("Prob eqn for "+str(i)+" is "+str(probi)+"\n")
        s.add(probi == prob[i])

        #Solving equation with the given contraints
    s.check()

    
    print("\nDie 1")
    for i in range(DieMax):
        rep = s.model()[p[i]].as_long()
        for _ in range(rep):
            print(i+1, end=" ")

    print("\nDie 2")
    for i in range(DieMax):
        rep = s.model()[q[i]].as_long()
        for _ in range(rep):
            print(i+1, end=" ")

if __name__ == "__main__":
    total_combo=total_combinations(Die_A,Die_B)
    print("1) Total combinations of rolling 2 six-sided dice is: ",total_combo)
    print_all_combinations(Die_A,Die_B)
    print_probability_of_sum(Die_A,Die_B,total_combinations(Die_A,Die_B))
    undoomed_dice(no_of_sides=6)
