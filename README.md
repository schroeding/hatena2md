# Hatena2MD

A small python application to convert text from Hatena Notation (はてな記法) to Markdown.
Hatena Notation has some nifty features (like automatic table of content generation, automatic link title fetching) that are implemented into this converter.

Take a look at this [sample file in Hatena Notation](./sample_hatena.txt) and its representation in [markdown](./sample_markdown.md)

## Usage

```bash
python -m hatena2md -i <inputfile> -o <outputfile>
```

## License

[The Unlicense](./LICENSE)