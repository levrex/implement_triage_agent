""" 
How to use: 

# 1. Activate conda environment (to ensure correct versions of modules, see build_conda_env.sh)
    source activate triage_env
    
# 2. Run script & supply content as flag in string format
    python script.py --input 'patient heeft ra'

"""


import re
import unicodedata
import pickle
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
import argparse
import json
import xgboost as xgb


# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True)
args = parser.parse_args()

#print(f"Input, {args.input}!")

content = args.input

# Functions
def removeAccent(text):
    """
    This function removes the accent of characters from the text.

    Variables:
        text = text to be processed
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return text

def remove_html_artefacts(line):
    """
    This function removes the html of artefacts from the text.

    Variables:
        line = text to be processed
    """
    new_line =  line.replace('\x00', '') # remove null bytes
    new_line = re.sub(r'\\[^ ]+', r'', new_line)
    new_line = new_line.replace('}', '').replace('{', '').replace('Calibri (Vietnamese)', '').replace('envelope address;', '').replace('envelope return;', '')
    
    new_line = re.sub(r'(Kop 1|Kop 2|Kop 3|Subtle Reference|Bottom of Form|Top of Form|No List|No Spacing)', r'', new_line)
    
    # remove font names
    new_line = re.sub(r'(Default Paragraph Font|Times New Roman|Calibri|Arial|Helvetica|Cambria) [^ ]+;', r'', new_line)
    new_line = re.sub(r'(Default Paragraph Font|Times New Roman|Calibri|Arial|Helvetica|Cambria);', r'', new_line)
    new_line = re.sub(r'Cambria [^ ]+ [^ ]+;', r'', new_line)
    
    # Remove special elements
    new_line = re.sub(r'(Medium|Light|Intense|Quote|Colorful|Dark|Table|Balloon|Ballontekst|List|footnote|Normal|Grid|Closing|Body|table) .+;', r'', new_line)
    new_line = re.sub(r'(macro|toa|toc|index|footnote|line|page|endnote|annotation|heading|Heading|Block|Plain|Document|Outline|HTML) [^ ]+;', r'', new_line)
    new_line = re.sub(r'(Signature|Hyperlink|Date|caption|Normal|bottom|heading|Heading|Outline|Subtle|Form|Bottom|Emphasis|Strong|footer|header|Closing|List|Kop|Char|iText|1T3XT|Note|Salutation|Form|Top|TOC|bottom|HTML|Followed|Spacing|Plain)', r'', new_line)#new_text = re.sub(r'\\[^ ]+', r'', text)
    ## Remove caps (in case it is from html or rich text, inferring caps lock) unless it is in another word (e.g. capsule)
    new_line = re.sub(r'\b(caps)\b', r'', new_line)
    
    # Remove HEX numbers
    new_line = re.sub(r"(?<!'|-)\b[0-9a-fA-F]{4,}\b", r'', new_line)
    new_line = re.sub(' +', ' ',new_line)
    # remove all "'"
    new_line = re.sub("(?<!N)'", ' ',new_line)
    new_line = re.sub("(?<!\));", '', new_line)
    new_line = re.sub("(N'([0-9a-fA-F\-]){4,})", "\g<1>'", new_line) # add quote
    new_line = new_line.replace(" , NULL)", ", NULL)\n'").replace('Calibri', '').replace('( )', '').replace('http://schemas.microsoft.com/office/word//wordml', '')
    new_line = new_line.replace('E-mail', "")
    return new_line 

def replace_dates(date_text):
    pattern = re.compile(r'\d{2}-\d{2}-\d{4}') 
    return re.sub(pattern, '[DATE]', date_text)

def preprocess(content):
    # remove accent
    content = removeAccent(content)
    # remove dates
    content = replace_dates(content)
    # remove html artefacts
    content = remove_html_artefacts(content)
    return content


if __name__ == "__main__":
    
    ### 1 Preprocess 
    content = preprocess(content)

    ### 2 Run models 
    l_targets = ['FMS', 'RA', 'OA'] # , 'Chronic'

    d_scores = {}

    for target in l_targets:
        # import specific tfidf 
        with open('model/tfidf/tfidf_vectorizer_%s_ngram_1000iter_new.pk' % target, 'rb') as fin:
            tfidf_vectorizer = pickle.load(fin)

        # import specific xgb
        with open('model/xgb/xgb_%s_ngram_1000iter_new.pk' % target, 'rb') as fin:
            bst = pickle.load(fin)


        # Apply tfidf 
        tfidf_content = tfidf_vectorizer.transform([content])

        # Format data for classifier
        dtest = xgb.DMatrix(tfidf_content) # label=y

        # Predict diagnosis
        y_pred = bst.predict(dtest)

        # Bookmark predictions (uitslagen)
        d_scores[target] = float(y_pred[0])

    # Return predictions
    #print(d_scores)
    print(json.dumps(d_scores, indent=2)) 