FROM oraclelinux:9

ENV PYTHONUNBUFFERED=1
ENV VulcanDEV=1

# System deps
#RUN dnf install -y epel-release && \
RUN dnf install -y \
        python3 \
        python3-pip \
        unixODBC \
        curl \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# Microsoft ODBC Driver
RUN curl -o /etc/yum.repos.d/msprod.repo \
    https://packages.microsoft.com/config/rhel/9/prod.repo && \
    ACCEPT_EULA=Y dnf install -y msodbcsql18


# App working directory
WORKDIR /VulcanActivityTracker


# Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy application code (THIS WAS MISSING)
COPY . .


EXPOSE 8000

#CMD ["python3", "app.py"]

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
