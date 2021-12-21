#!/usr/bin/env python
# coding: utf-8

# In[3]:


##enter your path here where you saved the resumes
import os
mypath='C:\\Users\\Fayaz\\Downloads\\Chubb\\Chubb' 
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
#print(onlyfiles)
len(onlyfiles)


# A Python port of the Apache Tika library, According to the documentation Apache tika supports text extraction from over 1500 file formats. pip install tika

# In[10]:


#pip install tika
from tika import parser
#filename="C:\\Users\\Fayaz\\Downloads\\Chubb\\Chubb\\MeghaHajeri[14_0].doc"
#docx_path="C:\\Users\\Fayaz\\Downloads\\Chubb\\Chubb\\Akshaya[9_0].docx"
#pdf_path="C:\\Users\\Fayaz\\Downloads\\Chubb\\Chubb\\Aishwarya[5_0].pdf"
#parsed = parser.from_file(pdf_path)
#print(parsed["metadata"]) #To get the meta data of the file
#print(parsed["content"]) # To get the content of the file
#count=0
#for file in onlyfiles:
    
    #parsed=parser.from_file(file)
    #print(parsed["content"])
    #count+=1
#print(count)
for file in onlyfiles:
    def extract_text_from_file(file):
        #txt = docx2txt.process(docx_path)
        parsed = parser.from_file(file)
        txt=parsed["content"]
        if txt:
            return txt.replace('\t', ' ')
        return None
    
    if __name__ == '__main__':
        TEXT=extract_text_from_file(file)
        #print(TEXT)
    


# In[11]:


from tika import parser
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


# In[21]:


#count=0
import re
import nltk
nltk.download('stopwords')
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'English',
]
RESERVED_WORDS = [
    'school',
    'college',
    'univers',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
]
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S','C.A.','c.a.','B.Com','B. Com','M. Com', 'M.Com','M. Com .',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'PHD', 'phd', 'ph.d', 'Ph.D.','MBA','mba','graduate', 'post-graduate','5 year integrated masters','masters',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII','Bachelor'
        ]

for file in onlyfiles:
    def extract_text_from_file(file):
        #txt = docx2txt.process(docx_path)
        parsed = parser.from_file(file)
        txt=parsed["content"]
        if txt:
            return txt.replace('\t', ' ')
        return None
    def extract_names(txt):
        person_names = []

        for sent in nltk.sent_tokenize(txt):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    person_names.append(
                        ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                    )
        return person_names
    #count+=1
    def extract_phone_number(input_text):
        phone = re.findall(PHONE_REG, input_text)

        if phone:
            number = ''.join(phone[0])

            if input_text.find(number) >= 0 and len(number) < 16:
                return number
        return None
    def extract_emails(input_text):
        return re.findall(EMAIL_REG, input_text)
    
    def extract_skills(input_text):
        stop_words = set(nltk.corpus.stopwords.words('english'))
        word_tokens = nltk.tokenize.word_tokenize(input_text)

        # remove the stop words
        filtered_tokens = [w for w in word_tokens if w not in stop_words]

        # remove the punctuation
        filtered_tokens = [w for w in word_tokens if w.isalpha()]

        # generate bigrams and trigrams (such as artificial intelligence)
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

        # we create a set to keep the results in.
        found_skills = set()

        # we search for each token in our skills database
        for token in filtered_tokens:
            if token.lower() in SKILLS_DB:
                found_skills.add(token)

    # we search for each bigram and trigram in our skills database
        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)

        return found_skills
    def extract_education_org(input_text):
        organizations = []

        # first get all the organization names using nltk
        for sent in nltk.sent_tokenize(input_text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                    organizations.append(' '.join(c[0] for c in chunk.leaves()))

        # we search for each bigram and trigram for reserved words
        # (college, university etc...)
        education = set()
        for org in organizations:
            for word in RESERVED_WORDS:
                if org.lower().find(word) >= 0:
                    education.add(org)

        return education
    def extract_education(input_text):
      # regex = re.compile(r"(B\.Tech|MSc).*?(?<=-)\s+(\d+)")
      # match = regex.match(resume_text)
        list123 = []
        for i in EDUCATION:
            reg = "(" + re.escape(i) + ").*?(?<=-)\s+(\d+)"
            regex = re.compile(reg, flags=re.M | re.IGNORECASE)
            for mat in regex.findall(input_text):
                  list123.append(mat)
        return list123 
    
    
    
    if __name__ == '__main__':
        TEXT=extract_text_from_file(file)
        names = extract_names(TEXT)
        if names:
            print(names[0])
        phone_number = extract_phone_number(TEXT)
        print(phone_number)
        emails = extract_emails(TEXT)
        if emails:
            print(emails[0]) 
        skills = extract_skills(TEXT)
        print(skills)
        education_information = extract_education_org(TEXT)
        print(education_information)
        qualification=extract_education(TEXT)
        print(qualification)
        #print(TEXT)
        #print(count)


# In[ ]:




