from django.db import models


class Audit(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class CustomerAuthTokens(models.Model):
    class Meta:
        db_table = 'fd_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)

class RestaurantAuthTokens(models.Model):
    class Meta:
        db_table = 'fd_restaurant_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)

class AdministratorAuthTokens(models.Model):
    class Meta:
        db_table = 'fd_admin_auth_tokens'

    access_token = models.TextField(null=True, db_column="auth_access_token")
    refresh_token = models.TextField(null=True, db_column="auth_refresh_token")
    created_at = models.DateTimeField(auto_now_add=True)