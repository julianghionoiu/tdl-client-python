from setuptools import setup

# !!!!!!! MAJOR DEBT - This is hardcoded
VERSION = "0.26.1"

# ~~~~~ Create configuration

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
        install_requires=['stomp.py==4.1.5', 'requests==2.21.0'],
        version=VERSION,
        description='tdl-client-python',
        author='Julian Ghionoiu',
        author_email='julian.ghionoiu@gmail.com',
        url='https://github.com/julianghionoiu/tdl-client-python',
        download_url='https://github.com/julianghionoiu/tdl-client-python/archive/v{0}.tar.gz'.format(VERSION),
        keywords=['kata', 'activemq', 'rpc'],
        classifiers=[],
)
