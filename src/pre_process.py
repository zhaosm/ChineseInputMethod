import os

data_dir = '../data'


def pre_process():
    article_paths = ['2016-0' + str(i) + '.json' for i in range(1, 10)] + ['2016-10.json', '2016-11.json']
    for i, article_path in enumerate(article_paths):
        with open(os.path.join(data_dir, article_path), 'r') as f:
            content = f.readlines()
            output = '[' + content[0].strip()
            for line in content[1:]:
                output += (', ' + line.strip())
            output += ']\n'
        with open(os.path.join(data_dir, article_path), 'w') as f:
            f.write(output)
        # debug
        print("fininshed file No. %d" % (i + 1))


if __name__ == '__main__':
    pre_process()