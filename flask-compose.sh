count=0
max_attempts=10

while [ $count -lt $max_attempts ]; do
    cd /app/
    if [ -f "./blast+/bin/blastn" ]; then
        echo "BLAST already installed. Skipping download."
    else
        echo "Downloading BLAST package..."
        wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.16.0/ncbi-blast-2.16.0+-x64-linux.tar.gz -O blast.tar.gz -q
        tar -zxvf blast.tar.gz
        mv ncbi-blast-2.16.0+ blast+
        rm -f blast.tar.gz
    fi
    mkdir uploads
    mkdir similarity/data
    python parthub/upload_collections.py
    ret_value=$?
    if [ $ret_value -eq 0 ]; then
        echo "Successfully uploaded collections"
        break
    else
        echo "Python script failed with return value $ret_value. Retrying..."
        count=$((count + 1))
    fi
done

if [ $count -eq $max_attempts ]; then
    echo "Python script failed after $max_attempts attempts."
else
    python parthub/init_fulltext_index.py create
    ./blast+/bin/makeblastdb -in similarity/data/seqdump.fasta -dbtype nucl
    echo "Building semantic search index..."
    python parthub/build_semantic_index.py
    echo "Starting Flask server..."
    python app.py --host=0.0.0.0
fi
