import numpy as np
import pandas as pd
from tqdm import tqdm
import pdb

#pdb.set_trace()

#This is for subscript printing
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

print("\n\n\nHello!, this program will calculate and solve power flow problems using the Guass-Seidel numerical method.\nPlease use the per unit values for all the required inputs (Voltages and power).\n\n\t\t\t~~~MADE BY ADIB~~~\n \n\t\t ======START OF THE PROGRAM=====\n\n")


#Get the number of busses
while(1):
    n = input("Number of buses:\n\n> ")

    try:
        n = int(n)
        break
    except:
        print("Invalid Input!, please try again.\n\n")


#receiving the connection array
i = 0
k = i + 1
connection_array = np.zeros((n,n),dtype=np.int)
print("\n\nEnter 1 if there is a connection between given buses or 0 if there is none:\n\n")

while(i < n):
    while(k<n):
        try:
            connection_array[i][k] = int(input("Bus %d <--> Bus %d : "%(i+1,k+1)))
        except:
            print("\n\nInvalid input!, please enter 0 or 1 only\n\n")
            continue

        if((connection_array[i][k] != 1) and (connection_array[i][k] != 0)):
            connection_array[i][k] = 0
            print("\n\nInvalid input!, please enter 0 or 1 only\n\n")
            continue
        else:
            connection_array[k][i] = connection_array[i][k]
            k = k + 1
    i = i + 1
    k = i + 1





#receiving bus type
bus_type = ["slack"]

print("for each bus please specify wether it's a PQ or PV bus: \n")
i = 2
while(i <= n):
    bus_type.append(input("Bus %d:\n> " % (i)))
    print("\n")
    if((bus_type[-1] != "PQ") and (bus_type[-1] != "PV")):
        print("Invalid Bus type!, please try again\n\n")
        bus_type.pop()
        continue
    i = i + 1


#receiving bus Voltages
i = 0
bus_voltages = np.zeros(n,dtype=np.complex)
print("Enter slack and PV bus Voltages in their triangular format:\n\n")
while (i<n):
        if((bus_type[i]=="slack") or (bus_type[i]=="PV")):
            while(1):
                try:
                    bus_voltages[i] = np.complex(input("Voltage of bus %d:\n> " % (i+1)))
                    print("\n")
                    break
                except:
                    print("Invalid Input!, please try again.\n\n")
        else:
            bus_voltages[i] = complex(1,0)

        i = i + 1



#receiving bus power
i = 0
bus_power = np.zeros((n,2),dtype=np.complex)
print("Enter the real and reactive power for each bus, in case of PV bus enter the max reactive power rating:\n\n")
while (i<n):
        if((bus_type[i]=="PV") or (bus_type[i]=="PQ")):
            while(1):
                try:
                    P = float(input("Real power of bus %d:\n\n> " % (i+1)))
                    Q = float(input("Reactive power of bus %d:\n\n> " % (i+1)))
                    print("\n")
                    if(bus_type[i] == "PV"):
                        bus_power[i][0] = complex(P,0)
                        bus_power[i][1] = complex(0,Q)
                    elif(bus_type[i] == "PQ"):
                        bus_power[i][0] = -1*complex(P,0)
                        bus_power[i][1] = -1*complex(0,Q)
                    break
                except:
                    print("Invalid Input!, please try again.\n\n")
        else:
            bus_power[i][0] = complex(0,0)
            bus_power[i][1] = complex(0,0)

        i = i + 1

#receiving the line impedence and forming the Y array
i = 0
k = 0
Y_bus = np.zeros((n,n),dtype=np.complex)
print("Enter the bus to bus impedence, enter the line resistance first, then the line reactance, then the line charging susceptance:\n ")
#breakpoint()

while(i < n):
    while(k<n):
        if(k<=i):
            k = k + 1
            continue
        elif(connection_array[i][k] == 0):
            k = k + 1
            if(k<n):
                Y_bus[i][k] = np.complex("0+0j")
                Y_bus[k][i] = Y_bus[i][k]
                continue
        else:
            while(1):
                try:
                    Z = np.complex(input("Line impedence %d ---> %d:\n\n> " % (i+1,k+1)))
                    Y = np.complex(input("Shunt admittance %d ---> %d:\n\n> " % (i+1,k+1)))
                    Y_bus[i][k] = -1*np.reciprocal(Z) + Y
                    Y_bus[k][i] = Y_bus[i][k]
                    break
                except:
                    print("Invalid Input!, please try again.\n")
        k = k + 1

    Y_bus[i][i] = -1*np.sum(Y_bus[i])
    i = i + 1
    k = i + 1

