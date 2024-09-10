# wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz # TO BE MODIFIED
python parthub/upload_collections.py

if [ $? -ne 0 ]; then
    echo "Failed to upload collections. Retrying..."
else
    echo "Successfully uploaded collections"
    tar -zxvf ncbi-blast-2.16.0+-x64-linux.tar.gz
    mv ncbi-blast-2.16.0+ blast+
    ./blast+/bin/makeblastdb -in similarity/data/seqdump.fasta -dbtype nucl
    python app.py --host=0.0.0.0
fi

# blastn -query /home/chc/fudan2024/similarity/data/temp_query.fasta \
#  -db /home/chc/fudan2024/similarity/data/seqdump.fasta \
#  -out /home/chc/fudan2024/similarity/data/query_ans.txt -evalue 1e-5 -outfmt 6