from setuptools import setup, find_packages

setup(
    name='gspreadplusplus',
    version='1.0.3',
    author='Daniel Simanek',
    author_email='daniel.simanek@decathlon.com',
    description='Advanced functions using the gspread library, used for making the code less bloated.',
    long_description=open('README.md').read(),  # Long description from the README file
    long_description_content_type='text/markdown',
    url='https://github.com/daniel-simanek/gspreadplusplus',
    packages=find_packages(),
    py_modules=['gspreadplusplus'],
    install_requires=[
        'gspread',
        'oauth2client',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
