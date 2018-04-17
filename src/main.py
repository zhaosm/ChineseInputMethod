import os
import json
import itertools
from src.generate_model import generate_bi_gram_model


data_dir = '../data'
gamma = 0.5


def main(n):
    # debug
    print("using %d-gram model, gamma=%f" % (n, gamma))
    while True:
        try:
            # debug
            print("loading model")
            with open(os.path.join(data_dir, 'numerators_' + str(n) + '.json'), 'r') as f:
                numerators = json.load(f)
            with open(os.path.join(data_dir, 'denominators_' + str(n) + '.json'), 'r') as f:
                denominators = json.load(f)
            break
        except Exception:
            # debug
            print("model not found. generating %d gram model..." % n)
            generate_bi_gram_model(n)
    # debug
    print("reading phonetic alphabet...")
    alphabet = {}
    with open(os.path.join(data_dir, 'alphabet.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            information = line.strip().split()
            alphabet[information[0]] = information[1:]

    # debug
    print("reading input")
    input = []
    with open(os.path.join(data_dir, 'input.txt'), 'r') as f:
        lines = f.readlines()
        for line in lines:
            input.append(line.strip().split())

    print("calculating...")
    for line in input:
        result = ''
        # debug
        count = 0
        max_score = 0

        candidates = [alphabet[spell] for spell in line]
        candidates = itertools.product(*candidates)
        for candidate in candidates:
            candidate = ''.join(list(candidate))
            s = score(candidate, numerators, denominators, n)
            if s > max_score:
                max_score = s
                result = candidate
            # debug
            count += 1
            print("candidate No. %d" % count)
        # debug
        print("input: %s, output: %s, score: %.16f" % (line, result, max_score))


def score(candidate, numerators, denominators, n):
    """
    :param candidate: list of characters
    :return: score based on n-gram model
    """
    length = len(candidate)
    if len(candidate) < n - 1:
        # debug
        print("need %d-gram information" % length)
        while True:
            # debug
            print("loading %d-gram model" % length)
            try:
                with open(os.path.join(data_dir, 'numerators_%d.json' % length), 'r') as f:
                    small_numerators = json.load(f)
                break
            except Exception:
                # debug
                print("haven't found %d-gram model, generating..." % length)
                generate_bi_gram_model(length)
        try:
            return small_numerators[candidate] / sum(small_numerators.values())
        except Exception:
            return 0.0
    numerators_sum = sum(numerators.values())
    denominators_sum = sum(denominators.values())
    try:
        score = denominators[candidate[0:n - 1]] / denominators_sum
    except Exception:
        return 0.0
    for i in range(n - 1, length):
        try:
            denominator = denominators[candidate[i - n + 1:i]] / denominators_sum
            numerator = numerators[candidate[i - n + 1:i + 1]] / numerators_sum
        except Exception:
            return 0.0
        score = score * numerator / denominator
    return score


if __name__ == '__main__':
    main(2)

