# Rocketbookie #

Utilities for my Rocketbook workflow.

## Goal ##

Easy incremental append to multiple existing PDFs, with searchable OCR.

## Setup ##

1. Top level PDFs which are appended to on an ongoing basis.
2. Cloud folders which receive new pages from the Rocketbook app.
3. Use destinations to save PDFs to appropriate cloud folders. Use timestamped
   naming template (default is fine). Turn OCR on, separate file for transcript
   (two files option). Bunding optional.

PDFs and associated folders should have the same name (minus the prefix) and
be in the same folder.

Basic workflow:

1. Write stuff.
2. Mark destinations and scan.
3. Run rocketbookie.

Rocketbookie does the following:

1. Checks cloud folders for new pdf/transcript pairs.
2. Appends the PDFs to the top level PDFs, in alphabetical (timestamp) order,
   using ghostscript:

```
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
  -sOutputFile=out.pdf \
  in1.pdf in2.pdf ...
```

3. Archives the PDFs and transcripts by moving them to the `archive` subfolder.

## Install ##

1. Install `python3`, `pipenv`, `ghostscript`.
2. `cd <dir> && pipenv --python 3 && pipenv install`.

## Usage ##

Run in the virtualenv created above:

```
$ pipenv shell
$ python ./rocketbookie.py --help

Usage: rocketbookie.py [OPTIONS] PATH

  Bundle PDFs at PATH.

  PATH can be a PDF, in which case additional PDFs to append are searched
  for in a directory with the same name sans suffix.

  PATH can be a directory, in which case all PDFs with matching directories
  are processed.

Options:
  --help  Show this message and exit.
```

## Notes ##

Dealing with privacy / encryption?

Option for monthly / yearly bundles?

Tried `tesseract-ocr` (via `pdfsandwich`) and it doesn't deal with handwriting
well. (Maybe version 5 will?) Also it slightly downgrades the scanned images.

Could use Google Vision API (1000 docs/mo is free) if Rocketbook OCR is not
good enough / goes away.

Options for merging PDFs:

https://stackoverflow.com/questions/2507766/merge-convert-multiple-pdf-files-into-one-pdf

* `pdfjoin` (doesn't work for large page sizes)
* `pdfunite` (breaks links, big files)
* `pdftk` (java)
* `sedja-console` (java)
* `qpdf` (breaks links)
* `ghostscript`
* various python libraries based on PyPDF* (sucks)
