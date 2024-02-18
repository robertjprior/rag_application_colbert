#!/bin/bash
# Step 5: Create docker containers
docker compose up -d --build

# Step 6: Wait for containers to start and display URLs
echo "Waiting for containers to start..."
sleep 500 # You can adjust this sleep duration as needed
echo "Streamlit app is running at http://localhost:8080/"
echo "FastAPI documentation is available at http://localhost:8082/docs"
echo "Weaviate documentation is available at http://localhost:8083/v1"
