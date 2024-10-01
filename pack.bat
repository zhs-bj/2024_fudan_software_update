@echo on
cd webUI
npm run build
cd ..
python pack.py
docker compose up -d