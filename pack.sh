cd webUI
npm run build
cd ../
python pack.py
git add .
docker compose up -d