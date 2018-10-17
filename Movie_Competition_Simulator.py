import random as rand
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as npr
from scipy.stats import truncnorm

#initializing number of people in a population
N = 100000
gamma = .5

## definining the different movie features:
#blockbuster Film characteristics
beta_b = 185.0
alpha_b = 3.0
r_b = 60.0
ab1 = .5

#kids Film Characteristics
beta_k = 140.0
alpha_k = 2.0
r_k = 85.0
ak1 = .75

#artsy film
beta_a = 25.0
alpha_a = 4.0
r_a = 100.0
aa1 = .25

#Putting different film characteristics in array to make calculations
# for this calculation we will store bolckbuster features, then kids characteristics, and then finally artsy films
beta = np.array([beta_b,beta_k,beta_a])
alpha = np.array([alpha_b,alpha_k,alpha_a])
r = np.array([r_b,r_k,r_a])
a1 = np.array([ab1,ak1,aa1])

#calculating movie reachability
lambdas = r*beta*a1/100
print(lambdas)

# calculating Probabilities Matrix
P = np.array([np.array([(beta[i]*(2.2-alpha[i])**2)/(beta[i]*(2.2-alpha[i])**2+beta[j]*(2.2-alpha[j])**2) for i in range(3)])for j in range(3)] )
for i in range(3):
    P[i][i]=1

### Doing Simulation for people
# this function takes in the lambda parameter, and transition probabilities of both functions and simulates how many people
# will choose to go to see which movie over what period of time
def simulate_competition(N,lambda1,lambda2,gamma,p12,p21):
    lambdas = np.array([lambda1,lambda2])
    p = np.array([p12,p21])
    T = np.array([np.array(npr.exponential(1/lambdas[i],N)) for i in range(2)])
    tow = np.array(npr.exponential(1/gamma,N))
    t = T + tow
    film1aud = np.array([])
    film2aud = np.array([])
    #for each individual checking to see which film he will go to
    for i in range(N):
        if t[0][i] > T[1][i]:
            if rand.random() >= p[0]:
                film2aud = np.append(film2aud,t[0][i])
            else:
                film1aud = np.append(film1aud,t[0][i])
        elif t[1][i] > T[0][i]:
            if rand.random() >= p[1]:
                film1aud = np.append(film1aud,t[1][i])
            else:
                film2aud = np.append(film2aud,t[1][i])
        else:
            if t[1][i] >= t[0][i]:
                film1aud = np.append(film1aud,t[0][i])
            else:
                film2aud = np.append(film2aud,t[1][i])
    return (film1aud,film2aud)

# counts the number of items that are below a certain threshold in an array
def less_than(arr, num):
    return sum(arr[i]<num for i in range(len(arr)))
counter =0


for i in range(3):
    for j in range(3):
        counter = counter+1
        print("Counter: {}".format(counter))
        print("lambda1 {}".format(lambdas[i]))
        print("lambda2 {}".format(lambdas[j]))
        p21 =lambdas[j]/(lambdas[i]+lambdas[j])
        p12 = lambdas[i]/(lambdas[i]+lambdas[j])
        print("p12: {}".format(p12))
        print("p21: {}".format(p21))
        (t1,t2) = simulate_competition(N,lambdas[i],lambdas[j],gamma,p12,p21)
        t1 = np.sort(t1)
        t2 = np.sort(t2)
        counts = np.array([l for l in range(0,15)])
        wr1 = np.array([less_than(t1, l * 1) for l in range(1, 15)])
        wr2 = np.array([ less_than(t2, l * 1) for l in range(1, 15)])
        wr1 = np.append([0],wr1)
        wr2 = np.append([0], wr2)
        plt.figure(counter)
        plt.plot(counts,wr1,'-o')
        plt.plot(counts,wr2,'-o')
        str1 = ""
        if i == 0:
            str1 = "BlockBuster"
        if i == 1:
            str1 = "Kids Film"
        if i == 2:
            str1 = "Artsy Film"
        if j == 0:
            str2 = "BlockBuster"
        if j == 1:
            str2 = "Kids Film"
        if j == 2:
            str2 = "Artsy Film"
        plt.legend([str1,str2])
        plt.title(str1+" vs. "+ str2)
        plt.xlabel("Week")
        plt.ylabel("Number of Tickets Sold")
        print(str1+" vs. "+str2)
plt.show()

