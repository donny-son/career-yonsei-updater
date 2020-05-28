import pickle


def initiate():
    PREVIOUS_UPDATES = {}
    CURRENT_UPDATES = {}
    save_obj(PREVIOUS_UPDATES, 'PREVIOUS_UPDATES')
    save_obj(CURRENT_UPDATES, 'CURRENT_UPDATES')

def save_obj(obj, name: str):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name: str):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

try:
    PREVIOUS_UPDATES = load_obj('PREVIOUS_UPDATES')
    CURRENT_UPDATES = load_obj('CURRENT_UPDATES')
except Exception as e:
    print('Please initialize pkl objects by running pickle_handler.py')

if __name__ == '__main__':
    initiate()