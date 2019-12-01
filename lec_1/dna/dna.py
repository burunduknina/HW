import re

import matplotlib.pyplot as plt


def dna_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    names = re.findall(r'>.*?\n', text)
    dna = re.split(r'>.*?\n', text)[1:]
    for i in range(len(dna)):
        dna[i] = dna[i].replace('\n', '')
    return dna, names


def count_nucleotides(dna):
    num_of_nucleotides = dict.fromkeys(['A', 'C', 'G', 'T'])
    for i in num_of_nucleotides.keys():
        num_of_nucleotides[i] = dna.count(i)
    return num_of_nucleotides


def translate_from_dna_to_rna(dna):
    rna = dna.replace('T', 'U')
    return rna


def codon_table_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return {i[0]: i[1] for i in map(
            str.split, re.findall(r'\w{3} \w*?\s', content))}


def translate_rna_to_protein(rna, codon_table):
    protein = ''
    tail = len(rna)
    i = 0
    while tail > 3 and i < 338:
        codon = rna[-tail: -tail+3]
        protein = protein + codon_table[codon]
        tail -= 3
    if tail == 3:
        codon = rna[-3:]
        protein = protein + codon_table[codon]
    return protein


def values_to_file(names, data, file_path):
    with open(file_path, 'w') as file:
        for i, name in enumerate(names):
            file.write(name)
            file.write(f'{str(data[i])}\n')


def nucleotides_bar(names, statistics, file_path):
    for i, stat in enumerate(statistics):
        plt.bar(*zip(*stat.items()), label=names[i])
    plt.title('number of nucleotides')
    plt.legend(loc=(0, 0))
    plt.xlabel('nucleotides')
    plt.ylabel('number')
    plt.savefig(file_path)
    plt.close()


if __name__ == '__main__':
    dna, names = dna_from_file('dna.fasta')
    statistics, rna, proteins = [], [], []
    codon_table = codon_table_from_file('rna_codon_table.txt')
    for item in dna:
        statistics.append(count_nucleotides(item))
        rna.append(translate_from_dna_to_rna(item))
    values_to_file(names, statistics, 'num_of_nucleotids.txt')
    values_to_file(names, rna, 'rna.txt')
    for item in rna:
        proteins.append(translate_rna_to_protein(item, codon_table))
    values_to_file(names, proteins, 'proteins.txt')
    nucleotides_bar(names, statistics, 'num_of_nucleotids_bar.png')
