# syntax=docker/dockerfile:1
FROM python:3.10.6-slim

# Install gnupg & wget...
RUN apt-get update -y \
    && apt-get install -y gnupg \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

# Trust keys for GC & install GC stable version.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update -y && apt-get install -y google-chrome-stable

# Install pipenv.
RUN pip3 install --no-cache-dir pipenv

# Set WORKDIR (equity).
WORKDIR /usr/src/equity

# Copy files into new WORKDIR.
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY equity ./equity

# Install API dependencies.
RUN pipenv install --system --deploy

# Start the Flask application.
EXPOSE 5001
ENTRYPOINT [ "/usr/src/app/bootstrap.sh" ]
