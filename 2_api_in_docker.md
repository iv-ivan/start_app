python3 -m fastapi run app/main.py --workers 4

vim Dockerfile
```
FROM python:3.13
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["python", "-m", "fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
# use exec, not shell, form to proper handle signals
# --proxy-headers for load balancer
```
docker build -t myimage .

docker run -d --name mycontainer -p 80:80 myimage

http://127.0.0.1/items/5?q=somequery

docker stop mycontainer

docker rm mycontainer
