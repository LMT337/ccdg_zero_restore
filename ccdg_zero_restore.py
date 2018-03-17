import os, csv, glob, subprocess

#test dir
# working_directory = '/Users/ltrani/Desktop/git/qc/ccdg_zero_restore/ccdg_zero_restore/'
working_directory = '/gscmnt/gc2783/qc/CCDGWGS2018/dev/'


#test file, will need to run illumina_info to get this file
# infile = '/Users/ltrani/Desktop/git/qc/ccdg_zero_restore/ccdg_zero_restore/correctsamples.tsv'

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

    qc_status_file = woid + '.qcstatus.tsv'
    qc_status_file_temp = woid + '.qcstatus.temp.tsv'
    with open(qc_status_file, 'r') as qc_status_filecsv, open(qc_status_file_temp, 'w') as qc_status_file_tempcsv:
        qc_status_file_reader = csv.DictReader(qc_status_filecsv, delimiter='\t')
        status_file_header = qc_status_file_reader.fieldnames
        qc_status_file_temp_writer = csv.DictWriter(qc_status_file_tempcsv, fieldnames=status_file_header, delimiter='\t')
        qc_status_file_temp_writer.writeheader()
        if os.path.exists(qc_status_file):
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
        os.rename(qc_status_file_temp, qc_status_file)
        return

#restore sample name in all qc files
def qc_all_file_fix(woid, qc_dir):

    #fix sample name in all.tsv
    qc_dir_split = str(qc_dir.split('qc.')[1])
    qc_all_file = woid + '.' + qc_dir_split + '.build38.all.tsv'
    qc_all_file_temp = woid + '.' + qc_dir_split + '.build38.all.temp.tsv'
    if os.path.exists(qc_all_file):
        with open(qc_all_file, 'r') as qc_all_filecsv, open(qc_all_file_temp, 'w') as qc_all_file_tempcsv:
            qc_all_file_reader = csv.DictReader(qc_all_filecsv, delimiter='\t')
            qc_file_header = qc_all_file_reader.fieldnames
            qc_all_file_temp_writer = csv.DictWriter(qc_all_file_tempcsv, fieldnames=qc_file_header, delimiter='\t')
            qc_all_file_temp_writer.writeheader()
            for line in qc_all_file_reader:
                if line['DNA'] in zero_samp_dict:
                    line['SAMPLE_ALIAS'] = zero_samp_dict[line['DNA']]
                    line['DNA'] = zero_samp_dict[line['DNA']]
                    qc_all_file_temp_writer.writerow(line)
                else:
                    qc_all_file_temp_writer.writerow(line)
    os.rename(qc_all_file_temp, qc_all_file)

    #fix sample name in qcpass.tsv
    qc_pass_file = woid + '.' + qc_dir_split + '.build38.qcpass.tsv'
    qc_pass_file_temp = woid + '.' + qc_dir_split + '.build38.qcpass.temp.tsv'
    if os.path.exists(qc_pass_file):
        with open(qc_pass_file, 'r') as qc_pass_filecsv, open(qc_pass_file_temp, 'w') as qc_pass_file_tempcsv:
            qc_pass_file_reader = csv.DictReader(qc_pass_filecsv, delimiter='\t')
            sample_pass_header = qc_pass_file_reader.fieldnames
            qc_pass_file_temp_writer = csv.DictWriter(qc_pass_file_tempcsv, fieldnames=sample_pass_header, delimiter='\t')
            qc_pass_file_temp_writer.writeheader()
            for line in qc_pass_file_reader:
                if line['DNA'] in zero_samp_dict:
                    line['SAMPLE_ALIAS'] = zero_samp_dict[line['DNA']]
                    line['DNA'] = zero_samp_dict[line['DNA']]
                    qc_pass_file_temp_writer.writerow(line)
                else:
                    qc_pass_file_temp_writer.writerow(line)
    os.rename(qc_pass_file_temp, qc_pass_file)

    #fix sample name in samplemap file
    qc_samplemap = woid + '.' + qc_dir_split + '.qcpass.samplemap.tsv'
    qc_samplemap_temp = woid + '.' + qc_dir_split + '.qcpass.samplemap.temp.tsv'
    if os.path.exists(qc_samplemap):
        with open(qc_samplemap, 'r') as qc_samplemapcsv, open(qc_samplemap_temp, 'w') as qc_samplemap_tempcsv:
            qc_samplemap_reader = csv.reader(qc_samplemapcsv, delimiter='\t')
            qc_samplemap_temp_writer = csv.writer(qc_samplemap_tempcsv, delimiter='\t')
            for line in qc_samplemap_reader:
                if line[0] in zero_samp_dict:
                    line[0] = zero_samp_dict[line[0]]
                    qc_samplemap_temp_writer.writerow(line)
                else:
                    qc_samplemap_temp_writer.writerow(line)
    os.rename(qc_samplemap_temp, qc_samplemap)

    #fix sample name in fail file
    qc_fail_file = woid + '.' + qc_dir_split + '.build38.fail.tsv'
    qc_fail_file_temp = woid + '.' + qc_dir_split + '.build38.fail.temp.tsv'
    if os.path.exists(qc_fail_file):
        with open(qc_fail_file, 'r') as qc_fail_filecsv, open(qc_fail_file_temp, 'w') as qc_fail_file_tempcsv:
            qc_fail_file_reader = csv.DictReader(qc_fail_filecsv, delimiter='\t')
            fail_file_header = qc_fail_file_reader.fieldnames
            qc_fail_file_temp_writer = csv.DictWriter(qc_fail_file_tempcsv, fieldnames=fail_file_header, delimiter='\t')
            qc_fail_file_temp_writer.writeheader()
            for line in qc_fail_file_reader:
                if line['DNA'] in zero_samp_dict:
                    line['SAMPLE_ALIAS'] = zero_samp_dict[line['DNA']]
                    line['DNA'] = zero_samp_dict[line['DNA']]
                    qc_fail_file_temp_writer.writerow(line)
                else:
                    qc_fail_file_temp_writer.writerow(line)
    os.rename(qc_fail_file_temp, qc_fail_file)

    return

