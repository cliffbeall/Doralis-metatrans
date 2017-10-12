import subprocess

samplenumbers = ["AU_01", "AU_02", "AU_05", "AU_07", "AU_08", "AU_09", "AU_10", "AU_11",
                 "AU_12", "AU_13", "AU_14", "AU_15", "AU_16", "AU_17", "AU_18", "AU_19"]
datadict = {}
genelist = []
command = 'htseq-count -f bam -r pos -s no -t gene -m intersection-nonempty -i locus_tag -q {0} {1}'
gff = 'ref_genomes/desulfobulbus/Doralis_genbank.gff'
for num in samplenumbers:
    bam = 'dsb_align2/{}_dsb_sorted.bam'.format(num)
    output = subprocess.check_output(command.format(bam, gff), shell=True)
    for line in output.strip().split('\n'):
        if line == '':
            continue
        linelist = line.split('\t')
        assert (num, linelist[0]) not in datadict
        datadict[(num, linelist[0])] = int(linelist[1])
for line2 in output.strip().split('\n'):
    if not line2 == '':
        genelist.append(line2.split('\t')[0])
with open('htseq-dsb-results.txt', 'w') as outfile:
    outfile.write('\t' + '\t'.join(samplenumbers) + '\n')
    for gene in genelist:
        outfile.write(gene)
        for num2 in samplenumbers:
            outfile.write('\t' + str(datadict[(num2, gene)]))
        outfile.write('\n')