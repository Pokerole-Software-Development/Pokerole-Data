from os.path import join, exists
from os import makedirs
from fire import Fire

class DataBuilder(object):
    """
    A template for objects that build Data Objects from a Dataset. Should be Extended.

    :param root: Base directory of your Dataset.
    :param version: A sufolder under the root to differentate versions in some paths.
    """
    
    def __init__(self, root='../', version="v2.0"):
        self.targets = {y.replace('build_',''):getattr(self,y) for y in [func for func in dir(self) if callable(getattr(self, func)) and 'build_' in func]}
        self.root=root
        self.version=version
        
    def _pathgen(self, path, root=None, does_exist=True):
        if not root: root = self.root
        full_path = join(root, path.format(version=self.version))
        
        if does_exist:
            if not exists(full_path): raise Exception(f"ERROR: Path {full_path} not found!")
        else:
            makedirs(full_path, exist_ok=True)
        
        return full_path
        
    def build_sample(self, source="", output=""):
        """
        Sample of a Build function. Takes data from a Source, processes it, and puts it
        into the output folder. If `{version}` is in either parameter, it will replaced 
        with the version provided on object creation.

        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        pass

    def update(self, *argv, 
        batch=False, 
        confirm=False):
        """
        Batch function to run all build_ functions to build data objects from 
        the dataset. 

        :param *argv: Names of Data Builds to run
        :param batch: Runs all the Data Builds configured in as part of Batch
        :param confirm: Automatically confirms each Build
        """
        
        # Decide which translations will be executed.
        updates = list(self.targets.keys()) if batch else []
        for t in argv:
            if t.lower() in self.targets:
                updates.append(t.lower())
            else:
                print(f"WARN: Target {t.lower()} not configured, Skipping...")
        updates = set(updates)
        if len(updates) == 0: return 'WARN: No Builds Selected, Cancelling...'
        
        # User confirmation of translations, unless pre confirmed.
        if not confirm: 
            conf = input(f'INFO: {updates}\nQUERY: Run these Builds? [Y/Yes]: ')
            if conf.lower() not in ['y', 'yes']:
                return "WARN: Did not confirm update, cancelling..."
        else: print(f'INFO: {updates}\nINFO: Running these translations...')
        
        # Run translations
        for t in updates:
            self._translate(t)
        print('INFO: All Builds Complete.')
        
    def _translate(self, target):
        
        
        func = self.targets[target]
        func()
        print(f'INFO: Build {target} Complete!')
        
    def help(self):
        print("""
Python Script to update run data translations. Functions with "build_" as a prefix will be
added as valid target functions from the command line automatically. This class is a base class,
it's useless on it's own. Extend it

update: 
    update [collection names], [--batch] [--subfolder Subfolder] [--confirm] [--orphans [clear]] [--orphan_clear_confirm]
        collection names     : one or more of the folders in the SRD. Optional when using --batch.
        batch                : Optional. Updates all SRD folderss
        version              : Optional. A subfolder hook for using different paths dynamically.
        confirm              : Optional. Skips confirmation step. 
        """)

if __name__ == '__main__':
    Fire(DataBuilder)