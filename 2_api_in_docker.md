# Docker container with our API server
You need Docker installed locally. On macOS you can use Docker Desktop

1) Check new `Dockerfile` file. It defines our image.
2) Then, build docker image: `docker build -t myimage . --platform linux/amd64`
   - I use `--platform` explicitly, because I have macOS but in AWS we will have Linux 

Now let's check this image works:
```shell
docker run -d --name mycontainer -p 80:80 myimage
curl -v http://127.0.0.1/items/5?q=somequery
docker stop mycontainer
docker rm mycontainer
```






