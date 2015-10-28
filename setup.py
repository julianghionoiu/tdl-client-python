from distutils.core import setup

VERSION = '0.0.3'

setup(
    name = 'tdl-client-python',
    packages = ['tdl'],
    package_dir = {'': 'src'},
    version = VERSION,
    description = 'tdl-client-python',
    author = 'Tim Preece, Julian Ghionoiu',
    author_email = 'tdpreece@gmail.com, julian.ghionoiu@gmail.com',
    url = 'https://github.com/julianghionoiu/tdl-client-python',
    download_url = 'https://github.com/julianghionoiu/tdl-client-python/archive/v{0}.tar.gz'.format(VERSION),
    keywords = ['kata', 'activemq', 'rpc'],
    classifiers = [],
)