from src import RAG
import argparse

parser = argparse.ArgumentParser(description='Option to choose')
parser.add_argument('-o', '--option', type=int)
args = parser.parse_args()
option = args.option
if option == 1:
    doc = "https://eye.hms.harvard.edu/files/eye/files/difficult-conversations-summary.pdf"
    source = "PDF"
if option == 2:
    doc= './difficult-conversations-summary.pdf'
    source = "PDF"
if option == 3:
    doc = 'https://alexchen373.medium.com/here-are-my-key-highlights-taken-from-the-book-difficult-conversations-by-douglas-stone-bruce-eb516953d07a'
    source = "Web"
if option == 4:
    doc = 'https://youtu.be/OWpP46NIMQg?si=DTHTJ63Ied60-rwp'
    source = "YouTube"
prompt = "tell me the main ideas"
print('Creating your answer')
rag = RAG(doc, source)
print('RAG created!')
answer = rag.qa(prompt)
print(answer)