import os
import json


data_dir = '../data'


def analyze():
    alphabet = []
    with open(os.path.join(data_dir, 'alphabet.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            information = line.strip().split()
            alphabet = alphabet + information[1:]
    with open(os.path.join(data_dir, 'denominators_2.json'), 'r') as f:
        denominators = json.load(f)
    count = 0
    for character in alphabet:
        try:
            value = denominators[character]
            count += 1
        except Exception:
            continue
    print("total characters: %d, common characters: %d" % (len(alphabet), count))


if __name__ == '__main__':
    analyze()