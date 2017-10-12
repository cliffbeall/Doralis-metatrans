import subprocess, os

samplefiledict = {}
with open('samples.txt', 'r') as samplefile:
    for line in samplefile:
        linelist = line.rstrip().split('\t')
        filename = 'mgm{}.050.upload.fastq.gz'.format(linelist[0])
        if linelist[1][:-3] in samplefiledict:
            samplefiledict[linelist[1][:-3]].append(filename)
        else:
            samplefiledict[linelist[1][:-3]] = [filename]

for sample in samplefiledict:
    samfile = os.path.join('dsb_align2', '{}_dsb.sam'.format(sample))
    print 'Running Bowtie2 on sample {}'.format(sample)
    command = ['bowtie2', '--very-sensitive-local', '--no-unal',
               '-p', '8', '-X', '1000', '--score-min', 'G,20,28',
               '--no-mixed', '--rg-id', sample,
               '-x', 'ref_genomes/desulfobulbus/Doralis_genbank',
               '-1', os.path.join('rawdata', samplefiledict[sample][0]),
               '-2', os.path.join('rawdata', samplefiledict[sample][1]),
               '-S', samfile]
    subprocess.call(command)
    print 'Running samtools on sample {}'.format(sample)
    bamfile = os.path.join('dsb_align2', '{}_dsb.bam'.format(sample))
    command2 = 'samtools view -bS {0} > {1}'.format(samfile, bamfile)
    subprocess.call(command2, shell = True)
    sortedbam = 'dsb_align2/{}_dsb_sorted.bam'.format(sample)
    command3 = ['samtools', 'sort', bamfile,
                sortedbam[:-4]]
    subprocess.call(command3)
    command4 = ['samtools', 'index', sortedbam]
    subprocess.call(command4)
