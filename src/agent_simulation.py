import numpy as np
import matplotlib.pyplot as plt

from random import seed
from random import randint

time = 10
time_future = 5

default = 5
size = int(input("Enter the size : (Default = 5) "))

if(size != 5 and size != 25):
    print("Wrong size")
    exit()

default = 5
seed_val = int(input("Enter the seed value : (Default is 5) "))

seed(seed_val)


trans = np.zeros((size*size,size*size))
for i in range(size):
    for j in range(size):
        for k in range(size):
            for l in range(size):
                if(i==k and j==l):
                    if not(i==0 or i==(size-1) or j==0 or j==(size-1)):
                        trans[i*size+j,k*size+l] = 0.0
                    elif((i==0 or i==(size-1)) and (j==0 or j==(size-1))):
                        trans[i*size+j,k*size+l] = 0.5
                    else:
                        trans[i*size+j,k*size+l] = 0.25
                elif((abs(i-k)==1) and j==l):
                    trans[i*size+j,k*size+l] = 0.25
                elif((abs(j-l)==1) and i==k):
                    trans[i*size+j,k*size+l] = 0.25
                else:
                    trans[i*size+j,k*size+l] = 0.0

rotor = np.zeros(size*size)
bump = np.zeros(size*size)
for i in range(size*size):
    if(randint(0,1)==0):
        rotor[i] = 0.1
    else:
        rotor[i] = 0.9
    
    if(randint(0,1)==0):
        bump[i] = 0.1
    else:
        bump[i] = 0.9
        
if(size==5):
    rotor = np.asarray([0.1,0.1,0.1,0.9,0.1,0.1,0.9,0.9,0.1,0.1,.9,0.1,0.9,0.9,0.9,0.9,0.1,0.9,0.9,0.1,0.1,0.1,0.1,0.1,0.1])
    bump = np.asarray([0.1,0.9,0.9,0.9,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.9,0.9,0.1,0.9,0.9,0.1,0.1,0.1,0.9,0.9,0.9,0.1,0.1])

fig, axs = plt.subplots(1, 2, figsize=(10,20))
axs[0].imshow(rotor.reshape(size,size),origin='bottom')
axs[0].set_title('Rotor Distribution')
axs[1].imshow(bump.reshape(size,size),origin='bottom')
axs[1].set_title('Bump Distribution')
plt.savefig("rotor_bump_dist_"+ str(size) +".jpg")
plt.clf()

seq_pos = list()
seq_bump = list()
seq_rotor = list()

starting = randint(0,(size*size)-1)

seq_pos.append(starting)


for i in range(time):
    current_pos = seq_pos[i]
    trans_prob = randint(1,4)/4
    for j in range(size*size):
        x = trans[current_pos,j]
        trans_prob -= x
        if(trans_prob<=0):
            seq_pos.append(j)
            bump_prob = randint(1,10)/10
            rotor_prob = randint(1,10)/10
            if(bump_prob <= bump[current_pos]):
                seq_bump.append(1)
            else:
                seq_bump.append(0)
            if(rotor_prob <= rotor[current_pos]):
                seq_rotor.append(1)
            else:
                seq_rotor.append(0)
            break
            
print("Position Sequence : ",seq_pos)
print("Bump Sequence : ",seq_bump)
print("Rotor Sequence : ",seq_rotor)

