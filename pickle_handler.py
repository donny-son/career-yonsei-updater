import pickle
from config import ROOT_DIR

def initiate():
    PREVIOUS_JOB_UPDATES = {}
    CURRENT_JOB_UPDATES = {}
    PREVIOUS_NEWS_UPDATES = {}
    CURRENT_NEWS_UPDATES = {}
    save_obj(PREVIOUS_JOB_UPDATES, 'PREVIOUS_JOB_UPDATES')
    save_obj(CURRENT_JOB_UPDATES, 'CURRENT_JOB_UPDATES')
    save_obj(PREVIOUS_NEWS_UPDATES, 'PREVIOUS_NEWS_UPDATES')
    save_obj(CURRENT_NEWS_UPDATES, 'CURRENT_NEWS_UPDATES')

def save_obj(obj, name: str):
    with open(ROOT_DIR+'/'+'obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)  # 4


def load_obj(name: str):
    with open(ROOT_DIR+'/'+'obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

try:
    PREVIOUS_JOB_UPDATES = load_obj('PREVIOUS_JOB_UPDATES')
    CURRENT_JOB_UPDATES = load_obj('CURRENT_JOB_UPDATES')
    PREVIOUS_NEWS_UPDATES = load_obj('PREVIOUS_NEWS_UPDATES')
    CURRENT_NEWS_UPDATES = load_obj('CURRENT_NEWS_UPDATES')
except Exception as e:
    print('Please initialize pkl objects by running pickle_handler.py')

if __name__ == '__main__':
    if input('initialize pickles? [Y/n]') == 'Y':
        initiate()
        print('Initiation Complete. Please run scheduled_run.py')
    else:
        print('Skip Initialization')
    PREVIOUS_JOB_UPDATES = load_obj('PREVIOUS_JOB_UPDATES')
    CURRENT_JOB_UPDATES = load_obj('CURRENT_JOB_UPDATES')
    PREVIOUS_NEWS_UPDATES = load_obj('PREVIOUS_NEWS_UPDATES')
    CURRENT_NEWS_UPDATES = load_obj('CURRENT_NEWS_UPDATES')
    print(PREVIOUS_JOB_UPDATES)
    print(CURRENT_JOB_UPDATES)
    print(PREVIOUS_NEWS_UPDATES)
    print(CURRENT_NEWS_UPDATES)