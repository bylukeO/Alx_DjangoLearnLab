# Django Library Project Security Documentation

This document outlines the security measures implemented in the Django Library Project to protect against common web vulnerabilities and security threats.

## Security Measures Implemented

### 1. Cross-Site Request Forgery (CSRF) Protection

**Implementation:**
- CSRF middleware is enabled in `settings.py`
- All forms include `{% csrf_token %}` template tag
- CSRF cookies are configured with security settings

**Settings:**
```python
CSRF_COOKIE_HTTPONLY = True  # Prevents JavaScript access to CSRF cookie
CSRF_COOKIE_SAMESITE = 'Strict'  # Strict SameSite policy for CSRF cookies
# CSRF_COOKIE_SECURE = True  # Enable in production with HTTPS
```

**Protection Against:** CSRF attacks where malicious websites trick users into performing unwanted actions.

### 2. Cross-Site Scripting (XSS) Protection

**Implementation:**
- Input validation and sanitization using `bleach` library in form validation
- Template auto-escaping enabled by default in Django
- Custom form validation methods that strip HTML tags and validate input patterns
- Browser XSS filter enabled via security headers

**Settings:**
```python
SECURE_BROWSER_XSS_FILTER = True  # Enables XSS filtering in browsers
```

**Form Validation Example:**
```python
def clean_title(self):
    title = self.cleaned_data.get('title')
    if title:
        title = bleach.clean(title.strip(), tags=[], strip=True)
        if re.search(r'<script|javascript:|data:', title, re.IGNORECASE):
            raise ValidationError("Invalid characters in title.")
    return title
```

**Protection Against:** XSS attacks through malicious script injection in user inputs.

### 3. SQL Injection Prevention

**Implementation:**
- Exclusive use of Django ORM for database queries
- No raw SQL queries or string concatenation
- Parameterized queries through ORM methods
- Input validation before database operations

**Examples:**
```python
# Safe ORM usage
books = Book.objects.all()  # ORM query prevents SQL injection
book = get_object_or_404(Book, pk=pk)  # Safe parameter binding
```

**Protection Against:** SQL injection attacks through malicious database queries.

### 4. Content Security Policy (CSP)

**Implementation:**
- Custom middleware `SecurityHeadersMiddleware` implements CSP headers
- Restrictive CSP policy allowing only same-origin resources
- Inline scripts and styles allowed with 'unsafe-inline' (can be tightened further)

**Settings:**
```python
CSP_DEFAULT_SRC = "'self'"
CSP_SCRIPT_SRC = "'self' 'unsafe-inline'"
CSP_STYLE_SRC = "'self' 'unsafe-inline'"
CSP_IMG_SRC = "'self' data: https:"
CSP_FONT_SRC = "'self' https:"
CSP_CONNECT_SRC = "'self'"
CSP_FRAME_ANCESTORS = "'none'"
```

**Protection Against:** XSS attacks, clickjacking, and unauthorized resource loading.

### 5. Session Security

**Implementation:**
- Secure session cookie configuration
- Session timeout configuration
- HttpOnly cookies to prevent JavaScript access

**Settings:**
```python
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Strict'  # Strict SameSite policy
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Sessions expire when browser closes
SESSION_COOKIE_AGE = 3600  # Session timeout in seconds (1 hour)
# SESSION_COOKIE_SECURE = True  # Enable in production with HTTPS
```

**Protection Against:** Session hijacking and fixation attacks.

### 6. Clickjacking Protection

**Implementation:**
- X-Frame-Options header set to DENY
- Frame-ancestors CSP directive set to 'none'

**Settings:**
```python
X_FRAME_OPTIONS = 'DENY'  # Prevents page from being displayed in frame/iframe
```

**Protection Against:** Clickjacking attacks where pages are embedded in malicious iframes.

### 7. MIME Type Sniffing Protection

**Implementation:**
- X-Content-Type-Options header set to 'nosniff'

**Settings:**
```python
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents MIME type sniffing
```

**Protection Against:** MIME type confusion attacks.

### 8. Referrer Policy

**Implementation:**
- Strict referrer policy to control information leakage

**Settings:**
```python
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

**Protection Against:** Information leakage through HTTP referrer headers.

### 9. Permission-Based Access Control

**Implementation:**
- Django's permission system for resource access control
- Custom permissions for book operations (can_view, can_create, can_edit, can_delete)
- Login required decorators on sensitive views
- Role-based access control for different user types

**Examples:**
```python
@permission_required('bookshelf.can_create', raise_exception=True)
@login_required
def book_create(request):
    # View implementation with security checks
```

**Protection Against:** Unauthorized access to sensitive resources and operations.

## Production Security Checklist

When deploying to production, enable these additional security settings:

### HTTPS Configuration
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### Environment Variables
- Move `SECRET_KEY` to environment variables
- Use strong, randomly generated secret keys
- Configure `ALLOWED_HOSTS` appropriately for your domain

### Database Security
- Use strong database passwords
- Restrict database access to application servers only
- Enable database connection encryption if available

## Security Testing

### Manual Testing Performed
- Form input validation with malicious payloads
- CSRF token verification on form submissions
- Permission checks on restricted views
- Session timeout functionality
- XSS prevention through input sanitization

### Recommended Additional Testing
- Automated security scanning with tools like OWASP ZAP
- Penetration testing for production deployment
- Regular dependency vulnerability scanning
- Code security reviews

## Dependencies

The following security-related dependencies are required:

```
Django>=5.2.3
bleach>=6.0.0  # For input sanitization
pillow>=10.0.0  # For secure image handling
```

## Security Headers Implemented

The following security headers are automatically added to all responses:

- `Content-Security-Policy`: Restricts resource loading
- `X-Content-Type-Options: nosniff`: Prevents MIME sniffing
- `X-Frame-Options: DENY`: Prevents clickjacking
- `X-XSS-Protection: 1; mode=block`: Browser XSS protection
- `Referrer-Policy`: Controls referrer information

## Monitoring and Maintenance

- Regularly update Django and all dependencies
- Monitor security advisories for Django and installed packages
- Review and update security configurations as needed
- Log and monitor security-related events
- Regular security audits and assessments

## Contact

For security-related questions or concerns, please refer to Django's security documentation and best practices.