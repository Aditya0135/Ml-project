from setuptools import find_packages, setup
from typing import List
## Meta data about your package

HYPEN_E_DOT = '-e .'
## we would need 100 of requirements so we would create a function
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name = 'mlproject',
    version='0.0.1',
    author='Aditya',
    author_email='adityabatlawala@gmail.com',
    packages=find_packages(), # Automatically find packages in the directory i.e. (__init__.py) files
    install_requires=get_requirements("requirements.txt"),
    #install_requires=['pandas', 'numpy', 'scikit-learn', 'flask']
)
