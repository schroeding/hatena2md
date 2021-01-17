# Hatena2MD

A small python application to convert text from Hatena Notation (はてな記法) to Markdown.
Hatena Notation has some nifty features (like automatic table of content generation, automatic link title fetching) that are implemented into this converter.

Take a look at this [sample file in Hatena Notation](https://github.com/schroeding/hatena2md/blob/master/sample_hatena.txt) and its representation in [markdown](https://github.com/schroeding/hatena2md/blob/master/sample_markdown.md)


## Installation

```bash
python -m pip install hatena2md
```

## Usage

```bash
python -m hatena2md -i <inputfile> -o <outputfile>
```

## License

[The Unlicense](https://choosealicense.com/licenses/unlicense/)