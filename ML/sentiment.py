import string 

data = [
    ("I love this movie", 1),
    ("This film is terrible", 0),
    ("Amazing experience", 1),
    ("I hate this", 0),
]


def preprocess(text):
    text = text.lower()
    text = text.translate(text.maketrans('','',string.punctuation))
    text = text.split(' ')

    stopwords = {'the', 'a', 'of'}
    sentence = []

    for word in text:
        if word not in stopwords:
            sentence.append(word)
    return sentence

for x in range(len(data)):
    sentence, label = data[x]
    data[x] = (preprocess(sentence), label)

vocab_set = set()

for tokens, label in data:
    for word in tokens:
        vocab_set.add(word)

vocab_list = sorted(list(vocab_set))

word_to_index = {}
index = 0
for word in vocab_list:
    word_to_index[word] = index
    index += 1

print(word_to_index)


vectors = []

for tokens, label in data:
    vector = [0] * len(word_to_index)
    for word in tokens:
        if word in word_to_index:
            index = word_to_index[word]
            vector[index] += 1
    vectors.append((vector, label))

print(vectors)
