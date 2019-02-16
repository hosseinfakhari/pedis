import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fh:
    readme = fh.read()


setup(
    name='pedis',
    version=__import__('pedis').__version__,
    description='pedis',
    long_description=readme,
    author='Hossein Fakhari',
    author_email='fakhari.hossein@gmail.com',
    url='https://github.com/semilanceata/pedis/',
    packages=[],
    py_modules=['pedis'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    scripts=['pedis.py'],
    test_suite='tests')