"""
#constructing the Y bus array
i = 0
k = 0
Z_line = np.around(Z_line,decimals=4)
Y_bus = np.zeros((n,n),dtype=np.complex)
Y_bus = np.around(-1*np.reciprocal(Z_line),decimals=4)
Y_bus = np.nan_to_num(Y_bus)
while(i<n):
    Y_bus[i][i] = complex(0,0)
    while(k<n):
        if(i!=k):
            Y_bus[i][i] = Y_bus[i][i] + (-1*Y_bus[i][k])

        k = k + 1


    k = 0
    i = i + 1
"""
print("\n\n\n\n\n")


iterations = int(input("Enter the number of the maximum iterations:\n\n> "))
accuracy = float(input("Enter the accuracy:\n\n> "))
V_orig = np.copy(bus_voltages)
Power_old = bus_power
l = 0
for l in tqdm(range(iterations)):
    V_previous = bus_voltages
    i = 0
    while(i<n):
        if(bus_type[i] == "slack"):
            i = i + 1
            continue
        elif(bus_type[i] == "PQ"):
            k = 0
            YV = complex(0,0)
            while(k<n):
                if(k!=i):
                    YV = YV + Y_bus[i][k]*V_previous[k]
                k = k + 1

            bus_voltages[i] = ((bus_power[i][0] - bus_power[i][1])/(np.conjugate(V_previous[i])) - (YV))/(Y_bus[i][i])
        elif(bus_type[i] == "PV"):
            k = 0
            YV = complex(0,0)
            while(k<n):
                YV = YV + Y_bus[i][k]*V_previous[k]
                k = k + 1

            bus_power[i][1] = -1*np.imag(np.conjugate(V_previous[i])*YV)
           # if(bus_power[i][1]>np.imag(Power_old[i][1])):
            #    bus_power[i][1] = np.imag(Power_old[i][1])
            k = 0
            YV = complex(0,0)
            while(k<n):
                if(k!=i):
                    YV = YV + Y_bus[i][k]*V_previous[k]
                k = k + 1
            bus_voltages[i] = (((bus_power[i][0] - np.complex(0,np.real(bus_power[i][1])))/np.conjugate(V_previous[i]) - YV)/Y_bus[i][i])
            bus_voltages[i] = (bus_voltages[i] * V_orig[i])/np.abs(bus_voltages[i])
        else:
            print("Unexpected Error!")

        i = i + 1
    #l = l + 1
    #ER = np.max(np.absolute(np.max(np.int(np.real(V_previous - bus_voltages)))),np.absolute(np.max(np.int(np.imag(V_previous - bus_voltages)))))
    #if(ER > accuracy):
    #    break


#OUTPUT formating

bus_voltages = np.around(bus_voltages,decimals=4)
Y_bus = np.around(Y_bus,decimals=4)
np.set_printoptions(precision=4)

V = pd.DataFrame(bus_voltages,index=[("Bus%d"%(x+1)) for x in list(range(n))])
Y_b = pd.DataFrame(Y_bus,columns=[x+1 for x in list(range(n))],index=[("Bus%d"%(x+1)) for x in list(range(n))])
print("The voltages array:\n\n")
print(V)
print("\n\nThe Admittance array:\n\n")
print(Y_b)
print("\n\nBus currents:\n\n")
i=0
k=0
I_bus = np.dot(Y_bus,bus_voltages)
I_b = pd.DataFrame(np.around(I_bus,decimals=2),columns=['I'],index=[("Bus%d"%(x+1)) for x in list(range(n))])

print(I_b)
print("\n\nThe real and reactive power matrix:\n\n")
bus_power_2 = np.zeros(n,dtype=complex)
for i in list(range(n)):
    bus_power_2[i] = bus_voltages[i]*np.conjugate(I_bus[i])

bus_power_2 = pd.DataFrame(np.around(bus_power_2,decimals=2),index=[("S%d"%(x+1)) for x in list(range(n))],columns=['Complex Power'])
print(bus_power_2)




V.to_csv("Voltages.csv")
Y_b.to_csv("Y_bus.csv")
I_b.to_csv("I_bus.csv")
bus_power_2.to_csv("complex_power.csv")
