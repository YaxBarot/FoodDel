from django.db import models

from common.models import Audit


class Customers(Audit):
    class Meta:
        db_table = 'fd_customers'

    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)
    password = models.TextField()

    mobile_no = models.CharField(max_length=50, null=True, unique=True, db_column="mobile_number")

    dob = models.DateField(db_column="usr_dob", null=True)

    # usr_profile_image = models.TextField(null=True, db_column="usr_profile_pic")

class CustomerOTP(Audit):
    class Meta:
        db_table = "fd_customer_otp"

    customer_otp_id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255)