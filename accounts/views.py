from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registered successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email,
        })
    return Response({"error": "Invalid credentials"}, status=401)

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
import requests
from django.conf import settings

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal whether the email exists — always respond the same way
        return Response({"message": "If that email is registered, a reset link has been sent."})

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = f"{settings.FRONTEND_URL}/reset-password.html?uid={uid}&token={token}"

    requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": settings.BREVO_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "sender": {"email": settings.DEFAULT_FROM_EMAIL},
            "to": [{"email": email}],
            "subject": "Reset your TenderSphere password",
            "htmlContent": f"<p>Click this link to reset your password:</p><p><a href='{reset_link}'>{reset_link}</a></p><p>If you didn't request this, ignore this email.</p>",
        },
    )
    return Response({"message": "If that email is registered, a reset link has been sent."})


@api_view(['POST'])
def reset_password(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Invalid reset link."}, status=400)

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        return Response({"error": "This reset link has expired or is invalid."}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password reset successfully."})

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
def get_profile(request):
    auth = JWTAuthentication()
    try:
        user, token = auth.authenticate(request)
    except Exception:
        return Response({"error": "Invalid or missing token"}, status=401)

    if user is None:
        return Response({"error": "Invalid or missing token"}, status=401)

    profile = user.profile
    return Response({
        "username": user.username,
        "email": user.email,
        "phone": profile.phone,
        "state": profile.get_state_display(),
        "tender_interests": profile.tender_interests,
    })


from rest_framework.permissions import IsAdminUser
from .models import Tender

@api_view(['POST'])
def add_tender(request):
    auth = JWTAuthentication()
    try:
        user, token = auth.authenticate(request)
    except Exception:
        return Response({"error": "Invalid or missing token"}, status=401)

    if user is None or not user.is_staff:
        return Response({"error": "Admin access required"}, status=403)

    data = request.data
    try:
        tender = Tender.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            department=data.get('department'),
            category=data.get('category'),
            state=data.get('state'),
            tender_value=data.get('tender_value', ''),
            deadline=data.get('deadline'),
            reference_number=data.get('reference_number'),
            document_link=data.get('document_link', ''),
        )
        return Response({"message": "Tender added successfully", "id": tender.id}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)