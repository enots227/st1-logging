  
from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='st1-logging',
    version='0.0.1',
    description='Common logging related function shared between applications.',
    author='Stone Sommers',
    author_email='enots227@gmail.com',
    include_package_data=True,
    packages=find_packages(
        exclude=['tests.*', 'tests']
    ),
    install_requires=[
        'python-json-logger>=2.0.2'
    ]
)