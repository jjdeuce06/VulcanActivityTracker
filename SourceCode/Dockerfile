# FROM oraclelinux:9

# ENV PYTHONUNBUFFERED=1
# ENV VulcanDEV=1

# # System deps
# #RUN dnf install -y epel-release && \
# RUN dnf install -y \
#         python3 \
#         python3-pip \
#         unixODBC \
#         curl \
#     && dnf clean all \
#     && rm -rf /var/cache/dnf

# # Microsoft ODBC Driver
# RUN curl -o /etc/yum.repos.d/msprod.repo \
#     https://packages.microsoft.com/config/rhel/9/prod.repo && \
#     ACCEPT_EULA=Y dnf install -y msodbcsql18


# # App working directory
# WORKDIR /VulcanActivityTracker


# # Python dependencies
# COPY requirements.txt /tmp/requirements.txt
# RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# # Copy application code (THIS WAS MISSING)
# COPY . .


# EXPOSE 8000

# #CMD ["python3", "app.py"]

# # Run with gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV VulcanDEV=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    unixodbc \
    unixodbc-dev \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set working directory
WORKDIR /VulcanActivityTracker

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]