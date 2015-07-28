try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    description         = 'Platform Python Core Library',
    author              = 'Bryan Moyles',
    author_email        = 'bmoy117@gmail.com',
    version             = '0.0.2',
    install_requires    = ['protobuf==2.6.1', 'pika==0.9.8'],
    packages            = ['microplatform'],
    name                = 'Platform Python'
)
