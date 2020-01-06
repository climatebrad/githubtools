import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='githubtools',
     version='0.1',
     scripts=['githubtools'] ,
     author="Brad Johnson",
     author_email="climatebrad@gmail.com",
     description="A Github search and cloning utility package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/climatebrad/githubtools",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License (GPL)",
         "Operating System :: OS Independent",
     ],
 )
