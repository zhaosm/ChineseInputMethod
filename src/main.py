import os
import json
import time
from src.generate_model import generate_bi_gram_model
import numpy as np


data_dir = '../data'
max_increase_each_round = 10


def main(n, inputs):
    # debug
    print("using %d-gram model" % n)
    start_time = time.time()
    numerators = []
    denominators = []
    for i in range(1, n + 1):
        while True:
            try:
                # debug
                print("loading %d-gram model" % i)
                with open(os.path.join(data_dir, 'numerators_' + str(i) + '.json'), 'r') as f:
                    _numerators = json.load(f)
                with open(os.path.join(data_dir, 'denominators_' + str(i) + '.json'), 'r') as f:
                    _denominators = json.load(f)
                numerators.append(_numerators)
                denominators.append(_denominators)
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

    print("calculating...")
    origin_n = n
    outputs = []
    inputs_count = len(inputs)
    for l, line in enumerate(inputs):
        if origin_n > len(line) + 1:
            n = len(line) + 1
            # debug
            print("input length < n - 1, use %d-gram instead" % n)
        else:
            n = origin_n
        try:
            candidates = [alphabet[spell] for spell in line]
        except Exception:
            print("the inputs contain unknown spells")
            exit(1)
        results = []  # list of strings
        scores = []
        round = 1
        new_scores = []
        for characters in candidates:
            # debug
            last_newly_added = len(new_scores)
            origin_len = len(results)
            new_results = []
            new_scores = []
            print("input %d/%d, round No. %d" % (l + 1, inputs_count, round))
            for character in characters:
                if round == 1:
                    if n > 2:
                        new_results.append(character)
                        new_scores.append(0)
                    else:
                        r = character
                        s = score(r, numerators, denominators, n, True)
                        new_results.append(r)
                        new_scores.append(s)
                    continue
                if round == 2 and n > 2:
                    for result in results[origin_len - last_newly_added:origin_len]:
                        r = result + character
                        s = score(r, numerators, denominators, n, True)
                        new_results.append(r)
                        new_scores.append(s)
                    continue
                for i, result in enumerate(results[origin_len - last_newly_added:origin_len]):
                    r = result + character
                    s = scores[i + origin_len - last_newly_added] * score(r, numerators, denominators, n, False)
                    new_results.append(r)
                    new_scores.append(s)
            if len(new_scores) > max_increase_each_round and not (round == 1 and n > 2):
                sorted_indexes = np.argsort([-s for s in new_scores]).tolist()
                new_results = [new_results[i] for i in sorted_indexes][:max_increase_each_round]
                new_scores = [new_scores[i] for i in sorted_indexes][:max_increase_each_round]
            # debug
            # print("new results: " + str(new_results))
            # print("new scores: " + str(new_scores))
            results = results + new_results
            scores = scores + new_scores
            round += 1
        last_newly_added = len(new_scores)
        scores = scores[-last_newly_added:]
        results = results[-last_newly_added:]
        if len(scores) == 0 or scores[0] == 0.0:
            print("input: %s, no results" % line)
            outputs.append('')
            continue
        else:
            outputs.append(results[0])
        sorted_indexes = np.argsort([-x for x in scores]).tolist()
        results = [results[i] for i in sorted_indexes]
        # best_index = scores.index(max(scores))
        # debug
        print("input: %s, top 10 outputs: %s" % (line, str(results)))

    # debug
    print("time cost: %.8f" % (time.time() - start_time))
    return outputs


def score(candidate, numerators, denominators, n, is_start):
    """
    :param candidate: list of characters
    :return: score based on n-gram model
    """
    length = len(candidate)
    # need small models. if didn't find such combination in this model, return 0
    if is_start:
        try:
            return float(numerators[length - 1][candidate]) / float(sum(numerators[length - 1].values()))
        except Exception:
            return 0.0
    if length < n:
        final_numerators = numerators[length - 1]
        final_denominators = denominators[length - 1]
    else:
        final_numerators = numerators[n - 1]
        final_denominators = denominators[n - 1]
    final_numerators_sum = sum(final_numerators.values())
    final_denominators_sum = sum(final_denominators.values())
    i = length - 1
    try:
        denominator = float(final_denominators[candidate[i - min([n, length]) + 1:i]]) / float(final_denominators_sum)
        numerator = float(final_numerators[candidate[i - min([n, length]) + 1:i + 1]]) / float(final_numerators_sum)
    except Exception:
        # no such combination, return 0
        return 0.0
    return numerator / denominator


if __name__ == '__main__':
    while True:
        n = int(input("please enter n(2 <= n <= 4)"))
        if n < 2 or n > 4:
            print("error input")
            continue
        test = input("please enter y for testing the test.txt, n for calculating your inputs")
        if test == "y":
            test = True
            inputs_fname = 'test.txt'
        elif test == 'n':
            test = False
            inputs_fname = 'input.txt'
        else:
            print("error input")
            continue
        print("reading " + inputs_fname)
        inputs = []
        with open(os.path.join(data_dir, inputs_fname), 'r') as f:
            lines = f.readlines()
            for line in lines:
                inputs.append(line.strip().split())
        outputs = main(n, inputs)
        # debug
        print("writing outputs to file...")
        with open(os.path.join(data_dir, 'output.txt'), 'w') as f:
            f.writelines([output + '\n' for output in outputs])
        if test:
            ground_truths = []
            with open(os.path.join(data_dir, 'ground_truths.txt'), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    ground_truths.append(line.strip())
            match_count = 0
            total_characters = 0
            for i, output in enumerate(outputs):
                ground_truth = ground_truths[i]
                for j, character in enumerate(output):
                    if character == ground_truth[j]:
                        match_count += 1
                    total_characters += 1
            print("match count / total_characters = %.8f" % (float(match_count) / float(total_characters)))


