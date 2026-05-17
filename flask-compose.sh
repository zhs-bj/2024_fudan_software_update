echo "Waiting for Neo4j to be ready..."
neo4j_ready=false
for i in $(seq 1 60); do
    python -c "
from py2neo import Graph
try:
    g = Graph('bolt://parthub:7687', auth=('neo4j', 'igem2024'))
    g.run('RETURN 1')
    print('Neo4j is ready')
    exit(0)
except Exception as e:
    exit(1)
" 2>/dev/null
    if [ $? -eq 0 ]; then
        neo4j_ready=true
        break
    fi
    echo "Neo4j not ready yet, waiting... ($i/60)"
    sleep 5
done

if [ "$neo4j_ready" != "true" ]; then
    echo "Neo4j did not become ready in time. Exiting."
    exit 1
fi

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
    PYTHONPATH=/app python parthub/build_semantic_index.py
    echo "Starting Flask server..."
    python app.py --host=0.0.0.0
fi
