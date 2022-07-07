import argparse
import numpy as np
from . import spectrum_conversion

def input_check_1(val):
    if int(val) == float(val):
        if int(val)<=9 and int(val)>=0: 
            return int(val)
        else: 
            print('Input value must be an integar between 0 and 9 - one of the options given above.') 
            val = input() 
            val = input_check_1(val)
    else: 
        print('Input value must be an integar between 0 and 9 - one of the options given above.') 
        val = input() 
        val = input_check_1(val)
    return int(val)

def initial_print(): 
    print('  ___________ _____________     __________ __   ___      __')
    print(' / ____|  __ \|  ____/ ____|   / ____/ __ \| \ | \ \    / /')
    print('| (___ | |__) | |__ | |       | |   | |  | |  \| |\ \  / / ')
    print(' \___ \|  ___/|  __|| |       | |   | |  | | . ` | \ \/ /  ')
    print(' ____) | |    | |___| |____   | |___| |__| | |\  |  \  /   ')
    print('|_____/|_|    |______\_____|   \_____\____/|_| \_|   \/    ')
    print('')
    print('This program converts spectra between RadWare, Ascii,')
    print('Xtrack (GASPWARE) and Ortec (binary Chn & ASCII Spe) formats,')
    print('including multiple-spectra (<999) Xtrack files, e.g. from AGATA.')
    print('and can gainmatch spectra.')
    print('(Ascii means (y) or (x y) data starting from channel zero)')
    print('Comment lines starting with # are ignored at the front of')
    print('ascii spectra. The 1 or 2 col. format is auto-detected.')
    print('')
    print('1) to convert RadWare (.spe) ==> Ascii (.txt)')
    print('2) to convert Ascii (.txt) ==> RadWare (.spe)')
    print('3) to convert Ascii (.txt) ==> Xtrack (.spec)')
    print('4) to convert Maestro_Chn (.Chn) ==> Ascii (.txt)')
    print('5) to convert Maestro_Chn (.Chn) ==> RadWare (.spe)')
    print('6) to convert Xtrack (.spec) ==> Ascii (.txt)')
    print('7) to convert Xtrack (.spec) ==> RadWare (.spe)')
    print('8) to convert GENIE (.IEC) ==> RadWare (.spe)')
    print('9) to convert Maestro_Spe (.Spe) ==> RadWare (.spe)')
    print('a) to convert Maestro_Spe (.Spe) ==> Ascii (.txt)')
    print('g) to gainmatch a RadWare spectrum')
    print('0) Quit')
    
def input_type_check(val): 
    if int(val) == float(val):
        if int(val)<10 and int(val)>0: 
            return int(val)
        else: 
            print('Input value must be an integar between 1 and 3 - one of the options given above.') 
            val = input() 
            val = input_type_check(val)
    else: 
        print('Input value must be an integar between 1 and 3 - one of the options given above.') 
        val = input() 
        val = input_type_check(val)
    return int(val)
    
def input_type(): 
    print('Choose how input spectra should be read:')
    print('') 
    print('1) A single spectrum using the path of the file. ')
    print('2) A list of spectra read from a textfile.') 
    print('3) A directory for which all files with the correct extension will be converted')
    return

def outfile_check(val): 
    if val == 'y' or val == 'n': 
        return val
    else: 
        print(f"Input value must be 'y' or 'n', not {val}") 
        val = input() 
        val = input_type_check(val)
    return val

def input_conversion(it): 
    if it == 1: 
        inp = ".spe"
        exp = ".txt"
    elif it == 2: 
        inp = ".txt"     
        exp = ".spe"
    elif it == 3: 
        inp = ".txt"
        exp = ".spec"
    elif it == 4: 
        inp = ".Chn"
        exp = ".txt"
    elif it == 5: 
        inp = ".Chn"
        exp = ".spe"
    elif it == 6: 
        inp = ".spec"
        exp = ".spe"
    elif it == 7: 
        inp = ".spec"
        exp = ".spe"
    elif it == 8: 
        inp = ".Spe"
        exp = ".spe"
    elif it == 9:
        inp = ".Spe"
        exp = ".txt"
    return inp, exp

def main():
    parser = argparse.ArgumentParser(prog ='spec_conv',
                                     description ='ENDF Nucleus and Decay data package.')
  
    args = parser.parse_args()
    initial_print() 
    val = input() 
    val = input_check_1(val)
    input_type()
    it = input() 
    it = input_type_check(it)
    inp, oup = input_conversion(val)
    if it == 1: 
        print('Type spectrum filename inc. extension (eg .spe):')
        directory = input()
        spectrum_conversion.run_spec_conv(directory, inp, exp, it)
    elif it == 2: 
        print('Type filename containing list of spectrum file names:')
        directory = input()
        spectrum_conversion.run_spec_conv(directory, inp, exp, it)
    else: 
        print('Type directory name for the conversions to take place')
        directory = input()
        print('Do you want an output file containing spectrum/a meta-data? (y/n)') 
        outfile = input()
        outfile = outfile_check(outfile)
        spectrum_conversion.convert_spectra(directory, inp, oup, delete_original=True, rerun=False, outfile=outfile)
        
        