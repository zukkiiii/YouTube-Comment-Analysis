#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import gensim
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary

class LDAparamater:
    def compute_coherence_values_numtopics(corpus, dictionary, texts, limit, start, step):
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, workers=2)
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())

        return model_list, coherence_values

    def compute_coherence_values_hyperparameters(corpus, dictionary, k, a, b):
        lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=k, alpha=a, eta=b, workers=2)

        coherence_model_lda = CoherenceModel(model=lda_model, texts=text_list, dictionary=dictionary, coherence='c_v')

        return coherence_model_lda.get_coherence()

    def compute_coherence_values_passes(corpus, dictionary, k, a, b, passes):
        lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=k, alpha=a, eta=b, passes=passes, workers=2)

        coherence_model_lda = CoherenceModel(model=lda_model, texts=text_list, dictionary=dictionary, coherence='c_v')

        return coherence_model_lda.get_coherence()

