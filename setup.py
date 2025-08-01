from setuptools import find_packages, setup

setup(
    name='dir-checker',
    version='1.0.0',
    description='Configurable pre-commit hook for validating directory structure and mandatory files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nitin Bisht',
    author_email='',
    url='https://github.com/nitinnbisht/dir-checker',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dir-checker=dir_checker.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
