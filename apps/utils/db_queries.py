from apps.users.models import CustomUser


def find_user(email: str) -> bool:
    user = CustomUser.objects.filter(email=email).exists()
    return user

