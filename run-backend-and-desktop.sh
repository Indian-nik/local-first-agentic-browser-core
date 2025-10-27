#!/bin/bash
echo "Starting Docker backend..."
docker-compose up --build -d

echo "Launching Electron desktop app..."
cd src/renderer
npm install
npm run electron:dev
