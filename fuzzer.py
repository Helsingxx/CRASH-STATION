import re
import random
import operator
import string
import subprocess
import shlex
import signal
import threading

def Str_Mutator(s_string):
	str_printed = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[]^_`{|}~ "
	if (is_hardcore):
		str_printed = string.printable
	#random_outchar = str_printed[random.randrange(len(str_printed))]
	#random_inchar = s_string[random.randrange(len(s_string))]
	#return str(s_string).replace(random_inchar, random_outchar)
	a_string = list(s_string)
	a_string[random.randrange(len(a_string))] =  str_printed[random.randrange(len(str_printed))]
	return "".join(a_string)



def El_Mutator(proto, functional, the_range):
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
			for c in range(the_range * 4):
				result[x].append(str(list(map(str_mutations[random.randrange(strmut_len)], [result[x][z]]))[0]))
				z += 1
		else:
			try:
				result.append(list(map(mutations[random.randrange(mut_len)], [i], [random.randrange(-256,256)])))
				result[x][0] = result [x][0] % types[proto[x]]
			except:
				result.append([0])
			s = 0
			for c in range(the_range):
				try:
					res = int(list(map(mutations[random.randrange(mut_len)], [result[x][s]], [random.randrange(-256, 256)]))[0])
					if (res >= 256 ** types[proto[x]]):
						res = res % 256 ** types[proto[x]]
					elif (res <= (256 ** types[proto[x]]) * -1):
						res = (res % 256 ** types[proto[x]]) * -1
					result[x].append(res)
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
	mut_arr = El_Mutator(prot, functional, 10)
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
	for i in range(0,int(input("How many lines do you wish to generate?: "))):
		f.write("{}({});\n".format(name, gen_args(prot, functional)))

def form_random_pass(proto):
	functional = input("Please enter the same number of functional example arguments (seperated by space): ").split(" ")
	inp = ""
	mut_arr = El_Mutator(proto, functional, 10)
	for i in range(len(proto)):
		inp += str(mut_arr[i][random.randrange(len(mut_arr[i]))])
		inp += " "
	inp = inp[:-1]
	return inp


def form_command(executable, exec_args):
	proto = []
	command = "./" + str(executable) + " "
	for i in range(exec_args):
		proto.append(list(types.keys())[random.randrange(30) % len(list(types.keys()))])
	command += form_random_pass(proto)
	return shlex.split(command)

def raw_fuzz():
	proto = []
	functional = []
	keylist = list(types.keys())
	functional = "This is a long {} string".format("long " * 10).split(" ")
	functional.remove("")
	functional_len = len(functional)
	for i in range(functional_len):
		proto.append("string")
	global is_hardcore
	is_hardcore = 1
	mut_result = El_Mutator(proto, functional, 10)
	is_hardcore = 0
	mut_true_res = []
	mut_true_true_res = ""
	for i in mut_result:
		mut_true_res.extend(i)
	for i in mut_true_res:
		mut_true_true_res += i
	return str(mut_true_true_res)

def parse_file(i):
	file = ""
	file_syntax = ""
	with open(i, "r+") as f:
		file += f.read()
	newfilename = str(i) + str(random.getrandbits(128))
	for i in file:
		if i not in file_syntax:
			file_syntax += i
	file_syntax_len = len(file_syntax)
	try:
		with open(newfilename, "w+") as f:
			for i in range(10000):
				f.write(file_syntax[random.randrange(file_syntax_len)])
	except:
		pass
	return newfilename


def run_exe(command, i):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	try:
		x = 1000
		while (x > 0):
			process.stdin.write(bytes(raw_fuzz() + "\n", 'ascii'))
			x -= 1
	except:
		pass
	stdout, stderr = process.communicate()
	global th
	th.append([stdout, stderr, int(process.returncode)])
	#print("Return code:", int(process.returncode))
#	if (int(process.returncode) == -signal.SIGSEGV):
	#	print("Your program has segfaulted!!!!!!")
	#elif (int(process.returncode) != 0):
	#	print("There is a problem with your program!!!!!")
	#else:
	#	print("Your program exited successfully!!")


filename = []
proto = []
size = []
fname = ""
gen_num_i = 0
types = {"char":1, "int":4, "short":2, "long":8, "long long":8, "string" :8, "pointer" :8}
create_multiple_exe = 0
executable  = 0
exec_command = 0
is_hardcore = 0
th = []


if(input ("Is your file already compiled? (y/n): ") == 'y'):
	executable = input("Enter the name of your executable: ")
	exec_args = int(input("Enter the number of arguments that you will pass to the file: "))
	choice = "f"
	if (exec_args > 0):
		choice = input("Are your arguments files or shell variables? (fil/var/none): ").lower()[0]
	if (choice == "v"):
		threads = []
		for i in range (100):
			thread = threading.Thread(target=run_exe, args=(form_command(executable, exec_args), i,))
			thread.start()
		for i in th:
			print ("Thread status: ")
			print ("Your program exited successfully!!!" if i[2] == 0 else "Your program has segfaulted!!!! GG" if i[2] == -signal.SIGSEGV else
					"There is some issue with your program....")
	else:
		filenames = []
		tmp_filenames = ""
		for i in range(exec_args):
			filenames.append(input ("Enter valid example file names for files that you would pass to the program:"))
		for i in filenames:
			tmp_filenames += " " + parse_file(i)
		command = shlex.split("./" + str(executable) + tmp_filenames)
		threads = []
		for i in range (100):
			thread = threading.Thread(target=run_exe, args=(command, i,))
			thread.start()
		for i in th:
			print ("Thread status: ")
			print ("Your program exited successfully!!!" if i[2] == 0 else "Your program has segfaulted!!!! GG" if i[2] == -signal.SIGSEGV else
					"There is some issue with your program....")
else:
	filename = input("Enter the name of the file where we will store the result: ")
	while (1):	
		fname = input("Enter the name of the function (without braces): ")
		if (not bool(re.search(r'^[A-Za-z_][0-9A-Za-z_]*$', fname))):
			print("That's not the correct syntax, retard!")
		else:
			break
	header = str(input("Enter the name of the header: ")).split('.')[0] + ".h"
	try:
		leng = int(input("Enter the number of arguments to the function: "))
	except:
		print("Wrong input. Exiting....")
		exit(1)
	for i in range(int(leng)):
		proto.append(str(input("Enter the types of the function arguments (\"string\" for a string): ")).lower().replace("unsigned",""))
	for i in range(len(proto)):
		proto[i] =  proto[i].strip(' ')
	for i in proto:
		if (i not in types.keys()):	
			types[str(i)] = input("Enter the intended size for \"{}\": ".format(i))
	with open(filename, "w+") as f:
		print("#include \"{}\"\n\nint main() {{\n".format(header), file=f)
		function_gen(fname, proto, f)
		print("\n}", file=f)




