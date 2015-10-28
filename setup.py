from distutils.core import setup

VERSION = '0.0.1'

setup(
    name = 'tdl-client-python',
    packages = ['tdl'],
    package_dir = {'': 'src'},
    version = VERSION,
    description = 'tdl-client-python',
    author = 'Tim Preece',
    author_email = 'tdpreece@gmail.com',
    url = 'https://github.com/julianghionoiu/tdl-client-python',
    download_url = 'https://github.com/peterldowns/tdl-client-python/tarball/' + VERSION,
    keywords = ['kata', 'activemq', 'rpc'],
    classifiers = [],
)