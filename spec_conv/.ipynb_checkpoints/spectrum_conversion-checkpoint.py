import pexpect
import pandas as pd 
import glob
import os

def info_file_to_txt(dirt, ext, output_ext, name=None): 
    spec_list = []
    for spec in os.listdir(dirt):
        if spec.endswith(ext):
            if name != None and name in spec: 
                spec_list.append(os.path.join(dirt, spec))
            else: 
                spec_list.append(os.path.join(dirt, spec))
    if len(spec_list) > 0:
        with open(os.path.join(dirt,'spec_conv_file'), 'w+') as file: 
            for spec in spec_list:
                file.write(f'{spec}\n')
    return len(spec_list)

def spec_conv_type(in_ext, output_ext):
    if output_ext == '.tge': 
        tge = True 
        output_ext = '.txt' 
    else:
        tge = False
    if in_ext == output_ext: 
        return 
    elif in_ext=='.spe' and output_ext == '.txt': 
        run_type = '1'
    elif in_ext=='.txt' and output_ext == '.spe': 
        run_type = '2'
    elif in_ext=='.Chn' and output_ext == '.spec': 
        run_type = '3'
    elif in_ext=='.Chn' and output_ext == '.txt': 
        run_type = '4'
    elif in_ext=='.Chn' and output_ext == '.spe': 
        run_type = '5'
    elif in_ext=='.spec' and output_ext == '.txt': 
        run_type = '6'
    elif in_ext=='.spec' and output_ext == '.spe': 
        run_type = '7'
    elif in_ext=='.IEC' and output_ext == '.spe': 
        run_type = '8'
    elif in_ext=='.Spe' and output_ext == '.spe': 
        run_type = '9'
    elif in_ext=='.Spe' and output_ext == '.txt': 
        run_type = 'a'
    else: 
        print(f'Input and output formats {in_ext} and {output_ext} not accepted.')
    return run_type, tge

def run_spec_conv(directory, input_ext='.Chn', output_ext='.spe', it=3, name=None):
    run_type, tge = spec_conv_type(input_ext, output_ext)
    counter = info_file_to_txt(directory, input_ext, output_ext, name=None)
    if counter == 0: 
        return None, None, counter, run_type
    child = pexpect.spawn('/home/alletro/python_packages/spec_conv/spec_conv/spec_con')
    child.setwinsize(1000,1000)
    child.send(run_type)
    if it == 1: 
        child.send('n')
        child.sendline(directory) 
    elif it ==2: 
        child.send('y')
        child.sendline(directory)
    else: 
        child.send('y')
        child.sendline(f'{directory}/spec_conv_file')
    return child.read(), tge, counter, run_type

def create_df_4(scrambled_data, parent_directory): 
    data_list = str(scrambled_data).split('Spectrum info:')[1:]
    df = pd.DataFrame(columns=['spectrum', 'date', 'start_time', 'live_time', 'real_time'])
    counter = 0
    tot_live = 0 
    tot_real = 0
    for item in data_list: 
        counter += 1
        item = item.lower()
        date = item[1:11].strip(' ')
        start_time = item.split('at')[1][:6].strip(' ')
        real_time = item.split('real time:')[1].split('s')[0].strip(' ')
        live_time = item.split('live time:')[1].split('s')[0].strip(' ')
        spectrum_name = item.split('==>')[1].split('8192')[0].strip(' ')
        if counter == 1:
            tot_start = start_time 
            tot_date = date
        tot_live += int(live_time)
        tot_real += int(real_time)
        row = [spectrum_name, date, start_time, live_time, real_time]
        df.loc[len(df)] = row
        df = df.sort_values('spectrum', ascending=True)
    row = [f'{parent_directory}/total.txt', tot_date, tot_start,tot_live , tot_real]    
    df.loc[len(df)] = row
    df.to_csv(os.path.join(parent_directory, 'spec_data'), index=False)
    return df

