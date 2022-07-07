from setuptools import setup, Extension
from pathlib import Path 

with open("README.md", "r") as fh:
    long_description = fh.read()

module = Extension('spec_con',
                   sources = ['spec_conv/spec_con.c'],
                   extra_compile_args=['-Wall', '-pedantic', '-lm', '-O2'], 
                   library_dirs=["/home/alletro/python_packages"])

    
setup(
    name="spec_conv", # Replace with your own username
    version="0.0.1",
    author="Carl Wheldon, Ross Allen",
    author_email="c.wheldon@bham.ac.uk",
    description="Gamma spectrum conversion file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Allentro/spec_conv",
    packages=setuptools.find_packages(),
    entry_points ={'console_scripts': ['spec_conv = spec_conv.commandline:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'argparse',
        'pandas', 
        'pexpect'],
    #cmdclass={'install': CustomInstall},
    #include_package_data=True,
    ext_modules=[module]
)
