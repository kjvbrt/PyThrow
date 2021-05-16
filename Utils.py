

def random_string(size: int = 12) -> str:
    '''
    Random string generator.
    '''
    from random import choice
    from string import ascii_lowercase, digits

    chars = ascii_lowercase + digits

    return ''.join(choice(chars) for _ in range(size))


def create_dir(dirpath: str) -> None:
    '''
    Create directory on disk
    '''
    from os import path, makedirs

    if len(dirpath) == 0:
        return

    dirpath = dirpath.strip()

    if dirpath[0] == '/':
        raise Exception('Using absolute path not allowed!')

    if '..' in dirpath:
        raise Exception('Using ".." not allowed!')

    if not path.exists(dirpath):
        makedirs(dirpath)


def make_ratio(obj1, obj2):
    if 'TH1D' in obj1.ClassName() and 'TH1D' in obj2.ClassName():
        obj = obj1.Clone(obj1.GetName() + '__' + obj2.GetName() +
                         '_' + random_string())
        obj.Divide(obj2)

        return obj

    raise Exception('This combination of objects does not support division!')
