from setuptools import setup, find_packages

setup(
    name='filetoolkit',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['pycryptodome', 'chardet'],
    entry_points={
        'console_scripts': [
            'filetoolkit=filetoolkit.cli:main',
        ],
    },
    author='Your Name',
    description='A simple multi-functional file toolkit.',
    license='MIT',
)
