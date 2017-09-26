from clustering.vectorizer import W2V_wrapper, Featurize
from clustering.preproccess import Normalization, TAG_norm
from clustering.clustering import Kmeans_WR

import pickle
import matplotlib.pyplot as plt

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
    save_dict('test_cl4.pickle', taggerUse='spacy', triples=True, lemm=True, norm=True)
    v = load_dict('test_cl4.pickle')

    k_means(40, v.matrix_normalizate, v.words)

def cluster5():
    save_dict('test_cl5.pickle', taggerUse='spacy', triples=True, lemm=True, norm=True, red=True)
    v = load_dict('test_cl5.pickle')

    k_means(40, v.matrix_reduced, v.words)

if __name__ == '__main__':
    # cluster2()
    # cluster3()
    # cluster4()
    # cluster5()
    v = load_dict('test_cl5.pickle')


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
