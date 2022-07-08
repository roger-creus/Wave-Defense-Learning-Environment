from setuptools import setup 
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='WaveDefense', version='0.0.3', install_requires=['gym', 'pygame', 'numpy'], author = "Roger Creus", author_email = "creus99@protonmail.com", long_description=long_description, long_description_content_type='text/markdown')