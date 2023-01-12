# Importing spacy and running 2 examples to look into similarities among different words. 
# NOTE: observation about word similarities is printed to the terminal, so can see percentages mentioned in the comment. 

import spacy
nlp = spacy.load('en_core_web_md')

word1 = nlp("cat")
word2 = nlp("monkey")
word3 = nlp("banana")

print ("--------------Example with 'cat' monkey' 'banana'--------------------'")
print(word1, word2, word1.similarity(word2))
print(word2, word3, word3.similarity(word2))
print(word1, word3, word3.similarity(word1))
print("---------------------------------------------------------------------")
print("OBSERVATIONAL NOTE: I get why monkey and banana has similarity, but I found it interesting that cat and banana has 22% similarity. It seems counterintuitive.")

word1 = nlp("cigarette")
word2 = nlp("fag") #jargon for cigarette
word3 = nlp("tulip")

print ("--------------My example--------------------'")
print(word1, word2, word1.similarity(word2))
print(word2, word3, word3.similarity(word2))
print(word1, word3, word3.similarity(word1))
print("---------------------------------------------------------------------")
print("OBSERVATIONAL NOTE: Interesting that 'fag' and 'cigarette' has only 10% similarity, while 'cigarette' and 'tulip' 23%.")

# NOTE: 
# Re-running 'example.py' with 'en_core_web_sm' gave the following warning about model not having word vectors:

# UserWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, 
# parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, 
# which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models 
# instead if available.

# With small models ('sm' version) similarity percentages have significantly reduced about 20-30%