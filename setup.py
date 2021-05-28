import os
from setuptools import setup, find_packages


def read_file(fname):
    """Read a local file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='mkdocs-simple-tags',
    version='0.5.1',
    description="Allow the usage of simple_tags specified in each markdown document's metadata",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs markdown tags',
    url='',
    author='Tai Vo',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.1',
        'jinja2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['*.tests']),
    package_data={'simple_tags': ['templates/*.md.template']},
    entry_points={
        'mkdocs.plugins': [
            'simple-tags = simple_tags.plugin:SimpleTagsPlugin'
        ]
    }
)
