from django.contrib.auth.models import AbstractUser


# p215 カスタムユーザーモデルを定義
class CustomUser(AbstractUser):
    # 拡張ユーザーモデル
    class Meta:
        verbose_name_plural = 'CustomUser'

# settingsのauth_user_model = 'accounts.CustomUser'
