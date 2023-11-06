from apps.users.models import CustomUser


def find_existing_user(uid: int = None, email: str = None) -> bool:
    return CustomUser.objects.filter(id=uid).first() if uid is not None else CustomUser.objects.filter(
        email=email).first() if email is not None else False
