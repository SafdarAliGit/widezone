from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in widezone/__init__.py
from widezone import __version__ as version

setup(
	name="widezone",
	version=version,
	description="ERP Customization",
	author="Safdar",
	author_email="safdar211@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
