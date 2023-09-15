#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 DIRECTORY"
  exit 1
fi

dir="$1"
reference="path_to_NC_004454_reference_genome"

for fastq1 in "$dir"/*_1.fastq; do
  base_fastq1=$(basename "$fastq1")
  fastq2="${fastq1%_1.fastq}_2.fastq"
  base_fastq2=$(basename "$fastq2")
  filtered_fastq1="${dir}/filtered_$base_fastq1.fq"
  filtered_fastq2="${dir}/filtered_$base_fastq2.fq"
  output="${dir}/${base_fastq1%_1.fastq}.asm"
  sam_file="${dir}/${base_fastq1%_1.fastq}.sam"

  # Create a SAM file using bwa-mem2 for paired-end reads
  bwa-mem2 mem -t 16 "$reference" "$fastq1" "$fastq2" > "$sam_file"

  # Convert the SAM file to a BAM file, filter it, and convert it back to a FASTQ file
  samtools view -@ 16 -h -b -S "$sam_file" | samtools view -@ 16 -b -F 4 - | samtools sort -@ 16 -n - | samtools fastq -@ 16 -n -1 "$filtered_fastq1" -2 "$filtered_fastq2" -

  # Use repair.sh to ensure that both forward and reverse reads are present
  repair.sh in="$filtered_fastq1" in2="$filtered_fastq2" out="$filtered_fastq1.repaired.fastq" out2="$filtered_fastq2.repaired.fastq"

  # Run SPAdes on the cleaned and filtered FASTQ files with the --isolate option
  spades.py --isolate -1 "$filtered_fastq1.repaired.fastq" -2 "$filtered_fastq2.repaired.fastq" -t 16 -o "$output"

  # Remove the intermediary files
  rm "$sam_file" "$filtered_fastq1" "$filtered_fastq2" "$filtered_fastq1.repaired.fastq" "$filtered_fastq2.repaired.fastq"
done
