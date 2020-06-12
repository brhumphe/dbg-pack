import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="DbgPack",
        version="0.0.1",
        author="Benjamin Humpherys",
        description="A tool for reading and extracting Dbg .pack files",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/brhumphe/dbg-pack",
        packages=setuptools.find_packages(),
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: GNU General Public License (GPL)",
                "Operating System :: OS Independent",
        ],
)
