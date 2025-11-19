# Django Custom User Model

這個專案示範如何在 Django 中建立自訂的使用者模型（Custom User Model），取代 Django 預設的 `auth_user` 表。

## 📋 專案簡介

Django 預設使用內建的 `User` 模型，但在許多情況下，我們需要自訂使用者模型以符合專案需求。這個專案展示了如何：

- 建立自訂的使用者模型（`NewUser`）
- 使用 `AbstractBaseUser` 和 `PermissionsMixin` 作為基礎
- 建立自訂的 User Manager（`CustomerAccountManager`）
- 在 settings.py 中設定 `AUTH_USER_MODEL`

## 🚀 功能特色

- ✅ 使用 Email 作為登入帳號（而非預設的 username）
- ✅ 自訂使用者欄位：`email`、`user_name`、`first_name`、`about`
- ✅ 支援建立一般使用者與超級使用者
- ✅ 完整的權限管理（PermissionsMixin）

## 📁 專案結構

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

### 1. 自訂使用者模型（models.py）

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

### 2. 自訂 User Manager

```python
class CustomerAccountManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        # 建立一般使用者
        ...
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        # 建立超級使用者
        ...
```

### 3. 設定檔修改（settings.py）

```python
AUTH_USER_MODEL = 'users.NewUser'
```

## 📦 安裝與使用

### 前置需求

- Python 3.x
- Django 3.2.5+

### 安裝步驟

1. Clone 專案：
```bash
git clone https://github.com/Michael-Yan-wun/Django_Customer_User.git
cd Django_Customer_User/CustomerAuth
```

2. 安裝依賴：
```bash
pip install django
```

3. 執行遷移：
```bash
python manage.py makemigrations
python manage.py migrate
```

4. 建立超級使用者：
```bash
python manage.py createsuperuser
```

## ⚠️ 重要注意事項

1. **在建立第一個 migration 之前設定**：`AUTH_USER_MODEL` 必須在建立第一個 migration 之前就設定好，否則後續修改會很困難。

2. **不要直接修改預設 User 模型**：應該建立新的自訂模型，而不是修改 Django 內建的 User 模型。

3. **外鍵引用**：在專案中引用使用者時，應該使用 `settings.AUTH_USER_MODEL` 而不是直接引用模型：
   ```python
   from django.conf import settings
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   ```

## 📝 使用範例

### 建立使用者

```python
from users.models import NewUser

# 建立一般使用者
user = NewUser.objects.create_user(
    email='user@example.com',
    user_name='johndoe',
    first_name='John',
    password='securepassword123'
)

# 建立超級使用者
admin = NewUser.objects.create_superuser(
    email='admin@example.com',
    user_name='admin',
    first_name='Admin',
    password='adminpassword123'
)
```

### 登入驗證

```python
from django.contrib.auth import authenticate

user = authenticate(email='user@example.com', password='securepassword123')
if user:
    print(f"登入成功：{user.user_name}")
```

## 🔗 相關資源

- [Django 官方文件 - Custom User Model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
- [Django 官方文件 - AbstractBaseUser](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser)

## 📄 授權

詳見 [LICENSE](LICENSE) 檔案。

## 👤 作者

Michael Lin

---

**注意**：這個專案僅供學習參考，在生產環境使用前請確保已充分測試並遵循 Django 最佳實踐。
