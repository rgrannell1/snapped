
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "snapped",
  version = "0.1.0",
  author = "Róisín Grannell",
  author_email = "r.grannell2@gmail.com",
  package = setuptools.find_packages(),
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  install_requires = [
    'docopt'
  ],
  python_requires = ">=3.5"
)
