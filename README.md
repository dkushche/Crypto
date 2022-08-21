# CRYPTO
Crypto is all my cryptology university labs that I have formed into one system.

# Table of contents

* [Requirements](https://github.com/dkushche/Crypto#requirements)
* [How to execute](https://github.com/dkushche/Crypto#how-to-execute)
* [Documentation](https://github.com/dkushche/Crypto#documentation)
  * [Commands flow](https://github.com/dkushche/Crypto#commands-flow)
  * [Development guide](https://github.com/dkushche/Crypto#development-guide)
    * [Crypto scripts](https://github.com/dkushche/Crypto#crypto-scripts)
    * [Crypto directories](https://github.com/dkushche/Crypto#crypto-directories)
    * [Crypto module](https://github.com/dkushche/Crypto#crypto-module)
    * [Crypto library](https://github.com/dkushche/Crypto#crypto-library)
* [Intersting ideas](https://github.com/dkushche/Crypto#intersting-ideas)
* [Afterword](https://github.com/dkushche/Crypto#afterword)
* [Contacts](https://github.com/dkushche/Crypto#contacts)

# Requirements

* OS: Linux/Windows
* Python 3 ecosystem:
  * pip
  * Python virtual environment utilities

# How to execute

If you try to run Crypto first time you need to call the install script.

```console
crypto@crypto_root:~# python3 install.py
```

After installation, you may start crypto with

```console
crypto@crypto_root:~# python3 crypto.py
```

You may find how to replace header and color palette in [Crypto directories](https://github.com/dkushche/Crypto#crypto-directories) iface_storage paragraph.

# Documentation

## Commands flow

Work with Crypto starts with the `main dialog`. Enter the algorithm name which you going to use. You may use <TAB> for autocompletion. To get more info about commands and a full list of them use `help`. if you need even more info write in the `help dialog` command name you're interested in. When you enter the command name you start a special `command dialog` specified by the `command module`. Usually, the first thing that the `command module` asks, it's the data that you want to process or `*.crypt` file where your data placed. **Warning** File extension `.crypt` is very important, it's a signal for Crypto that you pass filename. Then `command module` asks you for arguments that it needs to perform an action with your data. In case of any error you'll get a message and Crypto move you back into the `main dialog`. In the end, you'll get the result and the `command module` will ask you about saving the result in the file. **Warning** If you want to save just enter the filename, the extension will be added automatically, anyway the command module prints the resulting file path for you, so you'll get that something wrong. **Warning** All files where you store data for commands, need to be in the storage directory, but no one forbids you to make your own directory structure inside storage dir.

## Development guide

### Crypto scripts

* install.py
  * Creates environment into `crypto_env` directory and installs all packages listed in `(linux/windows)_requirements.txt` depending on your platform.

* create_module.py \[module_type\] \[module_name\]
  * Creates command module entry which includes:
    * ```python
        {module_type}/{module_name}.py
      ```
    * ```python
        tests/{module_type}/test_{module_name}.py
      ```

  Crypto has two main module types: `algo` and `hack`. `algo` stands for cryptography algorithms and `hack` for cryptanalysis algorithms. After creating the module you may call it via the `main dialog`. It's good practice to cover your module with tests, which you can run manually using `crypto_env/bin/pytest -v -m standard_set` or with Github Actions on every push.

* crypto.py
  * This script enters crypto_env and runs the Crypto core.

### Crypto directories

* algo/hack - directories that contain Crypto modules. Crypto module it's a file that contains the realization of a specific algorithm. For `algo` folder it's a cryptography algorithm, for `hack` it's a cryptoanalysis algorithm. In `__init__.py` happens forwarding entry point functions from each module. More about this you may read in [Crypto module](https://github.com/dkushche/Crypto/#crypto-module).

* crypto_commands - folder contains specific system modules(e.g help, exit).

* storage - folder contains `.crypt` files with clean, encrypted, or specific data that modules read as input or where they save their output. The storage contains the user's data, so it's added to `.gitignore`.

* iface_storage - **This folder is most important for cheaters, it contains palette and header configuration files**. You may replace the header on your own and edit markers and palettes for different log types. **Warning** Don't touch colors, you may choose between them while configuring log types color, but don't change them they just contain special shell color codes.

* crypto_native - It's the mistake that I made to faster pass the lab. It should be rewritten in clear python.

* crypto_storage - contains specific data that algorithms may use during data processing. For example, `words.json` contains words that used by Bruteforce to verify that it bumps the caesar algorithm. `freqchars.json` contains frequency characteristics for different languages. If your module needs some external data you should store it here and import in a runtime.

* crypto_tools - contains the main library of Crypto. More about this here [Crypto library](https://github.com/dkushche/Crypto/#crypto-library)

* crypto_env - Python virtual environment. If you don't know what is it, just google.

* tests - contains unit tests for your modules `processing functions`

### Crypto module

Every module has its own file with a special entry point function named the same as a command. This function is forwarding via the `__init__.py` script to the core. When you run Crypto, core imports `algo` and `hack` python modules which automatically runs `__init__.py` scripts in these modules, which import entry point functions from Crypto modules. When the user enters a command into the `main dialog` for example `caesar`, the core tries to call a function named caesar. It sounds a bit hard but a real example will help. Let's take look at the `xor.py` Crypto module. You will always get a similar structure with the use of the `create_module.py` which is best practice.
```python
# I deleted redundant calculations. Here we need to concentrate on the interface
# Crypto library contains important functions that you will need during writing your module
import crypto_tools

# ${module_name}_little_doc it's part of the module public interface. help command use it
# result while forming basic help message
def xor_little_doc():
    return "encrypt/decrypt using xor algo"

# ${module_name}_full_doc also part of public interface. help use it for showing more
# detailed info about the command
def xor_full_doc():
    return """
    Xor algorithm.
    Xor your data with repeating key
    """

# ${module_name}_processing function that contains main logic
# This function mustn't contain any user input/output, the flow of
# this function: get arguments, return the result.
def xor_processing(data, key, encrypt):

    ...

    return result_str

# Here I want to highlight two important ideas:
#
# 1. All commands have standard flow:
# -> read data(file || stream) -> process data -> write data in stream and save
# or not in a file. file_manipulation decorator takes reading and writing into
# a file on itself. You just need to get from the user additional parameters
# and process everything.
#
# 2. xor it's entry function. When you write xor in the main dialog,
# the core runs this function. It's mendatory to separate all logic in the processing function
# and keep all arguments and data prepering here. The main purpose of the entry point function
# it's being a part of Crypto, a part of the user interface.
@crypto_tools.file_manipulation()
def xor(data):
    
    ...

    return xor_processing(data, key, encrypt)

# To make other module functions public you need to add them as attributes
# into the entry function.
xor.little_doc = xor_little_doc
xor.full_doc = xor_full_doc
xor.processor = xor_processing
```

I hope you got the main idea. I tried to write self-documented code so, you may try to check how written different modules and I hope the code will answer some of your questions. Yeah, I almost forgot we didn't watch on `__init__.py` file example.

```python
from .xor import xor

def __doc__():
    return f"Cryptography module"
```

As you may see help uses the`__doc__` function while generating help message. From module file, with name xor, we import entry point function `xor`. **Warning** Please never add modules by yourself use `create_module` script. **Never** import modules from your Python module. For example, if `caesar` Crypto module for some reason needs to import `xor` Crypto module it's really bad, it means that you made something wrong or you must abstract functionality that you want to share, into function and add this function into `Crypto library` and then call it in `caesar` and `xor` Crypto modules. If you have `brute_force` Crypto module in `hack` and you need to import `caesar` or `xor` from `algo` it's okay, because these Crypto modules from different Python modules.

### Crypto library

The most important part of the project it's a Crypto library that you may find in the `crypto_tools` directory. It contains everything that I needed while I built Crypto modules. In this section, we will move through all library files.

* block_cypher_tools.py: block cyphers utils help you use feistel network in your modules.
* cert_tools.py: help generate certificates.
* file_manager.py: all file manipulation functions implemented in this file.
* general_decorators.py: all decorators that you may see in Crypto modules implemented here.
* general_tools.py: functions used by a couple of Crypto modules, contains some handy utilities.
* interface.py: If you want to interact with stdio you **must** use functions implemented here. Usage examples you may find in existed Crypto modules.
* math_tools.py, matrix_tools.py, elliptic_math_tools.py: If you need some math those files contain enough.
* ms_cryptoapi_tools.py: give you ability to use MS cryptoapi in your modules.
* plot_tools.py: if you need to create a plot to visualize some data check this out.

# Intersting ideas
1. Many crypto modules are child's play it'll be awesome to improve them.
1. Architecture still needs refinement. It needs: cleaner interface, cleaner separation of entry point and processing functions, more understandable imports and better encapsulation.
1. Anything that comes into your head.

# Afterword
At this point, I'll stop contribute actively to this project. I made all this, because I wanted to turn boring separate labs into something more, in a real learning project where I didn't just get knowledge in crypto algorithms, but improve my architect expertise and skills in so powerful and elegant language as Python. As usual, it was an awesome experience and this is why I so love programming. If you think it's an interesting project and you want to improve it I always open to new ideas on [my Linkedin](https://github.com/dkushche/Crypto/#contacts). Contact me and I'll try my best to help you or agree about your contribution. Also, I'm really interested in discovering something new, so if you have any ideas feel free to send me a message. At least for people who write their own labs, it may be a good testing system for checking does something wrong with their code or they use incorrect values. I won't get mad if you change the header and take my lab, someone was forced by parents to go into university as an IT specialist, other was confused by fancy names of specialties that the university wrote and reality disappointed their expectations, stuff happens. Feel free to take everything that you need and spend time on something better instead of torture yourself with things you don't really like.

# Contacts
* https://www.linkedin.com/in/dkushchevskyi/

***That's all for now folks.***
