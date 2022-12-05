Usage:

	git clone https://github.com/Helsingxx/CRASH-STATION.git

	cd CRASH-STATION

	source bin/activate

	python3 fuzzer.py

This script creates a new file for which you choose the name. It outputs into this file the range of function calls that you
want to use against your C code. You will have to input the prototype to the function. It will generate random inputs according
to the prototype specified.

This program can also run pre-compiled "a.out" files. You can enter the arguments to the executable and it will run it along with those
arguments.
It will fuzz the input to your program. If the program execution does not end cleanly, the script will report it.
You can pass files as arguments to the executable as well, not just strings.
The stdin the script will generate is completely random. It will not depend on your files.
If you pass files as arguments, it will parse the files, save a copy of the syntax used, then generate files with the randomized syntax which
it will pass as arguments to your file.

This is the first iteration of the program. Have fun!
