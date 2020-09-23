import csv
import os

import pyrata.re as pyrata_re
import pyrata
import spacy
import nltk
from pyrata.nltk import pyrata2conll

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('conll2000')


def get_noun_phrase(data_list):
    pyrata_np_pattern = 'pos = "DT"? [pos = "JJ" | pos = "NN"]∗ [pos = "NN" | pos = "NNS" | pos = "NNP"]+'
    pyrata_np_pattern = 'pos="DT"? pos~"JJ|NN"∗ pos~"NN.?"+'

    extended_data = pyrata.re.extend(pyrata_np_pattern, annotation, data_list, iob=iob)
    found_noun_phrases = pyrata_re.finditer('chunk~"B-NP" [chunk~"I-NP"]*', extended_data)

    return found_noun_phrases


if __name__ == '__main__':
    '''sentence = "Autonomous cars shift insurance liability toward manufacturers and the yellow dog"#"It is fast easy and funny to write regular expressions with PyRATA"
    data = [{'raw': word, 'pos': pos, 'lem': nltk.WordNetLemmatizer().lemmatize(word.lower())} for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))]
    #data = [{'pos': 'PRP', 'raw': 'It'}, {'pos': 'VBZ', 'raw': 'is'}, {'pos': 'JJ', 'raw': 'fast'}, {'pos': 'JJ', 'raw': 'easy'}, {'pos': 'CC', 'raw': 'and'}, {'pos': 'JJ', 'raw': 'funny'}, {'pos': 'TO', 'raw': 'to'}, {'pos': 'VB', 'raw': 'write'}, {'pos': 'JJ', 'raw': 'regular'}, {'pos': 'NNS', 'raw': 'expressions'}, {'pos': 'IN', 'raw': 'with'},{'pos': 'NNP', 'raw': 'PyRATA'}]
    pyrata_re.findall('pos~"NN."', data)
    print_hi(pyrata_re.findall('pos~"NN."', data))

    pattern = 'pos~"(DT|PRP\$|NNP)"? pos~"NN.?"'''''

    '''data = [{'raw': 'Over', 'pos': 'IN'},
            {'raw': 'a', 'pos': 'DT'},
            {'raw': 'cup', 'pos': 'NN'},
            {'raw': 'of', 'pos': 'IN'},
            {'raw': 'coffee', 'pos': 'NN'},
            {'raw': ',', 'pos': ','},
            {'raw': 'Mr.', 'pos': 'NNP'},
            {'raw': 'Stone', 'pos': 'NNP'},
            {'raw': 'told', 'pos': 'VBD'},
            {'raw': 'his', 'pos': 'PRP$'},
            {'raw': 'story', 'pos': 'NN'}]'''

    '''result = pyrata.re.extend(pattern, annotation, data, iob=iob)
    print_hi(result)
    print_hi(pyrata_re.findall('chunk~"B-NP|I-NP"', result))'''

    text = os.path.join(os.path.dirname(__file__), 'genia_pos.txt')
    annotation = {'chunk': 'NP'}
    iob = True
    annotated_data = {}
    with open(text, 'r+') as f:
        csvreader = csv.reader(f, delimiter="\t")
        for row in csvreader:
            qid = row[0]
            delimiter = row[1]
            raw = row[2]
            if qid not in annotated_data:
                annotated_data[qid] = []
            annotated_data[qid].append({'delimiter': row[1], 'raw': row[2], 'pos': row[3], 'lem': row[4], 'chunk': row[5]})
        # print(annotated_data)

    noun_chunks = []
    for key, data_list in annotated_data.items():
        nps = get_noun_phrase(data_list)
        noun_chunks.append(nps)
        for np in nps:
            print(' '.join([g['raw'] for g in np.group(0)]))
