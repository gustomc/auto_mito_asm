# auto_mito_asm

This script provides an automated pipeline to process paired-end FASTQ files, align them to a reference genome, filter the aligned reads, and finally perform genome assembly.

## Prerequisites

- bwa-mem2
- samtools
- repair.sh (From the BBTools suite)
- spades.py

## Usage

`./script_name.sh DIRECTORY`

**DIRECTORY**: The directory containing the paired-end FASTQ files (*_1.fastq and *_2.fastq).

**Note**: This script expects paired-end FASTQ files in the format 'filename_1.fastq' and 'filename_2.fastq'.

## How it works

1.  Takes a directory of paired-end FASTQ files as input.
2.  Aligns the FASTQ files to the reference genome using `bwa-mem2` creating a SAM file.
3.  Converts the SAM file to a BAM file, filter, and convert back to FASTQ using `samtools`.
4.  Ensures both forward and reverse reads are present using `repair.sh`.
5.  Runs assembly using `spades.py` with the --isolate option on the cleaned and filtered FASTQ files.
6.  Removes intermediary files to save disk space.

## Reference Genome

Ensure that the `reference` variable in the script points to the path of your desired reference genome.

## Feedback

For any issues, bugs, or feature requests, please raise an issue in the repository or contact the script maintainer.

## Credits and Disclaimer

This README was co-authored by Gus and John Webster, with assistance from ChatGPT by OpenAI. Any content or advice provided by ChatGPT should be double-checked for accuracy and appropriateness for specific use cases.
