# Device

Docker image that allows quick integration of media devices with [dojot](https://www.dojot.com.br).

## Building

```shell
docker build -t fberanizo/device:latest -f Dockerfile .
```

## Camera
docker run --rm -p 1883:1883 --device=/dev/video0:/dev/video0 -e "HOST=[hostname]" -e "TENANT=[tenant]" -e "DEVICE=[device]" -e "WIDTH=[width]" -e "HEIGHT=[height]" -e "FPS=[fps]" fberanizo/device:latest python image.py

## Microphone
docker run --rm -p 1883:1883 --device=/dev/snd:/dev/snd -e "HOST=[hostname]" -e "TENANT=[tenant]" -e "DEVICE=[device]" -e "RATE=[rate]" -e "CHANNELS=[channels]" fberanizo/device:latest python microphone.py

## Speaker
docker run --rm -p 1883:1883 --device=/dev/snd:/dev/snd -e "HOST=[hostname]" -e "TENANT=[tenant]" -e "DEVICE=[device]" -e "RATE=[rate]" -e "CHANNELS=[channels]" fberanizo/device:latest python speaker.py
