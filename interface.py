def draw_header():
    header = """\033[36m
*#############################################*
*_________                        __          *
*\_   ___ \_______ ___ __ _______/  |_  ____  *
*/    \  \/\_  __ <   |  |\____ \   __\/  _ \ *
*\     \____|  | \/\___  ||  |_> >  | (  <_> )*
* \______  /|__|   / ____||   __/|__|  \____/ *
*        \/        \/     |__|                *
*#############################################*
* Welcome to crypto.                          *
* Created by Dmytro Kushchevskyi              *
* Enter 'help' if you need some               *
*#############################################*\033[0m
"""
    print(header, end='')

def print_help():
    help_text = """\033[34mCrypto helper:

hack        -> hack some algorithm
caesar      -> encrypt/decrypt using caesar algo
xor         -> encrypt/decrypt using xor algo
exit        -> turn off crypto\033[0m
"""
    print(help_text, end='')
