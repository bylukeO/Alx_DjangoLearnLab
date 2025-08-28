# HTTPS Deployment Configuration Guide

This document provides comprehensive instructions for deploying the Django Library Project with HTTPS support and security enhancements.

## Table of Contents

1. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
2. [Web Server Configuration](#web-server-configuration)
3. [Django Environment Variables](#django-environment-variables)
4. [Security Testing](#security-testing)
5. [Troubleshooting](#troubleshooting)

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Recommended for Production)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal setup
sudo crontab -e
# Add line: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Self-Signed Certificate (Development Only)

```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate certificate signing request
openssl req -new -key private.key -out certificate.csr

# Generate self-signed certificate
openssl x509 -req -days 365 -in certificate.csr -signkey private.key -out certificate.crt
```

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/django-library`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificate configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # SSL Security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Additional Security Headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https:;" always;

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_redirect off;
    }

    # Static files
    location /static/ {
        alias /path/to/django/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/django/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

### Apache Configuration

Create or update your Apache virtual host file:

```apache
<IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName yourdomain.com
        ServerAlias www.yourdomain.com
        
        # SSL Configuration
        SSLEngine on
        SSLCertificateFile /path/to/certificate.crt
        SSLCertificateKeyFile /path/to/private.key
        
        # SSL Security Settings
        SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
        SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
        SSLHonorCipherOrder off
        
        # Security Headers
        Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        Header always set X-Frame-Options DENY
        Header always set X-Content-Type-Options nosniff
        Header always set X-XSS-Protection "1; mode=block"
        Header always set Referrer-Policy "strict-origin-when-cross-origin"
        
        # Django WSGI Configuration
        WSGIDaemonProcess django python-path=/path/to/django/project
        WSGIProcessGroup django
        WSGIScriptAlias / /path/to/django/project/wsgi.py
        
        # Static files
        Alias /static/ /path/to/django/static/
        <Directory /path/to/django/static/>
            Require all granted
        </Directory>
        
        # Media files
        Alias /media/ /path/to/django/media/
        <Directory /path/to/django/media/>
            Require all granted
        </Directory>
    </VirtualHost>
</IfModule>

# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>
```

## Django Environment Variables

Create a `.env` file or set environment variables:

### Production Environment Variables

```bash
# Basic Django Settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=your-production-secret-key-here

# HTTPS Configuration
ENABLE_HTTPS=True
SECURE_SSL_HOST=yourdomain.com

# Database Configuration (example for PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Static/Media Files
STATIC_ROOT=/path/to/static/files
MEDIA_ROOT=/path/to/media/files
```

### Development Environment Variables

```bash
# Basic Django Settings
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# HTTPS Configuration (disabled for development)
ENABLE_HTTPS=False

# Database Configuration (example for SQLite)
DATABASE_URL=sqlite:///db.sqlite3
```

### Environment Variable Setup Script

Create `scripts/setup_environment.sh`:

```bash
#!/bin/bash
# Production environment setup script

# Export production environment variables
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export ENABLE_HTTPS=True
export SECURE_SSL_HOST="yourdomain.com"

# Database configuration
export DATABASE_URL="postgresql://username:password@localhost:5432/library_db"

# Static and media files
export STATIC_ROOT="/var/www/django-library/static"
export MEDIA_ROOT="/var/www/django-library/media"

echo "Environment variables configured for production deployment"
```

## Security Testing

### SSL/TLS Testing Tools

1. **SSL Labs Test**: https://www.ssllabs.com/ssltest/
2. **testssl.sh**: Command-line SSL/TLS tester

```bash
# Install testssl.sh
git clone --depth 1 https://github.com/drwetter/testssl.sh.git
cd testssl.sh

# Test your domain
./testssl.sh yourdomain.com
```

### Security Headers Testing

```bash
# Test security headers
curl -I https://yourdomain.com

# Expected headers:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Content-Security-Policy: default-src 'self'; ...
```

### Django Security Check

```bash
# Run Django's built-in security check
python manage.py check --deploy

# Should show no security warnings for production configuration
```

## Deployment Checklist

### Pre-deployment

- [ ] SSL/TLS certificate obtained and installed
- [ ] Web server configured with HTTPS support
- [ ] Environment variables set correctly
- [ ] Django settings reviewed and secured
- [ ] Database backup created
- [ ] Static files collected (`python manage.py collectstatic`)

### Post-deployment

- [ ] HTTPS redirect working (HTTP → HTTPS)
- [ ] SSL/TLS configuration tested (SSL Labs A+ rating)
- [ ] Security headers present and correct
- [ ] Django security check passes
- [ ] Application functionality tested over HTTPS
- [ ] HSTS preload list submission (optional)

### Monitoring

- [ ] SSL certificate expiration monitoring
- [ ] Security header monitoring
- [ ] Application error monitoring
- [ ] Performance monitoring

## Troubleshooting

### Common Issues

#### 1. SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in certificate.crt -text -noout

# Test certificate chain
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

#### 2. HTTPS Redirect Loop

- Check that `SECURE_PROXY_SSL_HEADER` is correctly configured
- Ensure web server is passing the correct headers
- Verify `SECURE_SSL_REDIRECT` setting

#### 3. Mixed Content Warnings

- Ensure all resources (CSS, JS, images) use HTTPS URLs
- Check Content Security Policy settings
- Use protocol-relative URLs or HTTPS-only URLs

#### 4. HSTS Issues

- Clear browser HSTS cache: `chrome://net-internals/#hsts`
- Verify HSTS header syntax
- Check HSTS preload list inclusion

### Debug Commands

```bash
# Test Django configuration
python manage.py check --deploy

# Test SSL configuration
curl -vI https://yourdomain.com

# Check environment variables
python manage.py shell -c "from django.conf import settings; print('HTTPS enabled:', settings.ENABLE_HTTPS)"

# Test security middleware
python manage.py shell -c "
from django.test import RequestFactory
from LibraryProject.security_middleware import SecurityHeadersMiddleware
from django.http import HttpResponse
rf = RequestFactory()
request = rf.get('/')
middleware = SecurityHeadersMiddleware()
response = middleware.process_response(request, HttpResponse())
for header, value in response.items():
    print(f'{header}: {value}')
"
```

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

## Support

For deployment support and troubleshooting:

1. Check Django logs: `/var/log/django/error.log`
2. Check web server logs: `/var/log/nginx/error.log` or `/var/log/apache2/error.log`
3. Run security diagnostics: `python manage.py check --deploy`
4. Test SSL configuration: https://www.ssllabs.com/ssltest/