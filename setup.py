import setuptools
import re

with open("README.rst", "r") as f:
    readme = f.read()

with open("PogoOCR/__init__.py", "r") as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="PogoOCR",
    version=version,
    description="A Python tool for running OCR on Pokemon Screenshots",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="JayTurnr/DynamicalSystem",
    author_email="jaynicholasturner@gmail.com",
    maintainer="Jay Turner",
    maintainer_email="jay@trainerdex.co.uk",
    url="https://github.com/TrainerDex/PogoOCR",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
    ],
    keywords="pokemon pokemongo trainer",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=2.6",
)
