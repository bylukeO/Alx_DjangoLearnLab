# Library Project

A Django-based library management system for organizing and managing books, authors, and library operations.

## 🚀 Features

- **Book Management**: Add, edit, and delete books
- **Author Management**: Manage author information
- **Library Operations**: Track book availability and borrowing
- **Admin Interface**: Django admin panel for easy management
- **SQLite Database**: Lightweight database for development

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LibraryProject
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

## 🏃‍♂️ Running the Project

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
LibraryProject/
├── LibraryProject/          # Main project directory
│   ├── __init__.py
│   ├── asgi.py             # ASGI configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
└── README.md               # This file
```

## 🔧 Configuration

The project uses Django's default SQLite database for development. Key configuration files:

- `settings.py`: Main Django settings
- `urls.py`: URL routing configuration
- `db.sqlite3`: SQLite database file

## 📚 Usage

### Admin Panel
1. Navigate to http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials
3. Manage books, authors, and other library data

### Development
- The project is set up for development with `DEBUG = True`
- Static files are served from the `static/` directory
- Database is SQLite for easy development

## 🚧 Development

### Adding New Apps
```bash
python manage.py startapp your_app_name
```

### Creating Models
1. Define models in your app's `models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`

### Running Tests
```bash
python manage.py test
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

If you encounter any issues or have questions:

1. Check the Django documentation: https://docs.djangoproject.com/
2. Search existing issues
3. Create a new issue with detailed information

## 🔄 Version History

- **v1.0.0**: Initial project setup with Django framework

---

**Happy coding! 📖✨**
