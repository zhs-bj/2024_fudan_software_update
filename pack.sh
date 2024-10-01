cd webUI
npm run build
if [ $? -ne 0 ]; then
    echo "[ERROR] npm build failed"
else
    cd ../
    python pack.py
    docker compose up -d
fi