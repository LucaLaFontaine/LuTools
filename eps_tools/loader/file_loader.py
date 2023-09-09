import pandas as pd
import yaml
import os
from glob import glob
import inspect


def import_config(configFolder=''):
    """
Import all config files from the supplied folder. Defaults to the root folder

Any files ending in 'config.yaml' will be treated. So you could have a formatting config called 'format.config.yaml'

Parameters:
configFolder: string, default: empty
    """

    # Load any config files
    yamlFiles = glob(os.getcwd()+configFolder+'/**/*config.yaml', recursive=True)
    yamlFiles = [file.replace(os.getcwd(), '').lstrip('/\\') for file in yamlFiles]
    xlFiles = glob(os.getcwd()+configFolder+'/**/*config.xlsx', recursive=True)
    xlFiles = [file.replace(os.getcwd(), '').lstrip('/\\') for file in xlFiles]
    xlFiles = [file for file in xlFiles if '~' not in file]

    if yamlFiles or xlFiles:
        print(f'Loading config files: {yamlFiles+xlFiles}')
    else:
        configFile = 'config.yaml'
        func_dir_path = '/'.join(os.path.abspath(inspect.getfile(import_config)).split('\\')[0:-1])
        print(f"""There doesn't appear to be a config file in the root of your folder. \nLoading the default config from here:\n{func_dir_path}/{configFile}""")
        yamlFiles.append(f'{func_dir_path}/{configFile}')

    config = {}
    for file in yamlFiles:
        with open(file) as f:
            config.update(yaml.load(f, Loader=yaml.FullLoader))
            f.close()

    for file in xlFiles:
        df = pd.read_excel(file)
        dictName = df.columns[0]
        df.columns = df.iloc[0 ,:]
        df = df.iloc[1: ,:]
        config.update({dictName: df.T.to_dict()})

    return config

def getFiles(path='*', recursive=False, fileTypes=['']):
    """
Get list of all files in a supplied path. Can pass file types

Parameters:
path: string, default: empty
recursive: bool, default: False

Returns: list
    """
    files = []
    for fileType in fileTypes:
        files.extend(glob(path+fileType, recursive=recursive))

    return list(set(files))

def getExcelDFs(path='*', recursive=False, verbose=False,):
    """
Import all Excel files from a path into a list of DataFrames

Parameters:
path: string, default: '*'
recursive: bool, default: False
verbose: bool, default: False

verbose: Print the file list found by the path   

Returns: list of DataFames
    """
    fileTypes = ['.xlsx', '.xlsm' , '.xls',]
    files = getFiles(path=path, recursive=recursive, fileTypes=fileTypes)

    if verbose:
        print(f'File list:\n{files}\n')

    dfList = []
    for file in files:
        if verbose:
            print(f'Importing file: {file}')
        chunk = pd.read_excel(file,)
        dfList.append(chunk)
    return dfList







class DataLoader:
    def __init__(self, configFile='config.yaml'):

        self.config = self.import_config() 

        return
    
    def import_config(self, configFolder=''):
        """
Import all config files from the supplied folder. Defaults to the root folder

Any files ending in 'config.yaml' will be treated. So you could have a formatting config called 'format.config.yaml'

Parameters:
    configFolder: string, default: empty
        """

        # Load any config files
        files = glob(os.getcwd()+configFolder+'/**/*config.yaml', recursive=True)
        files = [file.replace(os.getcwd(), '').lstrip('/\\') for file in files]
        # print(configFolder+'/**/*config.yaml')

        if files:
            print(f'Loading config files: {files}')
        else:
            configFile = 'config.yaml'
            self.func_dir_path = '/'.join(os.path.abspath(inspect.getfile(self.import_config)).split('\\')[0:-1])
            print(f"""There doesn't appear to be a config file in the root of your folder. \nLoading the default config from here:\n{self.func_dir_path}/{configFile}""")
            files.append(f'{self.func_dir_path}/{configFile}')

        config = {}
        for file in files:
            with open(file) as f:
                config.update(yaml.load(f, Loader=yaml.FullLoader))
                f.close()

        return config
    
    def getFiles(self, path='*', recursive=False, fileTypes=['']):
        """
Get list of all files in a supplied path. Can pass file types

Parameters:
    path: string, default: empty
    recursive: bool, default: False

Returns: list
        """
        files = []
        for fileType in fileTypes:
            files.extend(glob(path+fileType))

        return list(set(files))
    
    def getExcelDFs(self, path='*', recursive=False, verbose=False,):
        """
Import all Excel files from a path into a list of DataFrames

Parameters:
    path: string, default: '*'
    recursive: bool, default: False
    verbose: bool, default: False

 verbose: Print the file list found by the path   

Returns: list of DataFames
        """
        fileTypes = ['.xlsx', '.xlsm' , '.xls',]
        files = self.getFiles(path=path, recursive=recursive, fileTypes=fileTypes)

        if verbose:
            print(f'File list:\n{files}\n')

        dfList = []
        for file in files:
            if verbose:
                print(f'Importing file: {file}')
            chunk = pd.read_excel(file,)
            dfList.append(chunk)
        return dfList


if __name__ == "__main__":
    loader = DataLoader()
    config = loader.import_config()
    print(config)
    # return