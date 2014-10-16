
## this setup.py inspired by setup.py`s from https://github.com/meejah/txtorcon and https://github.com/habnabit/txsocksx

from setuptools import setup

__version__ = '0.0.1'
__author__ = 'David Stainton'
__contact__ = 'dstainton415@gmail.com'
__url__ = 'https://github.com/david415/txtorsocksx'
__license__ = 'GPL'
__copyright__ = 'Copyright 2014'

setup(
    name='txtorsocksx',
    description='Twisted client endpoint and parser for Tor SOCKS client',
    version = __version__,
    long_description = open('README.rst', 'r').read(),
    keywords = ['python', 'twisted', 'tor', 'twisted endpoint', 'twisted endpoint parser', 'tor socks client'],

    classifiers=['Framework :: Twisted',
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'License :: OSI Approved :: GPL License',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 2 :: Only',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Internet',
                 'Topic :: Security'],
    author = __author__,
    author_email = __contact__,
    url = __url__,
    license = __license__,

#    setup_requires=['vcversioner>=1'],
#    vcversioner={
#        'version_module_paths': ['txtorsocksx/_version.py'],
#    },

    install_requires=open('requirements.txt', 'rb').read().split(),

    packages=['txtorsocksx', 'twisted.plugins'],

)
