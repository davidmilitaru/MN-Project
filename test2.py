import numpy as np 
import matplotlib.pyplot as plt
import csv

A = []
nr_senators = 101
nr_bills = 460
party_index = []

check = 0
with open('senate_116_raw.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        list = []
        if check != 0:
            party_index.append(row[1])
            for i in range(4, nr_bills + 4):
                var = int(row[i])
                list.append(var)
            A.append(list)
        else:
            check = 1

(U, S, V) = np.linalg.svd(A)
print(len(A[0]))
print("\n")

#calcularea procentului de informatie stocat in primii 5 vectori singulari stanga (vectori proprii ai matricei de covarianta)
sv_sum = 0
for i in range(nr_senators):
    sv_sum += S[i]*S[i]
print("Percentage of variance in the first 5 eigenvectors:")
perc_1 = (S[0]*S[0])/sv_sum
perc_2 = (S[1]*S[1])/sv_sum
perc_3 = (S[2]*S[2])/sv_sum
perc_4 = (S[3]*S[3])/sv_sum
perc_5 = (S[4]*S[4])/sv_sum
print(perc_1*100)
print(perc_2*100)
print(perc_3*100)
print(perc_4*100)
print(perc_5*100)

#plotarea modului in care voteaza senatorii

for i in range(nr_senators):
    if party_index[i] == 'R':
        rep = plt.scatter(U[i][0], U[i][1], c = 'red')
    elif party_index[i] == 'D':
        dem = plt.scatter(U[i][0], U[i][1], c = 'blue')
    else:
        ind = plt.scatter(U[i][0], U[i][1], c = 'green')
plt.xlabel("Partisan Coordinate")
plt.ylabel("Bipartisan Coordinate")
plt.legend((rep, dem, ind), ("Republicani", "Democrati", "Independenti"), loc='upper right')
plt.show()

#aproximarea de rang 2 a matricii voturilor
A_2 = U[:,:2] @ np.diag(S[:2]) @ V[:2,:]

#procentajul de predictie a voturilor fiecarui senator utilizand aproximarea de rang 2
for i in range(nr_senators):
    counter = 0
    for j in range(nr_bills):
        if np.sign(A[i][j]) == np.sign(A_2[i][j]):
            counter += 1
    perc = counter / nr_bills * 100
    if party_index[i] == 'R':
        rep = plt.scatter(U[i][0], perc, c = 'red')
    elif party_index[i] == 'D':
        dem = plt.scatter(U[i][0], perc, c = 'blue')
    else:
        ind = plt.scatter(U[i][0], perc, c = 'green')
plt.xlabel("Partisan Coordinate")
plt.ylabel("Percentage")
plt.legend((rep, dem, ind), ("Republicani", "Democrati", "Independenti"), loc='lower left')
plt.show()

#calcularea numarului de rezultate corect reconstituite cu aproximarea de rang 2
counter = 0
vote_result = []
for j in range(nr_bills):
    sum_approx = 0
    sum = 0
    for i in range(nr_senators):
        sum = sum + A[i][j]
        sum_approx = sum_approx + A_2[i][j]
    vote_result.append(np.sign(sum))
    if np.sign(sum) == np.sign(sum_approx):
        counter += 1
print(f"\n{counter} out of 460 vote results correctly reconstructed")
print(vote_result)
    
#plotarea voturilor si distingerea caracteristicilor fiecarui vot
for i in range(nr_bills):
    x = (2.5*V[0][i] - V[1][i])/2.9
    y = -0.4*x
    var1 = x - V[0][i]
    var2 = y - V[1][i]
    newx = V[0][i] + 2*var1
    newy = V[1][i] + 2*var2

    if(vote_result[i] == 1):
        yea = plt.scatter(newx, newy, c = 'green')
    else:
        nay = plt.scatter(newx, newy, c = 'red')   
plt.xlabel("Partisan Coordinate")
plt.ylabel("Bipartisan Coordinate")
plt.legend((yea, nay), ("Legi aprobate", "Legi neaprobate"))
plt.show()