#genearate list of correct sample names using
#need auto method and user input method
# illumina_info --report library_index_summary --format tsv --woid WOID --output-file-name outfile.test
#create dictionary with sample:zerosample from file
zero_samp_dict = {}
def qc_info_create(woid):

    info_outfile = 'illumina_info.' + woid + '.tsv'

    if not os.path.exists(info_outfile):
        subprocess.run(["illumina_info", "--report", 'library_index_summary', "--format", 'tsv', "--woid", woid,
                        "--output-file-name", info_outfile])

    with open(info_outfile, 'r') as info_outfilecsv:
        info_file_reader = csv.reader(info_outfilecsv, delimiter='\t')

        #skip three header lines
        next(info_file_reader)
        next(info_file_reader)
        next(info_file_reader)

        for line in info_file_reader:
            if line:
                zero_sample = str(line[1].split('-lib')[0].strip())
                if zero_sample[0] == '0':
                    non_zero_sample = zero_sample[1:]
                    zero_samp_dict[non_zero_sample] = zero_sample

    return

#set working dir, glob woid dirs
os.chdir(working_directory)
woid_dirs = glob.glob('285*')

#iterate through woid dirs, restore zeros to file
for woid in filter(is_int, woid_dirs):

    os.chdir(working_directory + woid)

    #create info file if it does not exist
    qc_info_create(woid)
    #restore status file samples
    qc_status_fix(woid)

    #find all qc_dirs
    qc_dirs = glob.glob('qc.*.*')

    #restore qc file samples
    for qc_dir in qc_dirs:
        os.chdir(qc_dir)
        qc_all_file_fix(woid, qc_dir)

    os.chdir(working_directory)





