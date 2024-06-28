from setuptools import setup

# !!!!!!! MAJOR DEBT - This is hardcoded
VERSION = "0.27.9"

# ~~~~~ Create configuration
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='tdl-client-python',
    packages=[
        'tdl',
        'tdl.audit',
        'tdl.queue',
        'tdl.queue.abstractions',
        'tdl.queue.abstractions.response',
        'tdl.queue.transport',
        'tdl.runner'
    ],
    package_dir={'': 'src'},
    install_requires=['stomp.py==8.1.2', 'requests==2.32.3'],
    version=VERSION,
    description='tdl-client-python',
    long_description=(this_directory / "README.md").read_text(),
    author='Julian Ghionoiu',
    author_email='julian.ghionoiu@gmail.com',
    url='https://github.com/julianghionoiu/tdl-client-python',
    download_url='https://github.com/julianghionoiu/tdl-client-python/archive/v{0}.tar.gz'.format(VERSION),
    keywords=['kata', 'activemq', 'rpc'],
    classifiers=[],
)
