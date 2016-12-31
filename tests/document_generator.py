import random
import uuid
import sys


class DocumentGenerator:
    """
    Fake document generator::

        def nested_item():
            nested_gen = DocumentGenerator()
            nested_gen.set_template({'user': 'email', 'hash': 'gid', 'posts': small_int})
            return nested_gen.gen_doc()

        generator = DocumentGenerator()
        generator.set_template({'id': 'index', 'user': nested_item, 'url': 'url', 'age': 43, 'one_of': ['male', 'female', 'both']})
        print(generator.gen_docs(5))

    """


    def __init__(self):
        self.index = 0
        self.fields = {}

    def gen_word(self):
        #http://norvig.com/mayzner.html
        vowels = 'aaeeeeiioou'
        cons = 'bccddddffgghhhhhjkllllmmnnnnnnnppqrrrrrttttttttvwy'
        bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of', 'ed',
                   'is', 'it', 'al', 'ar', 'st', 'to', 'nt', 'ng', 'se', 'ha', 'as', 'ou', 'io', 'le', 've', 'co',
                   'me', 'de', 'hi', 'ri', 'ro', 'ic', 'ne', 'ea', 'ra', 'ce', 'li', 'ch', 'll', 'be', 'ma', 'ma',
                   'si', 'om', 'ur',
                   'th', 'he',
                   'th', 'he', 'in', 'er'
                   'th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or', 'te', 'of', 'ed',
                   ]



        word_lens = [2,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
                     8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,11,11,11,11,11,12,12,
                     12,13,13,15,16]

        word = ""
        word_len = random.choice(word_lens)

        while len(word) < word_len:
            junction = random.random()
            if( junction < .5 ):
                word += random.choice(bigrams)
            elif( junction < .75 ):
                word += random.choice(cons) + random.choice(vowels)
            elif( junction < .85):
               word += random.choice(vowels)
            else:
                word += random.choice(cons)

        return word

    def gen_sentence(self, min_words = 3, max_words = 15):
        sentence = ""
        for i in range(random.randint(min_words, max_words)):
            sentence += self.gen_word() + " "

        return sentence.strip()


    def gen_paragraph(self, min_sentences=2, max_sentences=15):
        paragraph = ""
        for i in range(random.randint(min_sentences, max_sentences)):
            paragraph += self.gen_sentence().capitalize() + ". "

        return paragraph.strip()

    def gen_domain(self):

        domain = ""
        # https://w3techs.com/technologies/overview/top_level_domain/all
        tld = ['com', 'com', 'com', 'com', 'com', 'org', 'gov', 'biz', 'net', 'tv', 'us', 'edu', 'ru', 'co.uk', 'fr', 'jp']

        junction = random.random()

        if junction < .75:
            domain = "%s.%s" % (self.gen_word(), random.choice(tld))
        elif junction < .9:
            domain = "%s.%s.%s" % (self.gen_word(), self.gen_word(), random.choice(tld))
        else:
            domain = "%s%i.%s" % (self.gen_word(), random.randint(1,999), random.choice(tld))
        return domain

    def gen_email(self):
        email = ""
        junction = random.random()
        domain = self.gen_domain()

        if junction < .75:
            email = "%s@%s" % (self.gen_word(), self.gen_domain())
        elif junction < .9:
            email = "%s.%s@%s" % (self.gen_word(), self.gen_word(), self.gen_domain())
        else:
            email = "%s%i@%s" % (self.gen_word(), random.randint(1, 999), self.gen_domain())

        return email

    def gen_phone(self):
        return "%i-%i-%s" % (random.randint(200,999), random.randint(111,999), str(random.randint(0,9999)).zfill(4))

    def gen_gid(self):
        return str(uuid.uuid4())

    def set_template(self, template):
        self.template = template

    def gen_index(self):
        self.index += 1
        return self.index

    def gen_url(self):
        mimes = ['html', 'html', 'html', 'html', 'asp', 'jsp', 'php', 'png', 'jpg', 'gif']
        junction = random.random()
        url = self.gen_domain()

        proto = "http"
        if random.random() < .50:
            proto = "https"

        url = "%s://%s" % (proto, url)

        path_depth = random.randint(0,4)
        for i in range(path_depth):
            url += "/%s" % self.gen_word()

        if random.random() < .50:
            url = "%s.%s" % (url, random.choice(mimes))

        return url

    def small_int(self):
        return random.randint(0, 99)

    def integer(self):

        return random.randint(0, sys.maxsize)

    def small_float(self):
        return random.random()

    def floating(self):
        return random.random() * sys.maxsize

    def gen_doc(self):
        doc = {}
        type_map = {
            'index': self.gen_index,
            'word': self.gen_word,
            'sentence': self.gen_sentence,
            'paragraph': self.gen_paragraph,
            'email': self.gen_email,
            'gid': self.gen_gid,
            'url': self.gen_url,
            'small_int': self.small_int,
            'integer': self.integer,
            'small_float': self.small_float,
            'floating': self.floating
        }

        for field in self.template:
            if isinstance(self.template[field], list):
                doc[field] = random.choice(self.template[field])
            elif self.template[field] in type_map:
                doc[field] = type_map[self.template[field]]()
            elif callable(self.template[field]):
                doc[field] = self.template[field]()

            else:
                doc[field] = self.template[field]
        return doc


    def gen_docs(self, count):
        docs = []
        for i in range(count):
            docs.append(self.gen_doc())
        return docs



