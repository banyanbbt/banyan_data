from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager
from django.contrib.auth.hashers import make_password
from apps.user.model_status import USER_TYPE_STATUS


class UserProfileManager(BaseUserManager):

    def create_user(self, email, password):
        user = self.create(email=email,
                           password=make_password(password),
                           is_active=True,
                           is_staff=False,
                           is_superuser=False,
                           user_type='normal')
        return user

    def get_by_natural_key(self, email):
        return self.get(**{self.model.EMAIL_FIELD: email})

    def create_superuser(self, username, email, password):
        user = self.create(username=username,
                           email=email,
                           password=make_password(password),
                           is_active=True,
                           is_staff=True,
                           is_superuser=True)
        return user

    def create_company_user(self, email, password, customer_id):
        return self.create(email=email, password=make_password(password),
                           customer_id=customer_id, is_active=True,
                           is_staff=False, is_superuser=False,
                           user_type=USER_TYPE_STATUS['company'])


class UserApplyInterfaceInfoManager(Manager):

    def build_apply_interface_info(self, product_name, contact_name, contact_mobile, expected_dosage):
        self.create(product_name=product_name,
                    contact_name=contact_name,
                    contact_mobile=contact_mobile,
                    expected_dosage=expected_dosage)
