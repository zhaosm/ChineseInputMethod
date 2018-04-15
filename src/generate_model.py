import json
import os
import time

data_dir = '../data'


def generate_bi_gram_model():
    start_time = time.time()
    n = 2
    article_names = ['2016-0' + str(i) for i in range(1, 10)] + ['2016-10', '2016-11']
    # article_names = ['2016-01']
    # debug
    article_count = 0
    print_interval = 500
    for article_name in article_names:
        texts = []
        with open(os.path.join(data_dir, article_name + '.json'), 'r') as f:
            articles = json.load(f)
        for article in articles:
            texts.append(''.join(article['title'].split()))
            texts.append(''.join(article['html'].split()))
        numerators = {}
        denominators = {}

        # debug
        print("article No. %d, %d texts" % (article_count + 1, len(texts)))
        iter = 0
        for text in texts:
            length = len(text)
            for i in range(0, length - n + 1):
                denominator = text[i:i + n - 1]
                try:
                    denominators[denominator] += 1
                except Exception:
                    denominators[denominator] = 1
            for i in range(0, length - n):
                numerator = text[i:i + n]
                try:
                    numerators[numerator] += 1
                except Exception:
                    numerators[numerator] = 1
            iter += 1
            # debug
            if iter % print_interval == 0:
                print("article No. %d, text No. %d" % (article_count + 1, iter))
        with open(os.path.join(data_dir, 'numerators' + article_name + '_' + str(n) + '.json'), 'w') as f:
            json.dump(numerators, f, indent=4, ensure_ascii=False)
        with open(os.path.join(data_dir, 'denominators' + article_name + '_' + str(n) + '.json'), 'w') as f:
            json.dump(denominators, f, indent=4, ensure_ascii=False)
        article_count += 1

    numerators = {}
    denominators = {}
    for article_name in article_names:
        with open(os.path.join(data_dir, 'numerators' + article_name + '_' + str(n) + '.json'), 'r') as f:
            numerators_temp = json.load(f)
        with open(os.path.join(data_dir, 'denominators' + article_name + '_' + str(n) + '.json'), 'r') as f:
            denominators_temp = json.load(f)
        numerators = combine_dicts(numerators_temp, numerators)
        denominators = combine_dicts(denominators_temp, denominators)
    with open(os.path.join(data_dir, 'numerators' + '_' + str(n) + '.json'), 'w') as f:
        json.dump(numerators, f, indent=4, ensure_ascii=False)
    with open(os.path.join(data_dir, 'denominators' + '_' + str(n) + '.json'), 'w') as f:
        json.dump(denominators, f, indent=4, ensure_ascii=False)
    end_time = time.time()
    print("time: %f" % (end_time - start_time))


def combine_dicts(dict1, dict2):
    for k, v in dict2.items():
        try:
            dict1[k] += v
        except Exception:
            dict1[k] = v
    return dict1


if __name__ == '__main__':
    generate_bi_gram_model()


