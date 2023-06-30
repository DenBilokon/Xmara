from users.models import Avatar


def avatar_url(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return {'avatar_url': avatar.image.url if avatar else None}
