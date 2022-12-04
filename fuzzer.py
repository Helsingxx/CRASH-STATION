import re
import art
import os
import random
import operator
import string
import subprocess
import shlex

def Str_Mutator(s_string):
	str_printed = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[]^_`{|}~ "
	random_outchar = str_printed[random.randrange(len(str_printed))]
	random_inchar = s_string[random.randrange(len(s_string))]
	return str(s_string).replace(random_inchar, random_outchar)


def El_Mutator(proto, functional):
	result = []
	mutations = [ operator.add, operator.and_, operator.sub, operator.mul, 
	operator.xor, operator.or_, operator.mod, operator.lshift, operator.rshift, 
	 operator.is_, operator.floordiv, operator.truediv]
	str_mutations = [str.upper, str.lower, str.capitalize, str.title, str.swapcase,
					Str_Mutator, Str_Mutator, Str_Mutator, Str_Mutator, Str_Mutator]
	mut_len = len(mutations)
	strmut_len = len (str_mutations)
	x = 0
	for i in functional:
		if proto[x] == "string":
			result.append(list(map(str_mutations[random.randrange(strmut_len)], [i])))
			z = 0
			for c in range(40):
				result[x].append(str(list(map(str_mutations[random.randrange(strmut_len)], [result[x][z]]))[0]))
				z += 1
		else:
			try:
				result.append(list(map(mutations[random.randrange(mut_len)], [i], [random.randrange(-256,256)])))
			except:
				result.append([0])
			s = 0
			for c in range(10):
				try:
					result[x].append(int(list(map(mutations[random.randrange(mut_len)], [result[x][s]], [random.randrange(-256, 256)]))[0]))
				except:
					result[x].append(-1)
				s += 1
		x += 1
	return list(map(list, list(map(set, result))))


#def gen_num(power):
#	global gen_num_i
#	gen_num_i += 1
#	if gen_num_i % 2 :
#		return random.randrange(0, 256 ** power)
#	else :
#		return random.randrange(-(256 ** power / 2), 256 ** power / 2)

def gen_args(prot, functional):
	inp = ""
	mut_arr = El_Mutator(prot, functional)
	for i in range(len(prot)):
		if (prot[i] == "string"):
			inp += "\""
			inp += str(mut_arr[i][random.randrange(len(mut_arr[i]))])
			inp += "\""
		else :
			inp += str(int(mut_arr[i][random.randrange(len(mut_arr[i]))]))
		inp += ","
	inp = inp[:-1]
	return inp

def function_gen(name, prot, f):
	functional = []
	for i in proto:
		if i == "string":
			functional.append(str(input ("Enter an example for a functional input; {}: ".format(i))))
		else:
			functional.append(int(input ("Enter an example for a functional input; {}: ".format(i))))
	for i in range(0,10000):
		f.write("{}({});\n".format(name, gen_args(prot, functional)))

def form_random_pass(proto):
	functional = input("Please enter the same number of functional example arguments (seperated by space): ").split(" ")
	inp = ""
	mut_arr = El_Mutator(proto, functional)
	for i in range(len(proto)):
		inp += str(mut_arr[i][random.randrange(len(mut_arr[i]))])
		inp += " "
	inp = inp[:-1]
	return inp


def form_command(executable, exec_args):
	proto = []
	command = str(executable) + " "
	for i in range(exec_args):
		proto.append(list(types.keys())[random.randrange(30) % len(list(types.keys()))])
	command += form_random_pass(proto)
	return shlex.split(command)

filename = []
proto = []
size = []
fname = ""
gen_num_i = 0
types = {"char":1, "int":4, "short":2, "long":8, "long long":8, "string" :8, "pointer" :8}
create_multiple_exe = 0
executable  = 0
exec_command = 0

art.tprint("CRASH-STATION")

while (1):
	if(input ("Is your file already compiled? (y/n): ") == 'y'):
		executable = input("Enter the name of your executable: ")
		exec_args = int(input("Enter the number of arguments that you will pass to the file: "))
		choice = input("Are your arguments files or shell variables? (fil/var/both): ").lower()[0]
		if (choice == "v"):
			subprocess.Popen(form_command(executable, exec_args))
			
		elif (choice == "f"):
			pass
		elif (choice == "b"):
			pass
		for i in range(exec_args):
			input ("Enter the file path of each file that will be passed: ")
		break
	else:
		break
if (executable):
	pass
while (1):
	filename.append(input("Enter the name of your files (you can use *): "))
	done = input("Done? (y/n): ")
	if (done.lower()[0] ==  'y'):
		break
while (1):	
	fname = input("Enter the name of the function (without braces): ")
	if (not bool(re.search(r'^[A-Za-z_][0-9A-Za-z_]*$', fname))):
		print("That's not the correct syntax, retard!")
	else:
		break
leng = input("Enter the number of arguments to the function: ")
for i in range(int(leng)):
	proto.append(str(input("Enter the types of the function arguments (\"string\" for a string): ")).lower().replace("unsigned",""))
for i in range(len(proto)):
	proto[i] =  proto[i].strip(' ')
for i in proto:
	if (i not in types.keys()):	
		types[str(i)] = input("Enter the intended size for \"{}\": ".format(i))

with open(filename[0], "a+") as f:
	print("""\nint main() {\n""", file=f)
	function_gen(fname, proto, f)
	print("\n}", file=f)




