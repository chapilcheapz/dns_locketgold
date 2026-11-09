FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy certs và source
COPY certs/ ./certs/
COPY main.py .

# HTTP profile/DOH port
ENV PORT=8080
# HTTPS MITM port (giả revenuecat)
ENV PORT_MITM=8443

EXPOSE 8080 8443

CMD ["python", "main.py"]
