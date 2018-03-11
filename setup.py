import re
from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

version = ''
with open('PokeOCR/__init__.py') as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
	raise RuntimeError('version is not set')

setup(
	name='PokeOCR',
	version=version,
	description='A Python tool for running OCR on Pokemon Screenshots',
	long_description=readme(),
	author='JayTurnr/DynamicalSystem',
	author_email='jaynicholasturner@gmail.com',
	url='https://github.com/TrainerDex/PokeOCR',
	license='N/A',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Topic :: Games/Entertainment'
		],
	keywords='pokemon pokemongo trainer',
	packages=['PokeOCR'],
	zip_safe=True,
	install_requires=[
		'opencv-python',
		'pyocr',
		'PIL',
	],
)
