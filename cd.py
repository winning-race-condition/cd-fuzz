import os
import sys
import json


root_dir_to_index = os.path.expanduser('~')

def log(msg):
    sys.stderr.write(msg)

class AbstractAction():

    def shell_argument(self):
        raise NotImplemented()

    def run_action(self,fles):
        raise NotImplemented()

class CDFirstAction(AbstractAction):

    def shell_argument(self):
        # Is also the default...
        return 'c'

    def run_action(self,fles):
        print("cd {}".format(fles[0][0]))

class ListFilesAction(AbstractAction):

    def shell_argument(self):
        return 'l'

    def run_action(self,fles):
        print("echo {}".format([fle[0] for fle in fles[0:10]]))


actions = [CDFirstAction(),ListFilesAction(),]

actions = {action.shell_argument():action for action in actions}


def this_dir():
    return os.path.dirname(__file__)


index_file = os.path.join(this_dir(),'index.json')

def complexity(fle_path):
    return len(fle_path) + 2 * fle_path.count(str(os.path.sep))

def add_file_to_index(fle,index,):
    index[fle] = complexity(fle)

def add_dir_to_index(dr,index,):
    index[dr] = complexity(dr)


def index_dir(d):
    index = {}
    print('index not found, recreating it at {}'.format(index_file))

    for root, dirs, fles in os.walk(root_dir_to_index):
        path = root.split(os.sep)

        for fle in fles:
            add_file_to_index(os.path.join(root,fle),index,)

        for dr in dirs:
            add_dir_to_index(os.path.join(root,dr),index,)
    return index


if __name__ == '__main__':

    # Getting the arguments from the shell
    import sys
    args = sys.argv[1:]

    #print('>',args)

    # Parsing the arguments from the shell.
    # What do we want to do?
    if args and args[0] in actions:
        action = actions[args[0]]
        args = args[1:]
    else:
        action = actions['c']
    
    try:
        with open(index_file,'r') as fin:
            index = json.load(fin)
    except:
        index = index_dir(root_dir_to_index)
        with open(index_file,'w') as fout:
            json.dump(index,fout)

    if args:

        candidates = sorted([(k,v) for k,v in index.items() if all([arg in k for arg in args])],key=lambda kv: kv[1])

        #print(candidates[0][0])
        if candidates:
            action.run_action(candidates)
        else:
            log('no candidates found for query!')


