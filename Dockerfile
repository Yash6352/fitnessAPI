# # For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8

# COPY . /app

# # # Keeps Python from generating .pyc files in the container
# # ENV PYTHONDONTWRITEBYTECODE=1

# # Turns off buffering for easier container logging
# # ENV PYTHONUNBUFFERED=1

# # Install pip requirements
# COPY requirements.txt .


# WORKDIR /app
# RUN python -m pip install -r requirements.txt


# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# # RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# # USER appuser
# EXPOSE 8000
# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# # CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "MY_FITI\Project\Server\app:app"]
# # CMD ["uvicorn", "MY_FITI\Project\Server\app:app", "--host", "0.0.0.0","--port", "8000", "--reload"]
# CMD ["MY_FITI\Project\main.py"]


FROM python:3.8

WORKDIR /Project

ADD . .
RUN pip install -r requirements.txt

EXPOSE 8000

# COPY ./app /app

CMD ["python3", "Project/main.py"]