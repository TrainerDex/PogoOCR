import setuptools
import re

with open("README.md", "r") as f:
    readme = f.read()

with open("PogoOCR/__init__.py", "r") as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="PogoOCR",
    version=version,
    author="Jay Turner",
    author_email="jay@trainerdex.co.uk",
    description="A Python tool for running OCR on Pokemon Screenshots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TrainerDex/PogoOCR",
    packages=setuptools.find_packages(),
    data_files=[("PogoOCR", ["PogoOCR/pattern_lookups.json"])],
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
