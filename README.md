# Rocketbookie #

Utilities for my Rocketbook workflow.

Goal:

Easy incremental append to multiple existing PDFs, with searchable OCR.

Setup:

1. Top level PDFs which are appended to on an ongoing basis.
2. Cloud folders which receive new pages from the Rocketbook app.

PDFs and associated folders should have the same name (minus the prefix) and
be in the same folder.

Basic workflow:

1. Write stuff in Rocketbook.
2. Use destinations to save (non-OCR'd) PDFs to appropriate cloud folders,
   using standard naming template (RB-timestamp.pdf). Bunding optional.
3. Run rocketbookie.

Rocketbookie does the following:

1. Runs tesseract OCR on the new bundles.
2. Appends the bundles to the top level PDFs, in alphabetical (timestamp)
   order.
3. Archives the bundles by moving them to the "archive" subfolder.

Install:

1. Install `tesseract-ocr` and `libtesseract-dev`.
2. Install `pipenv`.
3. `pipenv install`.
