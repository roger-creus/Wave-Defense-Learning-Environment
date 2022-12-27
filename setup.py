from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='WaveDefense',
    version='1.6', 
    install_requires=['gym==0.17.0', 'pygame', 'numpy'], 
    py_modules=['WaveDefense', 'WaveDefense.envs.wave_defense', 'WaveDefense.envs.wave_defense_no_reward', 'WaveDefense.envs.wave_defense_tabular', 'WaveDefense.envs', 'WaveDefense.envs.prefabs.bullet', 'WaveDefense.envs.prefabs.enemy_spawner', 'WaveDefense.envs.prefabs.normal_enemy', 'WaveDefense.envs.prefabs.player', 'WaveDefense.envs.prefabs'], 
    packages = find_packages(),
    include_package_data=True,
    author = "Roger Creus", 
    author_email = "creus99@protonmail.com", 
    long_description=long_description, 
    long_description_content_type='text/markdown')