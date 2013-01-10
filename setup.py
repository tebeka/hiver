try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='hiver',
    version='0.2.0',
    description='Hive thrift client',
    long_description=open('README.rst').read(),
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    license='MIT',
    url='https://bitbucket.org/tebeka/hive',
    packages=[
        'hiver',
        'hiver.fb303',
        'hiver.fb303_scripts',
        'hiver.hive_metastore',
        'hiver.hive_serde',
        'hiver.hive_service',
        'hiver.queryplan',
    ],
    install_requires=['thrift'],
)
