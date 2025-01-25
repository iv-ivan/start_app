FROM python:3.13
WORKDIR /code/app
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["python", "-m", "fastapi", "run", "main.py", "--port", "80", "--proxy-headers"]
# We use exec, not shell form, of CMD to proper handle signals
# "--proxy-headers" is included for load balancer to work properly (next steps)
# We can add "--workers", "4" if we want to run multiple processes
