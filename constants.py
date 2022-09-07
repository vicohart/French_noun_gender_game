DATABASE = r'C:\Users\victorlh\OneDrive\Documents\coding\corpus_coding\Lexique383\french_nounds_gender_game\lexique.db'

WORD_COLLECTION_SIZE = 100

WORDS_PER_GAME = 15

PLAYER_ID = 1

CONSONANT_ARTICLES = {
    'le': {'choices': ('le', 'la', 'le/la'), 'frequency': 10}, 
    'un': {'choices': ('un', 'une', 'un/une'), 'frequency': 10}, 
    'ce': {'choices': ('ce', 'cette', 'ce/cette'), 'frequency': 5}, 
    'mon': {'choices': ('mon', 'ma', 'mon/ma'), 'frequency': 1}, 
    'son': {'choices': ('son', 'sa', 'son/sa'), 'frequency': 5}, 
    'ton': {'choices': ('ton', 'ta', 'ton/ta'), 'frequency': 5}
    }
CONSONANT_KEYS = list(CONSONANT_ARTICLES.keys())
CONSONANT_FREQUENCIES = [value['frequency'] for value in CONSONANT_ARTICLES.values()] 

VOWEL_ARTICLES = {
    'un': {'choices': ('un', 'une', 'un/une'), 'frequency': 10}, 
    'ce': {'choices': ('cet', 'cette', 'cet/cette'), 'frequency': 5}
    }
VOWEL_KEYS = list(VOWEL_ARTICLES.keys())
VOWEL_FREQUENCIES = [value['frequency'] for value in VOWEL_ARTICLES.values()] 

VOWELS = ('a', 'â', 'e', 'é', 'ê', 'i', 'î', 'o', 'ô,' 'u', 'û')