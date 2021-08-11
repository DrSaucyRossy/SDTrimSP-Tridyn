#! /usr/bin/python3

import os
import glob
from sys import exit

#Needs to be run from the input directory

directory = os.getcwd()
parent = os.path.join(directory, "tri.inp")


 

with open(parent) as openfile:
	for line in openfile:
		for part in line.split():
			if "ttarget" in part:
				thick_data = line.split()
				print(thick_data)
				thickness = thick_data[2]
			elif "ttarget=" in part:
				thick_data = line.split()
				if len(thick_data) == 1:
					thickness_data = line.split("=")
					thickness = thickness_data[1]
				elif len(thick_data) == 2:
					thickness = thick_data[1]
				else:
					print("Something wrong with simulation file")
			if "nqx" in part:
				layer_data = line.split()
				layers = layer_data[2]
			elif "nqx=" in part:
				layer_data = line.split()
				if len(layer_data) == 1:
					layer_data = line.split("=")
					layers = layer_data[1]
				elif len(layer_data) == 2:
					layers = thick_data[1]
				else:
					print("Something wrong with simulation file")    
 
                                              
print(thickness)
print(layers)      
layer_thickness = float(thickness)/float(layers)*1e-8
print(f"The layer thickness is {layer_thickness} cm")

'''

E_31_data = open ('E0_31_target.dat', "r") #Opens the file to read
Read_data = E_31_data.readlines() #reads the data as an array
sim_var = Read_data[4].split() #this is where the actual data is stored
num_layer = Sim_var[1]
print(num_layer)
E_31_data.close
print("What profile do you want to look at?")
dose = input()
filename = dose + ".txt"
path = parent + "/Implant Profiles/" + filename

'''

weight_file = open("weight_retained.txt", "w+")
weight_file.write("Fluence (cm-2) Retained Dose (cm-2) \n")
for filename in sorted(glob.glob(os.path.join(directory, 'Implant Profiles','*.txt')), key = os.path.getmtime):
	fluences = filename.replace(directory+"/Implant Profiles/", "")
	fluence = fluences.replace(".txt", "")
	print(fluence)
	with open(os.path.join(directory, "Implant Profiles", filename), "r") as filehandle:
		data = filehandle.readlines()
		total = 0
		for i in (range(len(data)-1)):
			profile_data = data[i+1].split() #this is where the actual data is stored
			density = profile_data[1]
			fraction = profile_data[2]
			atom_density = float(density)*float(fraction)* (10**24)
			areal_density = atom_density*layer_thickness
			total = total + areal_density       
	weight_file.write(f"{fluence} {total} \n")
	print(total)
weight_file.close
exit()
