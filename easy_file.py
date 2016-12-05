#CLS
import os
os.system('clear')

def readf(fname):
	f = open(fname, 'r')
	print(f.read())
	f.close()

def wrf(fname, content):
	f = open(fname, 'w') 
	f.write(str(content))
	f.close()

def clrf(fname):
	f = open(fname, 'w') 
	f.write(str(""))
	f.close()

def addf(fname, content):
	f = open(fname, 'a') 
	for item in content:
  		f.write(str(item) + "\n")
	f.close()

def mk_list(fname):
	#counter to number the list items for display
	f = open(fname, 'r')
	#convert the comma delimeted string to a list
	lst1 = f.read().split('\n')
	#remove empty list items
	lst1 = filter(None, lst1)
	f.close()
	return lst1

def disp_list(fname):
	counter1 = 1
	os.system('clear')
	print("The search terms are: \n")
	for line in mk_list(fname):
		print("Term #" + str(counter1) + ": " + line)
		counter1 += 1

def show_options():
	print("\nSELECT AN OPTION\n")
	# 1: Run Twitter search using term
	# 2: Add a new saved tern for reuse
	print("[2] Add new term")
	print("[3] Remove a term")
	# 4: Set RT threshold
	print("[5] Back to search")
	print("")

def prompt(fname):
	prompt1 = raw_input(": ")
	try:
		int(prompt1)
		#Add new term to list
		if int(prompt1) == 2:
			#addf
			new_term = raw_input("Enter your new search term: ")
			try:
				addf(fname, [new_term])
				print(new_term + " added to list")
			except ValueError:
				print("Value Error")
		#Remove term from list
		elif int(prompt1) == 3:
			#remf
			del_item = raw_input("Select number for the term you want removed: ")
			#get the list
			list1 = mk_list(fname)
			#make sure user selects valid number to remove
			if 0 <= int(del_item) <= len(list1):
				#delete the entry by index
				del list1[int(del_item)-1]
				#cler the file
				clrf(fname)
				#write the new list back to file
				addf(fname, list1)
		elif int(prompt1) == 5:
			#remf
			prompt2(fname)
		else:
			print("# out of range")
	except ValueError:
		print("Not int")
	disp_list(fname)
	show_options()
	prompt(fname)

def prompt2(fname):
	prompt2 = raw_input("\nEnter a search term number from the list above: ")
	list1 = mk_list(fname)
	try:
		#If it's an appropriate number
		int(prompt2)
		#Print the term
		if 0 <= int(prompt2) <= len(list1):
			#load the search term
			return list1[int(prompt2)-1]
		else:
			print('number out of range')
	except ValueError:
		if prompt2 == "e":
			print("Edit mode")
			show_options()
			prompt(fname)

#MAIN()
# fname = "workfile.txt"
# disp_list(fname)
# show_options()
# prompt(fname)
