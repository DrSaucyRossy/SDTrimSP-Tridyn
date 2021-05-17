#! /usr/bin/python3
import os
from sys import exit

parent= os.getcwd()

#print (parent)



path = "/Implant Profiles"

if os.path.exists( parent + path) is False:
    os.mkdir(parent +path)
else:
    print("Directory already exists")

try:
    filehandle = open ('time_run.dat',"r")
    linelist = filehandle.readlines()
    #print(linelist)
    if " end outp" in linelist[-1]:
        text = linelist[-6].partition("E:")
        data = text[0].partition("flc:")
        final_flc = data[2].strip()
        flc_stps = data[0]
        print(f"The final fluency is {final_flc}")
        print(f"The number of steps were {flc_stps}")
        E_31_data = open ('E0_31_target.dat', "r")
        Read_data = E_31_data.readlines()
        Sim_header = Read_data[3]
        Sim_var = Read_data[4].split()
        #print(Sim_var)
        num_his = Sim_var[0]
        num_layer = Sim_var[1]
        num_elem = Sim_var[2]
        idout = Sim_var[3]
        if idout == -1:
            steps = int(num_his)/100
        else:
            steps = float(num_his)/float(idout)
            print(steps)
        for i in range(int(steps)):
            fluence = str(round((float(final_flc)/steps)*(i+1),2))
            file_name =parent + path + "/" +  fluence + ".txt"
            fp = open (file_name, "w+")
            fp.write("center[A]  density[a/A^3]  atomic fraction")
            fp.close()
            if i == 0:
            	fp = open (file_name, "a")
            	end_data = 39 + int(num_layer)
            	layer_data = Read_data[40:end_data]
            	print(type(layer_data))
            	fp.write("\n")
            	fp.writelines(layer_data)
            	fp.close()
            else:
            	fp = open (file_name, "a")
            	begin_data = 40 + (166*i)
            	end_data = begin_data +150
            	layer_data = Read_data[begin_data:end_data]
            	fp.write("\n")
            	fp.writelines(layer_data)
            	fp.close()
    else: 
        print(linelist[-1])
        print("Simulation incomplete run again")
except IOError:
        print("File Does Not Exist Run SDTrimSP")
finally:
    filehandle.close

exit()
