from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext
from difflib import SequenceMatcher
from django.core.exceptions import FieldDoesNotExist
import re
from django.utils.translation import gettext as _



# https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/#MinimumLengthValidator

def exceeds_maximum_length_ratio(password, max_similarity, value):
    pwd_len = len(password)
    length_bound_similarity = max_similarity / 2 * pwd_len
    value_len = len(value)
    return pwd_len >= 10 * value_len and value_len < length_bound_similarity

class MinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "你的密碼必須大於 %(min_length)d 個字元",
                    "你的密碼必須大於 %(min_length)d 個字元",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
       return ngettext(
           "你的密碼必須大於 %(min_length)d 個字元",
           "你的密碼必須大於 %(min_length)d 個字元",
           self.min_length
       ) % {'min_length': self.min_length}
    
class UserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("密碼與帳號太相近"),
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

    def get_help_text(self):
        return _(
            "密碼與帳號太相近"
        )

class CommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("此組密碼太簡單"),
                code="password_too_common",
            )

    def get_help_text(self):
        return _("此組密碼太過於簡單，請嘗試更複雜的密碼")
class NumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("密碼不能完全由數字組成"),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("密碼不能完全由數字組成")
