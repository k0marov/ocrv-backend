 docker run -v $(pwd)/dev:/app/var \
    -e OCRV_RECORDER_SECRET_KEY=1234 \
    -e OCRV_RECORDER_TEXTS_PATH=/app/var/texts.csv \
    -e OCRV_RECORDER_LOG_PATH=/app/var/logs.log \
    -e OCRV_RECORDER_RECORDINGS_DIR=/app/var/recordings/ \
    -e OCRV_RECORDER_DB_PATH=/app/var/db.sqlite3 \
    -e OCRV_RECORDER_RECORDINGS_URL=TEST \
    -p 8000:8000 ocrv-backend