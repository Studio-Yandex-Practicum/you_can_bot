from django.contrib.auth.mixins import UserPassesTestMixin


class IsStaffMixin(UserPassesTestMixin):
    """Mixin для проверки, является ли пользователь сотрудником."""

    def test_func(self):
        return self.request.user.is_staff
