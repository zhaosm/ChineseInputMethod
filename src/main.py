import os
import json
import itertools
from src.generate_model import generate_bi_gram_model
import numpy as np


data_dir = '../data'
max_increase_each_round = 10


def main(n):
    # debug
    print("using %d-gram model" % n)
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
        try:
            candidates = [alphabet[spell] for spell in line]
        except Exception:
            print("the inputs contain unknown spells")
            exit(1)
        results = []  # list of strings
        scores = []
        round = 1
        new_results = []
        new_scores = []
        for characters in candidates:
            # debug
            last_newly_added = len(new_scores)
            origin_len = len(results)
            new_results = []
            new_scores = []
            print("round No. %d" % round)
            for character in characters:
                if round == 1:
                    r = character
                    s = score(r, numerators, denominators, n)
                    new_results.append(r)
                    new_scores.append(s)
                    continue
                for i, result in enumerate(results[origin_len - last_newly_added:origin_len]):
                    r = result + character
                    s = scores[i] * score(r, numerators, denominators, n)
                    new_results.append(r)
                    new_scores.append(s)
            if len(new_scores) > max_increase_each_round:
                sorted_indexes = np.argsort([-s for s in new_scores]).tolist()
                new_results = [new_results[i] for i in sorted_indexes][:max_increase_each_round]
                new_scores = [new_scores[i] for i in sorted_indexes][:max_increase_each_round]
            results = results + new_results
            scores = scores + new_scores
            round += 1
        last_newly_added = len(new_scores)
        scores = scores[-last_newly_added:]
        results = results[-last_newly_added:]
        if len(scores) == 0:
            print("input: %s, no results" % line)
            continue
        sorted_indexes = np.argsort([-x for x in scores]).tolist()
        results = [results[i] for i in sorted_indexes]
        # best_index = scores.index(max(scores))
        # debug
        print("input: %s, outputs: %s" % (line, str(results)))


def score(candidate, numerators, denominators, n):
    """
    :param candidate: list of characters
    :return: score based on n-gram model
    """
    length = len(candidate)
    # need small models. if didn't find such combination in this model, return 0
    if length < n - 1:
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
    if length == n - 1:
        try:
            return denominators[candidate] / denominators_sum
        except Exception:
            return 0.0

    # normal length
    i = length - 1
    try:
        denominator = denominators[candidate[i - n + 1:i]] / denominators_sum
        numerator = numerators[candidate[i - n + 1:i + 1]] / numerators_sum
    except Exception:
        # no such combination, return 0
        return 0.0
    return numerator / denominator


if __name__ == '__main__':
    main(3)

