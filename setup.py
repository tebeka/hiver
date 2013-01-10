try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='hive',
    version='0.1.0',
    description='Hive thrift client',
    long_description=open('README.rst').read(),
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    license='MIT',
    url='https://bitbucket.org/tebeka/hive',
    py_modules=['hive'],
    install_requires=['thrift'],
)
