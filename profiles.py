#! /usr/bin/python3

''' Created by Ross Anthony reads data from output.dat and E0_31_target.dat and create different profiles for each fluence step'''
 
import os
import time
from sys import exit
 
parent= os.getcwd() #Gets the current working directory
#print (parent)
path = "/Implant Profiles"
 
if os.path.exists( parent + path) is False: # Checks if the implnt profile directory exists
    os.mkdir(parent +path) # if it doesn't exist create the folder
else:
    print("Directory already exists") # if it does exists print the statement

try:
	filehandle = open ('time_run.dat',"r") #Opens the time_run files to read it
	linelist = filehandle.readlines() #Reads the lines from the file as a variable
	#print(linelist)
	if " end outp" in linelist[-1]: #Checks the last line of the file to see that the simulation existed
		text = linelist[-6].partition("E:") #reads the 6th line from the bottom and partitions it into three different elements everything before the character, the characters and everything after the characters
		data = text[0].partition("flc:") #partions element 0 from the above array based on flc
		final_flc = data[2].strip() # removes spaces from element 2 from above array
		flc_stps = data[0]
		print(f"The final fluency is {final_flc}")
		print(f"The number of steps were {flc_stps}")
		E_31_data = open ('E0_31_target.dat', "r") #Opens the file to read
		Read_data = E_31_data.readlines() #reads the data as an array
		#Sim_header = Read_data[3] #reads the third lines this is where the headers for histories, layer number, etc,
		Sim_var = Read_data[4].split() #this is where the actual data is stored
		print(Sim_var)
		num_his = Sim_var[0]
		num_layer = Sim_var[1]
		num_elem = Sim_var[2]
		idout = Sim_var[3]
		if idout == -1: #Checks what the fluence step is
			steps = int(num_his)/100
		else:
			steps = float(num_his)/float(idout)
		print(steps)
		for i in range(int(steps)): #creates the implant pro
			fluence = str(round((float(final_flc)/steps)*(i+1),2))
			file_name =parent + path + "/" +  fluence + ".txt"
			fp = open (file_name, "w+")
			fp.write("center[A]  density[a/A^3]  atomic fraction \n")
			begin_data = 40 + ((int(num_layer)+16)*(i+1))
			end_data = begin_data + int(num_layer)
			layer_data = Read_data[begin_data:end_data]
			fp.writelines(layer_data)
			fp.close()
			time.sleep(0.1)
			E_31_data.close
	else:
		print(linelist[-1])
		print("Simulation incomplete run again")
except IOError:
	print("File Does Not Exist Run SDTrimSP")
finally:
	filehandle.close

exit()
