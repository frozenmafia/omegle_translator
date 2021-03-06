import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyomegle-translator", # Replace with your own username
    version='0.1.6',
    author="Shivank Anchal",
    author_email="shivajay295@gmail.com",
    description="A small example package,to communicate on omegle in any language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://githuself.b.com/frozenmafia/omego_transo.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'googletrans',
        'selenium',
        'WConio2'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    download_url='https://github.com/frozenmafia/omegle_translator/archive/=0.1.2.tar.gz'
)