filtering = np.zeros((time+1,size*size))
filtering[0:starting] = 1
for i in range(time):
    e1 = seq_bump[i]
    e2 = seq_rotor[i]
    pe1 = (1*(1-e1) + (-1)**(1-e1) * bump)
    pe2 = (1*(1-e2) + (-1)**(1-e2) * rotor)
    summer = np.sum(trans * filtering[i], axis = 1)
    filtering[i+1] = pe1 * pe2 * summer
    filtering[i+1]/= np.sum(filtering[i+1])

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    axs[i//4,i%4].imshow(filtering[i+1].reshape(size,size),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].axis('off')
plt.savefig("filtering_likelihood_"+ str(size) +".jpg")
plt.clf()

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    plotter = np.zeros((size*size,3))
    plotter[seq_pos[i+1]][1] += 1
    plotter[np.argmax(filtering[i+1])][0] += 1 
    axs[i//4,i%4].imshow(plotter.reshape(size,size,3),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].set_title("Green - Ground Truth \n Red - Most Likely", pad = -100)
axs[2,3].axis('off')
plt.savefig("filtering_compare_"+ str(size) +".jpg")
plt.clf()

filtering_1 = np.zeros((time+1,size*size))
filtering_1[0,starting] = 1
for i in range(time):
    e1 = seq_rotor[i]
    pe1 = (1*(1-e1) + (-1)**(1-e1) * bump)
    summer = np.sum(trans * filtering_1[i], axis = 1)
    filtering_1[i+1] = pe1 * summer
    filtering_1[i+1]/= np.sum(filtering_1[i+1])

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    axs[i//4,i%4].imshow(filtering_1[i+1].reshape(size,size),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].axis('off')
plt.savefig("filtering_single_modal_likelihood_"+ str(size) +".jpg")
plt.clf()

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    plotter = np.zeros((size*size,3))
    plotter[seq_pos[i+1]][1] += 1
    plotter[np.argmax(filtering_1[i+1])][0] += 1 
    axs[i//4,i%4].imshow(plotter.reshape(size,size,3),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].set_title("Green - Ground Truth \n Red - Most Likely", pad = -100)
axs[2,3].axis('off')
plt.savefig("filtering_single_modal_compare_"+ str(size) +".jpg")
plt.clf()

filtering_2 = np.zeros((time+1+time_future,size*size))
filtering_2[:time+1,:] = filtering
for i in range(time,time+time_future):
    filtering_2[i+1] = np.sum(trans * filtering_2[i], axis = 1)
    filtering_2[i+1]/= np.sum(filtering_2[i+1])

fig, axs = plt.subplots(2, 3, figsize=(10,10))
for i in range(5):
    axs[i//3,i%3].imshow(filtering_2[i+11].reshape(size,size),origin='bottom')
    axs[i//3,i%3].set_title('Time = ' + str(i+11))
axs[1,2].axis('off')
plt.savefig("future_timestep_likelihood_"+ str(size) +".jpg")
plt.clf()


backward = np.zeros((time+1,size*size))
smoothing = np.zeros((time+1,size*size))
backward[0,:] = 1
for i in range(time):
    e1 = seq_bump[time-i-1]
    e2 = seq_rotor[time-i-1]
    pe1 = (1*(1-e1) + (-1)**(1-e1) * bump)
    pe2 = (1*(1-e2) + (-1)**(1-e2) * rotor)
    backward[i+1] = np.sum(pe1 * pe2 * backward[i] * trans, axis = 1)
    backward[i+1]/= np.sum(backward[i+1])

for i in range(time+1):
    smoothing[i] = filtering[i] * backward[time-i]
    smoothing[i]/= np.sum(smoothing[i])

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    axs[i//4,i%4].imshow(smoothing[i+1].reshape(size,size),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].axis('off')
plt.savefig("smoothing_likelihood_"+ str(size) +".jpg")
plt.clf()

fig, axs = plt.subplots(3, 4, figsize=(10,10))
for i in range(10):
    plotter = np.zeros((size*size,3))
    plotter[seq_pos[i+1]][1] += 1
    plotter[np.argmax(smoothing[i+1])][0] += 1 
    axs[i//4,i%4].imshow(plotter.reshape(size,size,3),origin='bottom')
    axs[i//4,i%4].set_title('Time = ' + str(i+1))
axs[2,2].axis('off')
axs[2,3].set_title("Green - Ground Truth \n Red - Most Likely", pad = -100)
axs[2,3].axis('off')
plt.savefig("smoothing_compare_"+ str(size) +".jpg")
plt.clf()

T1 = np.zeros((time+1,size*size))
T2 = np.zeros((time+1,size*size))
pi = np.zeros(size*size)
pi[starting] = 1
T1[0,:] = pi
T2[0,:] = 0
for i in range(time):
    e1 = seq_bump[i]
    e2 = seq_rotor[i]
    pe1 = (1*(1-e1) + (-1)**(1-e1) * bump)
    pe2 = (1*(1-e2) + (-1)**(1-e2) * rotor)
    T1[i+1,:] = np.max((T1[i,:] * trans * pe1 * pe2),axis=1)
    T2[i+1,:] = np.argmax((T1[i,:] * trans * pe1 * pe2),axis=1)
    T1[i+1,:] /= np.sum(T1[i+1,:])

mean_path = np.zeros(11)
mean_path[time] = int(np.argmax(T1[time,:]))
for i in range(time,0,-1):
    mean_path[i-1] = T2[i,int(mean_path[i])]

mean_path = mean_path.astype(int)
print("Most likely path : ",mean_path.tolist())

print("Ground Truth path : ",seq_pos)

dist = 0
for i in range(len(mean_path)):
    a = mean_path[i]
    b = seq_pos[i]
    a_x = a//size
    a_y = a%size
    b_x = b//size
    b_y = b%size    
    dist += abs(a_x - b_x) + abs(a_y - b_y)

print("Manhattan Distance between paths : ", dist)



