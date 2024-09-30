count=0
max_attempts=10

while [ $count -lt $max_attempts ]; do
    cd /app/
    BLASTPACK="blast.tar.gz"
    if [ -f "$BLASTPACK" ]; then
        echo "BLAST package already exists. Skipping download."
    else
        echo "Downloading BLAST package..."
        wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz -O $BLASTPACK -q
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
    tar -zxvf blast.tar.gz
    mv ncbi-blast-2.16.0+ blast+
    ./blast+/bin/makeblastdb -in similarity/data/seqdump.fasta -dbtype nucl
    python app.py --host=0.0.0.0
fi