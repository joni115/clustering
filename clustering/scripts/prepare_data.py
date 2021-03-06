from clustering.vectorizer import W2V_wrapper, Featurize
from clustering.preproccess import Normalization, TAG_norm, WC_token
from clustering.clustering import Kmeans_WR

import pickle
import pandas as pd

def w2v_train_data():
    data = Normalization()
    data.digit_to_NUM()
    corpus = data.tokenize()
    w2v_ = W2V_wrapper(corpus)
    w2v_.config()
    w2v_.train()
    w2v_.save()

def save_dict(filename, taggerUse, triples, lemm=False, norm=False, red=False):
    tagger = TAG_norm(taggerUse=taggerUse, lemm=lemm)
    tagg_data = tagger.tagger()
    featurize = Featurize(tagg_data, tagger=taggerUse, triples=triples)
    featurize.feat2dic()
    featurize.dict2matrix()
    if norm: featurize.normalizate()
    if red: featurize.reduce()
    featurize.class2pickle(filename)
    print(filename + ' already saved')

def save_wiki(filename, semantic=False):
    tokenize = WC_token()
    featurize = Featurize(tokenize.splited_data, tagger="wiki", count_words=tokenize.count_words, semantic=semantic)
    featurize.feat2dic(wiki_corpus=True)
    featurize.dict2matrix()
    featurize.normalizate()
    featurize.class2pickle(filename)
    print(filename + ' already saved')

def load_dict(filename):
    """
    filename -- pickle's file name
    """
    features = []
    with open(filename, 'rb') as f:
        features = pickle.load(f)
    print(filename + ' already loaded')
    return features

def k_means(k, matrix, words):
    clusters = Kmeans_WR(K=k, data=matrix, words=words).fit()

    for i, clus in enumerate(clusters):
        print(i, clusters[clus])

def cluster1():
    save_dict('test_cl1.pickle', taggerUse='spacy', triples=False)
    v = load_dict('test_cl1.pickle')

    k_means(40, v.matrix, v.words)

def cluster2():
    save_dict('test_cl2.pickle', taggerUse='spacy', triples=True)
    v = load_dict('test_cl2.pickle')

    k_means(40, v.matrix, v.words)

def cluster3():
    save_dict('test_cl3.pickle', taggerUse='spacy', triples=True, lemm=True)
    v = load_dict('test_cl3.pickle')

    k_means(40, v.matrix, v.words)

def cluster4():
    save_dict('test_cl4.60.pickle', taggerUse='spacy', triples=True, lemm=True, norm=True)
    v = load_dict('test_cl4.60.pickle')

    k_means(60, v.matrix_normalizate, v.words)

def cluster5():
    save_dict('test_cl5.pickle', taggerUse='spacy', triples=True, lemm=True, norm=True, red=True)
    v = load_dict('test_cl5.pickle')

    k_means(40, v.matrix_reduced, v.words)

def get_stadistic(dict_words, wiki=False):
    if wiki:
        words, occur = zip(*((word, dict_words[word]) for word in dict_words))
    else:
        words, occur = zip(*((word, dict_words[word]['n']) for word in dict_words))
    df = pd.DataFrame({'n':occur, 'word':words})
    print(df.sort_values(by='n', ascending=False).head(150))
    print(df.sort_values(by='n').head(150))
    print('150>=x<14000 mean: {}'.format(df[df['n'].isin(range(150,14000))]['n'].mean()))
    print('150>=x<14000: {}'.format(df[df['n'].isin(range(150,14000))]['n'].count() / df['n'].count() * 100))
    print('<150 mean: {}'.format(df['n'].mean()))
    print('<150: {}'.format(df[df['n'].isin(range(1,151))]['n'].count() / df['n'].count() * 100))
    print('150<=x<1001:{}'.format(df[df['n'].isin(range(150,1001))]['n'].count() / df['n'].count() * 100))
    print('150<=x<1001 mean: {}'.format(df[df['n'].isin(range(150,1001))]['n'].mean()))

def cluster6():
    print("##### CLUSTER UNSUPERVISED - MORE FEATURES#####")
    save_wiki('test_cl1.wiki.cl')
    v = load_dict('test_cl1.wiki.cl')
    v.reduce()

    k_means(130, v.matrix_reduced, v.words)

def cluster8():
    print("###### CLUSTER SUPERVISED - TAGS #######")
    save_wiki("test_cl1.wiki.supervised.cl")
    v = load_dict('test_cl1.wiki.cl')
    v.reduce_supervised()

    k_means(130, v.matrix_reduced, v.words)

def cluster7():
    print("###### CLUSTER SUPERVISED - SEMANTIC ########")
    save_wiki('test_cl2.wiki.sem.cl', semantic=True)
    v = load_dict('test_cl2.wiki.sem.cl')
    v.reduce_supervised()

    k_means(130, v.matrix_reduced, v.words)

if __name__ == '__main__':
    # cluster2()
    # cluster3()
    # cluster4()
    # cluster5()
    #  print("##### CLUSTER 6 #########")
      cluster6()
    #  print("###### CLUSTER 7 ########")
    #  cluster7()
    #  print("##### CLUSTER 8 #######")
    #  cluster8()
    v = load_dict('test_cl2.wiki.sem.cl')
    print(v.dict_words)

########### STADISTIC ###########
    # v = load_dict('cl1.wiki.sem.cl')
    # print(v.words, v.label)
    # print(v.dict_words)
    # print(v.matrix_normalizate)
    # v.reduce()
    # print(v.matrix_reduced)

##### GET BEST K ########
    # Kmean = Kmeans_WR(10, v.matrix_reduced, v.words)
    # list_k = Kmean.get_best_K()
    # print(list_k)
    # K, j_funct = zip(*list_k)
    # plt.plot(K, j_funct)
    # plt.title('Elbow method')
    # plt.xlabel('K')
    # plt.ylabel('J-funct')
    # plt.show()
