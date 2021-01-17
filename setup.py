import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="hatena2md",
	version="0.1.0",
	author="Florian Eder",
	author_email="others.meder@gmail.com",
	description="Python application to convert Hatena Notation (はてな記法) to Markdown",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/schroeding/hatena2md",
	packages=setuptools.find_packages(),
	classifiers=[
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 3",
		"License :: Public Domain",
		"Operating System :: OS Independent",
		"Topic :: Text Processing :: Markup"
	],
	entry_points = {
		'console_scripts': ['hatena2md=hatena2md.__main__:main'],
	},
	install_requires = [
	],
	python_requires='>=3.6',
)