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
    packages=find_packages(), # Automatically find packages in the directory i.e. (__init__.py) files (your own modules)
    install_requires=get_requirements("requirements.txt"),
    #install_requires=['pandas', 'numpy', 'scikit-learn', 'flask']
)
"""
Summary of -e . and requirements:

1. -e . in requirements.txt
   - Editable mode: links your local project instead of copying.
   (Your project folder  --->  Python’s site-packages folder in the virtual environment)
   (make your own modules/packages editable and live inside the virtual environment.
   It does not affect external libraries like numpy or pandas; those are handled separately )
   - Runs setup.py automatically to:
       1. Build your package
       2. Install it
       3. Install dependencies (install_requires)
   - Changes in your code are immediately reflected when importing.

2. setup.py vs requirements.txt
   - packages=find_packages() → installs your project code (__init__.py folders)
   - install_requires in setup.py → installs external libraries
   - requirements.txt → also lists external libraries, can include -e .

   Note: Pip merges dependencies; nothing is installed twice.

3. Why -e . at the bottom
   - Pip installs requirements top to bottom.
   - External libraries first → ensures setup.py can run.
   - -e . last → links your project live.

4. Virtual environment
   - Always use one to isolate project dependencies.
   - Safe to experiment and prevents conflicts.

5. Simple translation:
   Hey Python,
     1. Install external libraries (numpy, pandas…)
     2. Run my project (-e .) so it’s linked live
     3. Build package and install its dependencies

   packages = my code
   install_requires / requirements.txt = libraries my code depends on
   -e . = link my project live, auto-build, editable
"""
