class RoleMiddleware:
    """
    Attaches the user's role to the request object.
    Reads from user.profile.role (UserProfile model).
    Anonymous users get role='free'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.core.exceptions import ObjectDoesNotExist
        from apps.core.models import UserProfile, UserRole

        if request.user.is_authenticated:
            try:
                request.role = request.user.profile.role
            except (ObjectDoesNotExist, AttributeError):
                UserProfile.objects.get_or_create(
                    user=request.user, defaults={'role': UserRole.FREE}
                )
                request.role = request.user.profile.role
        else:
            request.role = UserRole.FREE

        response = self.get_response(request)
        return response
