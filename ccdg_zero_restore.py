import os, csv, glob

#genearate list of correct sample names using
#need auto method and user input method
# illumina_info --report library_index_summary --format tsv --woid WOID --output-file-name outfile.test
# Store sample names in dictionary or list? open files that have samples names, if they are missing the zero
# and match, add zero back on. write file

working_directory = '/Users/ltrani/Desktop/git/qc/ccdg_zero_restore/ccdg_zero_restore/'

#test file, will need to run illumina_info to get this file
infile = '/Users/ltrani/Desktop/git/qc/ccdg_zero_restore/ccdg_zero_restore/2854509/correctsamples.tsv'

#remove non woid file names from
def is_int(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True

#restore zeros to woid.qcstatus.tsv
def qc_status_fix(woid):
    cwd = os.getcwd()
    os.chdir(woid)
    qc_status_file = woid + '.qcstatus.tsv'
    qc_status_file_temp = woid + '.qcstatus.temp.tsv'
    with open(qc_status_file, 'r') as qc_status_filecsv, open(qc_status_file_temp, 'w') as qc_status_file_tempcsv:

        qc_status_file_reader = csv.DictReader(qc_status_filecsv, delimiter='\t')
        status_file_header = qc_status_file_reader.fieldnames

        qc_status_file_temp_writer = csv.DictWriter(qc_status_file_tempcsv, fieldnames=status_file_header,
                                                    delimiter='\t')
        qc_status_file_temp_writer.writeheader()

        for line in qc_status_file_reader:

            if line['Full Name'] in zero_samp_dict:
                line['Content'] = zero_samp_dict[line['Full Name']]
                line['Name'] = zero_samp_dict[line['Full Name']]
                line['Sample Name'] = zero_samp_dict[line['Full Name']]
                line['DNA'] = zero_samp_dict[line['Full Name']]
                line['Read Group Sample Name'] = zero_samp_dict[line['Full Name']]
                line['QC Sample'] = zero_samp_dict[line['Full Name']]
                line['Full Name'] = zero_samp_dict[line['Full Name']]
                qc_status_file_temp_writer.writerow(line)
            else:
                qc_status_file_temp_writer.writerow(line)

    os.chdir(cwd)
    return


zero_samp_dict = {}

#create dictionary with sample:zerosample from file
with open(infile, 'r') as infilecsv:
    infile_reader = csv.reader(infilecsv, delimiter='\t')

    #skip three header lines
    next(infile_reader)
    next(infile_reader)
    next(infile_reader)

    for line in infile_reader:
        if line:
            zero_sample = str(line[1].split('-lib')[0].strip())
            if zero_sample[0] == '0':
                non_zero_sample = zero_sample[1:]
                zero_samp_dict[non_zero_sample] = zero_sample

#set working dir, glob woid dirs
os.chdir(working_directory)
woid_dirs = glob.glob('285*')

#iterate through woid dirs, restore zeros to file
for woid in filter(is_int, woid_dirs):
    qc_status_fix(woid)