def create_df_5(scrambled_data, parent_directory): 
    data_list = str(scrambled_data).split('Spectrum info:')[1:]
    df = pd.DataFrame(columns=['spectrum', 'date', 'start_time', 'live_time', 'real_time'])
    counter = 0
    tot_live = 0 
    tot_real = 0
    for item in data_list: 
        counter += 1
        item = item.lower()
        date = item[1:11].strip(' ')
        start_time = item.split('at')[1][:6].strip(' ')
        real_time = item.split('real time:')[1].split('s')[0].strip(' ')
        live_time = item.split('live time:')[1].split('s')[0].strip(' ')
        spectrum_name = item.split('==>')[1].split('8192')[0].strip(' ')
        if counter == 1:
            tot_start = start_time 
            tot_date = date
        tot_live += int(live_time)
        tot_real += int(real_time)
        row = [spectrum_name, date, start_time, live_time, real_time]
        df.loc[len(df)] = row
        df = df.sort_values('spectrum', ascending=True)
    row = [f'{parent_directory}/total.spe', tot_date, tot_start,tot_live , tot_real]    
    df.loc[len(df)] = row
    df.to_csv(os.path.join(parent_directory, 'spec_data'), index=False)
    return df

def txt_to_tge(directory):
    new_extension = '.tge' 
    file_list = glob.glob(f"{directory}/*.txt")
    for file in file_list: 
        pre, ext = os.path.splitext(file)
        os.rename(file, pre + new_extension)
    return

def run_conversion(directory, input_extension, output_extension, outfile, name=None): 
    output, tge, counter, run_type = run_spec_conv(directory, input_extension, output_extension, name=None)
    try:
        os.remove(os.path.join(directory,"spec_conv_file"))
    except: 
        pass
    if counter == 0: 
        return
    elif outfile == 'y':
        if run_type == '4': 
            df = create_df_4(output, directory)  
        elif run_type == '5': 
            df = create_df_5(output, directory)
        else: 
            raise ValueError(f"The conversion type '{run_type}' for spec_conv does not currently have a meta_data extraction tool")
        if tge == True: 
            txt_to_tge(directory)
    return

def convert_spectra(parent_directory, input_extension, output_extension, deep=True, outfile='y', name=None): 
    run_conversion(parent_directory, input_extension, output_extension, outfile, name=None)
    if deep == True: 
        for root, dirs, files in os.walk(parent_directory, topdown=False):
            for sub_directory in dirs: 
                run_conversion(os.path.join(root,sub_directory), input_extension, output_extension, outfile, name=name)
    return

def delete_conv_files(directory, out_ext):
    dir_list = [x[0] for x in os.walk(directory)]
    for sub_directory in dir_list:
        for item in os.listdir(sub_directory):
            if item.endswith(out_ext):
                os.remove(f'{sub_directory}/{item}')
            #elif item == 'spec_data': 
            #    os.remove(f'{sub_directory}/{item}')
    return 

def check_file_count(directory, in_ext, out_ext):
    spe_count = 0 
    chn_count = 0
    dir_list = [x[0] for x in os.walk(directory)]
    for sub_directory in dir_list:
        for item in os.listdir(sub_directory):
            if item.endswith(in_ext):
                spe_count += 1 
            elif item.endswith(out_ext): 
                chn_count += 1
        if chn_count != spe_count: 
            raise ValueError(f"The {in_ext} and {out_ext} found do not match in the following directory: {sub_directory}")
    print('All values match in conversion')
    return 

def delete_original_files(directory, in_ext): 
    dir_list = [x[0] for x in os.walk(directory)]
    for sub_directory in dir_list:
        for item in os.listdir(sub_directory):
            if item.endswith(in_ext):
                os.remove(f'{sub_directory}/{item}')
    return 

def convert_master(directory, input_extension, output_extension, delete_original=True, rerun=False, outfile='y', name=None):
    if input_extension != output_extension: 
        #if rerun and delete_orginal: 
        #    raise ValueError("The variables 'delete original' and 'rerun' cannot both be set as true.")
        if rerun: 
            delete_conv_files(directory, output_extension)
        convert_spectra(directory, input_extension, output_extension, outfile=outfile, name=None)
        check_file_count(directory, input_extension, output_extension)
        if delete_original: 
            delete_original_files(directory, input_extension) 
    return