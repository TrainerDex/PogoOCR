import setuptools
import re

with open("README.md", "r") as fh:
	long_description = fh.read()

def version():
	with open('PogoOCR/__init__.py') as f:
		   return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

def requirements():
	with open('requirements.txt') as f:
		return f.read().splitlines()

setuptools.setup(
	name="PogoOCR",
	version=version(),
	author="Jay Turner",
	author_email="jay@trainerdex.co.uk",
	description="A Python tool for running OCR on Pokemon Screenshots",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/TrainerDex/PogoOCR",
	packages=setuptools.find_packages(),
	install_requires=requirements(),
	python_requires='>=3.6',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
