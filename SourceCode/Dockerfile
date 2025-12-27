FROM oraclelinux:9

ENV PYTHONUNBUFFERED=1
ENV VulcanDEV=1

# System deps
RUN dnf install -y epel-release && \
    dnf install -y \
        python3 \
        python3-pip \
        ncurses \
        iputils \
        traceroute \
        iproute \
        git \
        unixODBC && \
    dnf clean all

# Microsoft ODBC Driver
RUN curl -o /etc/yum.repos.d/msprod.repo \
    https://packages.microsoft.com/config/rhel/9/prod.repo && \
    ACCEPT_EULA=Y dnf install -y msodbcsql17

# Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# App working directory
WORKDIR /VulcanActivityTracker

EXPOSE 6455

CMD ["python3", "app.py"]
