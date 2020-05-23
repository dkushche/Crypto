# CRYPTO

Crypto isn't a real project it's just all my cryptology labs in university that I have formed in one project. It contains some logically split directories and files and here I'm going to explain for me in future and for someone who cares how it works and how to add something new inside of this program.

## 1. Commands
For now I have 2 types of commands. The first type means that the command calls the algorithm that fits the standard template of actions. By these actions I mean get the data or filename from stdio if it's a file, get the data from inside of it, call your function, get result string or byte array from function, ask a user does he want to save, get $filename or no and if the answer isn't "no" save in storage/$filename.crypt. For now the second type it's functions like exit, help. I have 2 JSON files which I formatted as "command_name": "what I need to run", so it works quite easy. If I need to add a second type function I just add command name and how to call this function in actions.json. If I need to add the first type function I need to work with 2 JSONs. In actions.json I forward command_name in run_algo(it's a function that abstract getting and putting data in files or std(out/in)) and call the function as written in algo_run.json. This abstraction helps me concentrate only on algorithms that I'm going to write. I don't like how big and hard for understanding algo_run.json and I hope that I'll change it in the future. 

## 2. Algorithms
As I mentioned before I had cryptology labs and this means that I have cryptography and cryptoanalysis functions inside of this project. algo directory contains all cryptography algorithms and hack directory contains all cryptoanalysis algorithm. It's a bit tricky question what I need to do with create_plot.py and hack_decorators.py because I use them only for cryptoanalysis algorithms. Maybe I need to rename it in something more clear and put in crypto_tools, but later).

## 3. Crypto Tools
This module's heart of the crypto. Here we have functionality that most of the functions use. File manager contains all interactions with files, get_param_json it's an exception but it haves quite similar logic to tell that it interacts with the file. General tools it something quite abstract and general and I can't split it in different modules. Matrix tools were created for Hill algorithm. Interface has some tools to work with colorful output some marker and animation. You may setup header, help message, colors, and markers in iface_storage directory.

***That's all for now folks.***
