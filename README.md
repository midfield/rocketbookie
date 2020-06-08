# Rocketbookie #

Utilities for my Rocketbook workflow.

## Goal ##

Easy incremental append to multiple existing PDFs, with searchable OCR.

## Setup ##

1. Top level PDFs which are appended to on an ongoing basis.
2. Cloud folders which receive new pages from the Rocketbook app.

PDFs and associated folders should have the same name (minus the prefix) and
be in the same folder.

Basic workflow:

1. Write stuff in Rocketbook.
2. Use destinations to save PDFs to appropriate cloud folders. Use standard
   naming template (RB-timestamp.pdf). Turn OCR on, in two files. Bunding
   optional.
3. Run rocketbookie.

Rocketbookie does the following:

1. Checks folders for new pdf/transcript pairs.
2. Appends the PDFs to the top level PDFs, in alphabetical (timestamp) order,
   using

```
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
  -sOutputFile=out.pdf \
  in1.pdf in2.pdf ...
```

3. Archives the PDFs and transcripts by moving them to the "archive" subfolder.

## Install ##

1. Install `ghostscript`.
2. Install `pipenv`.
3. `pipenv install`.

## Notes ##

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

