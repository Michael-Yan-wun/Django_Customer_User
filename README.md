# Django Custom User Model

這個專案示範如何在 Django 中建立自訂的使用者模型（Custom User Model），取代 Django 預設的 `auth_user` 表。
This project demonstrates how to replace Django's default `auth_user` table with a custom user model tailored to specific requirements.

## 📋 專案簡介 / Project Overview

Django 預設使用內建的 `User` 模型，但在許多情況下，我們需要自訂使用者模型以符合專案需求。這個專案展示了如何：
While Django ships with a built-in `User` model, real-world projects often require additional fields or behaviors. This repository walks through how to:

- 建立自訂的使用者模型（`NewUser`） / Build a custom user model (`NewUser`)
- 使用 `AbstractBaseUser` 和 `PermissionsMixin` 作為基礎 / Extend `AbstractBaseUser` and `PermissionsMixin`
- 建立自訂的 User Manager（`CustomerAccountManager`） / Implement a tailored user manager (`CustomerAccountManager`)
- 在 settings.py 中設定 `AUTH_USER_MODEL` / Wire the model via `AUTH_USER_MODEL` in `settings.py`

## 🚀 功能特色 / Key Features

- ✅ 使用 Email 作為登入帳號（而非預設的 username） / Email-first authentication instead of usernames
- ✅ 自訂使用者欄位：`email`、`user_name`、`first_name`、`about` / Custom profile fields for richer data
- ✅ 支援建立一般使用者與超級使用者 / Helper APIs for regular and superuser creation
- ✅ 完整的權限管理（PermissionsMixin） / Full permission management through `PermissionsMixin`

## 📁 專案結構 / Project Structure

```
Django_Customer_User/
├── CustomerAuth/
│   ├── core/
│   │   ├── settings.py      # 設定 AUTH_USER_MODEL = 'users.NewUser'
│   │   └── ...
│   └── users/
│       ├── models.py         # 自訂使用者模型 NewUser
│       └── ...
└── README.md
```

## 🔧 核心實作

### 1. 自訂使用者模型（models.py） / Custom user model

```python
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']
```

### 2. 自訂 User Manager / Custom user manager

```python
class CustomerAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        # 建立一般使用者 / Create a regular user
        ...
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        # 建立超級使用者 / Create a superuser
        ...
```

### 3. 設定檔修改（settings.py） / Settings hook

```python
AUTH_USER_MODEL = 'users.NewUser'
```

## 📦 安裝與使用 / Installation & Usage

### 前置需求 / Prerequisites

- Python 3.x
- Django 3.2.5+

### 安裝步驟 / Setup Steps

1. Clone 專案 / Clone the repo：
```bash
git clone https://github.com/Michael-Yan-wun/Django_Customer_User.git
cd Django_Customer_User/CustomerAuth
```

2. 安裝依賴 / Install dependencies：
```bash
pip install django
```

3. 執行遷移 / Run migrations：
```bash
python manage.py makemigrations
python manage.py migrate
```

4. 建立超級使用者 / Create a superuser：
```bash
python manage.py createsuperuser
```

## ⚠️ 重要注意事項 / Important Notes

1. **在建立第一個 migration 之前設定**：`AUTH_USER_MODEL` 必須在建立第一個 migration 之前就設定好，否則後續修改會很困難。  
   **Set this before the first migration**: `AUTH_USER_MODEL` must be configured prior to generating initial migrations; changing it later is painful.

2. **不要直接修改預設 User 模型**：應該建立新的自訂模型，而不是修改 Django 內建的 User 模型。  
   **Avoid editing Django's default User model**; always define your own implementation.

3. **外鍵引用**：在專案中引用使用者時，應該使用 `settings.AUTH_USER_MODEL` 而不是直接引用模型：  
   **Foreign keys**: always refer to `settings.AUTH_USER_MODEL` to keep relations decoupled from concrete classes.
   ```python
   from django.conf import settings
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   ```

## 📝 使用範例 / Usage Examples

### 建立使用者 / Create users

```python
from users.models import NewUser

# 建立一般使用者 / Create a regular user
user = NewUser.objects.create_user(
    email='user@example.com',
    user_name='johndoe',
    first_name='John',
    password='securepassword123'
)

# 建立超級使用者 / Create a superuser
admin = NewUser.objects.create_superuser(
    email='admin@example.com',
    user_name='admin',
    first_name='Admin',
    password='adminpassword123'
)
```

### 登入驗證 / Authenticate

```python
from django.contrib.auth import authenticate

user = authenticate(email='user@example.com', password='securepassword123')
if user:
    print(f"登入成功：{user.user_name}")
    print(f"Login success: {user.user_name}")
```

## 🔗 相關資源 / Resources

- [Django 官方文件 - Custom User Model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
- [Django 官方文件 - AbstractBaseUser](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser)

## 📄 授權 / License

詳見 [LICENSE](LICENSE) 檔案。  
Refer to the [LICENSE](LICENSE) file for full terms.

## 👤 作者 / Author

Michael Lin

---

**注意**：這個專案僅供學習參考，在生產環境使用前請確保已充分測試並遵循 Django 最佳實踐。  
**Note**: This repository is for educational purposes; follow Django best practices and perform thorough testing before deploying to production.
