import setuptools
import pathlib


DIR = pathlib.Path(__file__).parent
README = (DIR / 'README.md').read_text()

VERSION = '0.6.1'
DESCRIPTION = 'Lab report data analysis and LaTeX file generation'

setuptools.setup(
    name='labtex',
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/CianLM/labtex',
    project_urls={
        "Documentation" : "https://www.cianlm.dev/labtex",
    },
    author='CianLM',
    packages=['labtex'],
    install_requires=['matplotlib','numpy','scipy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)