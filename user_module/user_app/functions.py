from .models import CustomUser 
def get_user_details(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        return {
            "user_id": user.id,
            "name": user.username,
            "email": user.email,
            "mobile_number": user.mobile_number
        }
    except CustomUser.DoesNotExist:
        return {"error": "User not found"}