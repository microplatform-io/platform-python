try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description         = 'Platform Python Core Library',
    author              = 'Bryan Moyles',
    author_email        = 'bmoy117@gmail.com',
    version             = '0.0.1',
    install_requires    = ['protobuf==2.6.1'],
    packages            = ['microplatform'],
    name                = 'Platform Python'
)