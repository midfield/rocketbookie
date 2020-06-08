#!/usr/bin/env python3

# Copyright 2020 Benjamin Lee. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import subprocess

import click

TRANSCRIPT_EXT = ".pdf Transcription.gdoc"
GS_CMD = [
    "gs",
    "-dBATCH",
    "-dNOPAUSE",
    "-dQUIET",
    "-sDEVICE=pdfwrite",
    "-dPDFSETTINGS=/prepress",
]


@click.command()
@click.argument("path", type=click.Path(exists=True))
def cli(path):
    """
    Bundle PDFs at PATH.

    PATH can be a PDF, in which case additional PDFs to append are searched for
    in a directory with the same name sans suffix.

    PATH can be a directory, in which case all PDFs with matching directories
    are processed.
    """
    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_folder(path)
    else:
        raise ValueError(f"PATH '{path}' must be a file or a directory")


def process_file(path):
    process_bundle(*validate_bundle(path))


def validate_bundle(path):
    path = os.path.abspath(path)
    if not path.lower().endswith(".pdf"):
        raise ValueError("PATH '{path}' must be a PDF")
    if not os.path.isfile(path):
        raise ValueError("PATH '{path}' not a file")
    folder = path[:-4]
    if not os.path.isdir(folder):
        raise ValueError("PATH is '{path}' but '{folder}' is not a directory")
    archive = os.path.join(folder, "archive")
    if os.path.exists(archive):
        if not os.path.isdir(archive):
            raise IOError("Archive '{archive}' is not a directory")
    else:
        os.makedirs(archive)
    return (path, folder, archive)


def process_bundle(toppdf, folder, archive):
    assert toppdf.endswith(".pdf")
    folder_base = os.path.basename(folder)
    print(f"Processing '{folder_base}'...")
    files = [os.path.abspath(entry.path) for entry in os.scandir(folder)
             if entry.is_file()]
    pdfs = set(f for f in files if f.endswith(".pdf"))
    transcripts = set(f[:-len(TRANSCRIPT_EXT)] + ".pdf"
                      for f in files if f.endswith(TRANSCRIPT_EXT))
    with_transcripts = sorted(pdfs & transcripts)
    missing_transcripts = sorted(pdfs - transcripts)
    if len(missing_transcripts) > 0:
        lst = "\n".join(os.path.basename(f) for f in missing_transcripts)
        print(f"Found {len(missing_transcripts)} PDFs without transcripts in "
              f"'{folder_base}':\n{lst}")
    if len(with_transcripts) == 0:
        print(f"No PDFs with transcripts found in '{folder_base}'")
        return
    lst = "\n".join(os.path.basename(f) for f in with_transcripts)
    print(f"Found {len(pdfs)} PDFS in '{folder_base}':\n{lst}\n")
    print("Bundling...")
    tmp = toppdf[:-4] + ".tmp.pdf"
    subprocess.run(
        GS_CMD + [f"-sOutputFile={tmp}"] + [toppdf] + with_transcripts,
        check=True)
    os.rename(toppdf, toppdf + ".bak")
    os.rename(tmp, toppdf)
    print("Archiving...")
    for f in pdfs:
        archive_file(f, archive)
        archive_file(f[:-4] + TRANSCRIPT_EXT, archive)


def archive_file(path, archive):
    fname = os.path.basename(path)
    dst = os.path.join(archive, fname)
    if os.path.exists(dst):
        raise IOError(f"'{dst}' already exists!")
    os.rename(path, dst)


def process_folder(path):
    if not os.path.isdir(path):
        raise ValueError(f"PATH '{path}' is not a directory")
    print("Processing all PDFs in '%s'" % (path,))
    for f in os.listdir(path):
        if f.endswith(".pdf"):
            try:
                toppdf, folder, archive = validate_bundle(
                    os.path.join(path, f))
            except:
                print(f"Error processing '{f}', skipping")
                continue
            process_bundle(toppdf, folder, archive)


if __name__ == "__main__":
    cli()
