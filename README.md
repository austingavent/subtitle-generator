# subtitle-generator
Generates English Subtitles


### Build

```bash
docker build -t whisper-nvidia:latest
```


### Run
```bash
DATA_DIR=/path/to/data
docker run -v $DATA_DIR:/app/data whisper-nvidia
```

After running, run `docker ps -a` to fetch container ID, then run `docker log <container id>` to view logs. After running, the subtitles should be in the `$DATA_DIR/subtitles`. Or view logs in Docker desktop.
