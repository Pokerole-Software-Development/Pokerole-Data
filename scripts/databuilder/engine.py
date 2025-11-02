from os.path import join, exists, isdir, dirname
from os import makedirs, listdir
from fire import Fire
from shutil import copy, rmtree

class Engine(object):
    
    def __init__(self, output_path, game_version):
        self.output_path = output_path
        self.game_version = game_version
        self.driver = None
    
    # # These functions take JSON and return a string to be outputted. 
    
    def pokedex_entry(self, entry):
        pass
    def movedex_entry(self, entry):
        pass
    def abilitydex_entry(self, entry):
        pass
    def itemdex_entry(self, entry):
        pass
    def naturedex_entry(self, entry):
        pass
    def import_images(self, source, setname):
        pass

    # # Utility
    
    def _write_to(self, data, path, mode='w'):
        self._pathgen(dirname(path))
        open(path,mode).write(data)
    
    def _pathgen(self, path, validate=False):
        '''
        Ensures a path exists, or can create it . Optionally adds a root layer. 
        Formats {game_version} with game_version.
        '''
        if validate:
            if not exists(path): raise Exception(f"ERROR: Path {path} not found!")
        else:
            makedirs(path, exist_ok=True)
        return path
    
    def _copy_imageset(self, source, output, prefix='', postfix=''):
        for img in [x for x in listdir(source) if '.png' in x]:
            sname = img.split('.')
            srdname = f'{prefix}{sname[0]}{postfix}.{sname[1]}'
            copy(join(source, img), join(output, srdname))
            # print(join(source, img), join(output, srdname))