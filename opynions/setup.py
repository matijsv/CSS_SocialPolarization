from setuptools import setup, find_packages

setup(
    name='opynions',
    version='1.0.0',
    url='https://github.com/matijsv/opynions/new/main/opynions',
    author='Matijs Verloo',
    author_email='matijs.verloo@gmail.com',
    description='A package for exploring rewiring opinion dynamics models',
    packages=['opynions'],    
    install_requires=['matplotlib','numpy','pandas','scipy','seaborn','networkx'],
)
