import pickle
from config import ROOT_DIR

def initiate():
    PREVIOUS_UPDATES = {}
    CURRENT_UPDATES = {}
    save_obj(PREVIOUS_UPDATES, 'PREVIOUS_UPDATES')
    save_obj(CURRENT_UPDATES, 'CURRENT_UPDATES')

def save_obj(obj, name: str):
    with open(ROOT_DIR+'/'+'obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)


def load_obj(name: str):
    with open(ROOT_DIR+'/'+'obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

try:
    PREVIOUS_UPDATES = load_obj('PREVIOUS_UPDATES')
    CURRENT_UPDATES = load_obj('CURRENT_UPDATES')
except Exception as e:
    print('Please initialize pkl objects by running pickle_handler.py')

if __name__ == '__main__':
    if input('initialize pickles? [Y/n]') == 'Y':
        initiate()
        print('Initiation Complete. Please run scheduled_run.py')
    else:
        print('Skip Initialization')
    PREVIOUS_UPDATES = load_obj('PREVIOUS_UPDATES')
    CURRENT_UPDATES = load_obj('CURRENT_UPDATES')
    print(PREVIOUS_UPDATES)
    print(CURRENT_UPDATES)