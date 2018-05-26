from sklearn.datasets import load_files

from src import xml_reader, clarin_api
from src.corpus_data import show_summary_plot

raw_wiki = "../data/wiki/raw"
text_wiki = "../data/wiki/text"
ccl_wiki = "../data/wiki/ccl"


# lemma_dir = "../data/korpus/lemma"
# text_category = "../data/korpus/text"
# ccl_category = "../data/korpus/ccl"
# lemma_category = "../data/korpus/lemma"
# raw_files = "../data/korpus/raw"

# redistribute_to_categories_wiki(raw_wiki, categories_wiki)

show_summary_plot(text_wiki, 100)


# read files
# files = xml_reader.read_files_from_dir(path=raw_files, max_per_dir=800)

# distribute to categories
# corpus_data.redistribute_to_categories(files, text_category, min_per_category=200, max_per_category=300)


def create_ccl_files_lemma():
    # create ccl files - lemma
    text_data = load_files(text_wiki)
    files = [f for f in text_data.filenames]
    for input_file in files:
        output_file = input_file.replace("data/wiki/text", "data/wiki/ccl", 1)
        clarin_api.process_text(input_file, output_file)


def ccl_to_lemma():
    # ccls to lemma
    ccl_data = load_files(ccl_wiki)
    files = [f for f in ccl_data.filenames]
    for input_file in files:
        output_file = input_file.replace("data/wiki/ccl", "data/wiki/lemma", 1)
        xml_reader.ccl_to_lemma(input_file, output_file)


def ccl_to_lemma_nouns():
    #ccls to lemma nouns
    ccl_data = load_files(ccl_wiki)
    files = [f for f in ccl_data.filenames]
    for input_file in files:
        output_file = input_file.replace("data/wiki/ccl", "data/wiki/lemma", 1)
        xml_reader.ccl_to_lemma(input_file, output_file)