from decimal import Decimal
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm



# import view sets from the REST framework
from rest_framework import viewsets
from rest_framework import generics

# import the TodoSerializer from the serializer file
from .serializers import *

# import the Todo model from the models file
from .models import *

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .forms import ContactForm, FlavourServingsForm, NewUserForm

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

# Email AUTH
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings

import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

import urllib.request


# create a class for the Todo model viewsets
class MagnoliaCakesAndCupcakesView(viewsets.ModelViewSet):
    # create a serializer class and
    # assign it to the TodoSerializer class
    serializer_class = MagnoliaCakesAndCupcakesSerializer

    # define a variable and populate it
    # with the Todo list objects
    queryset = MagnoliaCakesAndCupcakes.objects.all()


############### Authentication view ###############
@api_view(["POST"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()

            # Create user profile
            UserVideo.objects.create(user=user)
            UserFirstOrder.objects.create(user=user)
            UserCustomerID.objects.create(user=user)

            return activateEmail(request, user, form.cleaned_data.get("username"))
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def activateEmail(request, user, to_email):

    mail_subject = "Activate your user account."

    context = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
    }

    message = render_to_string("template_activate_account.html", context)
    #added email_from
    email = EmailMessage(mail_subject, message, settings.EMAIL_FROM, to=[to_email])
    try:
        if email.send():
            return Response(
                {
                    "message": "User registered successfully. Please complete verification by clicking the link sent to your email."
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": "Problem sending confirmation email. Please contact an administrator."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as error:
        print(error)
        return Response(
            {
                "message": "Problem sending confirmation email. Please contact an administrator."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

from django.shortcuts import redirect

@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(f"{settings.FRONTEND_APP_URL}/login/?success=true")

    return redirect(f"{settings.FRONTEND_APP_URL}/login/?success=false")


@api_view(["POST"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request._request, data=request.data)
        print("form ", form.error_messages)

        if form.is_valid():
            username = request.data.get("username").lower()
            password = request.data.get("password")

            user = authenticate(request._request, username=username, password=password)
            if user is not None:
                django_login(
                    request._request, user
                )  # Use django_login instead of login
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "Login failed",
                        "error_messages": "user does not exist",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"message": "Login failed", "error_messages": form.error_messages},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

############### Base View ###############
@api_view(["GET", "PUT"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def terms_and_conditions(request):
    # Retrieve the t&c
    if request.method == "GET":
        terms = TermsAndCondition.objects.all()
        serializer = TermsAndConditionsSerializer(terms, many=True)
        return Response(serializer.data)
    
    # Admin edit t&c
    elif request.method == "PUT":
        terms = TermsAndCondition.objects.first()
        serializer = TermsAndConditionsSerializer(terms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Terms & Conditions updated"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def test_email(request):
    try:
        send_mail(
            'Test Subject',
            'Test Message',
            settings.EMAIL_FROM,
            ['pranavakumar98@gmail.com'],  # Replace with a test email address
            fail_silently=False,
        )
        return Response({"message": "Test email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Failed to send test email. Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def contact(request):
    if request.method == "GET":
        return Response({
            "message": "Contact form endpoint is ready. Please send a POST request with the form data to submit.",
            "required_fields": ["email", "subject", "message"],
            "optional_fields": ["file"]
        }, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        form = ContactForm(request.data, request.FILES)
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            files = request.FILES.getlist("file")

            admin_email_obj = ContactUsEmail.objects.first()
            backup_emails = BackupEmail.objects.all()

            to_emails = [admin_email_obj.your_email] if admin_email_obj else []
            to_emails.extend([e.email for e in backup_emails])

            if not to_emails:
                return Response(
                    {"message": "No admin email configured. Please contact the site administrator."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            email = EmailMessage(
                subject, 
                message,
                settings.EMAIL_FROM, 
                to=to_emails, 
                
                reply_to=[user_email]
            )

            for f in files:
                email.attach(f.name, f.read(), f.content_type)

            try:
                email.send()
                return Response(
                    {"message": "Success! Your message has been sent."}, 
                    status=status.HTTP_200_OK
                )
            except Exception as error:
                print(f"Email sending error: {str(error)}")  # Log the error
                return Response(
                    {
                        "message": "Problem sending email. Please contact an administrator.",
                        "error": str(error)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {"message": "Invalid form data", "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def products_list(request):
    if request.method == "GET":
        cakes = Product.objects.all()
        serializer = ProductSerializer(cakes, many=True)

        # Create a list to store the updated cake data with image URLs
        cakes_with_image_urls = []

        for cake_data in serializer.data:
            cake = Product.objects.get(id=cake_data["id"])
            # Add the image URL to the cake data
            cake_data["image"] = cake.picture.url
            cakes_with_image_urls.append(cake_data)

        return Response(cakes_with_image_urls, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def flavor_list(request):
    if request.method == "GET":
        flavor = Flavor.objects.all()
        serializer = FlavorSerializer(flavor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@permission_classes([AllowAny])
def cakes_list(request):
    if request.method == "GET":
        cakesizeprices = CakeVariant.objects.all()
        serializer = CakeSerializer(cakesizeprices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def slider_images(request):
    if request.method == "GET":
        images = SliderImage.objects.all()
        serializer = SliderImageSerializer(images, many=True)

        # Create a list to store the updated cake data with image URLs
        images_with_urls = []

        for image_data in serializer.data:
            imageObject = SliderImage.objects.get(id=image_data["id"])
            # Add the image URL to the cake data
            image_data["image"] = imageObject.image.url
            images_with_urls.append(image_data)

        return Response(images_with_urls, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def flavours_and_servings(request):
    if request.method == "GET":
        flavours_servings_lists = FlavoursAndServings.objects.all()
        serializer = FlavoursAndServingsSerializer(flavours_servings_lists, many=True)
        return Response(serializer.data)


@api_view(["GET", "PUT"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def about_us(request):
    if request.method == "GET":
        about_us = AboutUs.objects.first()
        serializer = AboutUsSerializer(about_us)
        return Response(serializer.data)

    elif request.method == "PUT":
        about_us = AboutUs.objects.first()
        serializer = AboutUsSerializer(about_us, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "About Us updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def faq_categories_list(request):
    if request.method == "GET":
        categories = FAQCategory.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])  # Assuming you want anyone to be able to access this
def reviews_list_create(request):
    """Handle GET and POST requests for reviews"""
    
    if request.method == "GET":
        reviews = Review.objects.all()  # Fetch all reviews
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new review to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def faq_questions_list(request):
    if request.method == "GET":
        questions = FAQQuestion.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def footer_location(request):
    if request.method == "GET":
        footer_location = FooterLocation.objects.first()
        serializer = FooterLocationSerializer(footer_location)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def footer_contact_us(request):
    if request.method == "GET":
        footer_contact = FooterContactUs.objects.first()
        serializer = FooterContactUsSerializer(footer_contact)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def footer_business_hrs(request):
    if request.method == "GET":
        footer_bushrs = FooterBusinessHours.objects.first()
        serializer = FooterBusinessHoursSerializer(footer_bushrs)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def social_medias(request):
    if request.method == "GET":
        social_media_accounts = SocialMedias.objects.all()
        serializer = SocialMediasSerializer(social_media_accounts, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def flavours_and_servings_info(request):
    if request.method == "GET":
        flavours_servings_info = FlavoursAndServingsInfo.objects.first()
        serializer = FlavoursAndServingsInfoSerializer(flavours_servings_info)
        return Response(serializer.data)


@api_view(["GET"])
def get_user(request):
    if request.method == "GET":
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(["POST"])
def reset_names(request):
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        if not (first_name and last_name):
            return Response({'error': 'Both first_name and last_name are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assuming you have an authenticated user, you can access it using request.user
        user = request.user
        
        try:
            # Update the first_name and last_name fields of the user
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Check if the user has a UserCustomerID associated with them
            try:
                user_customer_id = UserCustomerID.objects.get(user=user)
                
                # Update the Stripe customer's name using the Stripe API
                if user_customer_id.customer_id:
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    stripe.Customer.modify(
                        user_customer_id.customer_id,
                        name=f'{first_name} {last_name}'
                    )
            except UserCustomerID.DoesNotExist:
                # Handle the case where the user doesn't have a UserCustomerID
                UserCustomerID.objects.create(user=user)
            
            # Return a JSON response indicating success
            return Response({'message': 'Name updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Return an error response if any exception occurs during the update
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Return an error response for unsupported methods
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "PUT"])
@permission_classes([AllowAny])
def gallery_categories_list(request):
    if request.method == "GET":
        categories = GalleryCategory.objects.all()
        serializer = GalleryCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def gallery_items_list(request):
    if request.method == "GET":
        items = GalleryItem.objects.all()
        serializer = GalleryItemSerializer(items, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def location_page_content(request):
    if request.method == "GET":
        location_page_content = LocationPageContent.objects.first()
        serializer = LocationPageContentSerializer(location_page_content)
        return Response(serializer.data)

@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def welcome_section(request):
    if request.method == "GET":
        content = HomepageWelcomeSection.objects.first()
        serializer = WelcomeSectionContentSerializer(content)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def about_us_section(request):
    if request.method == "GET":
        content = HomepageAboutUsSection.objects.first()
        serializer = AboutUsSectionContentSerializer(content)
        return Response(serializer.data)

'''

@api_view(["GET"])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def gallery_section(request):
    if request.method == "GET":
        content = HomepageGallerySection.objects.first()
        serializer = GallerySectionContentSerializer(content)
'''
@api_view(["GET"])
@permission_classes([AllowAny])  ###### Add this to allow users to access despite not being logged in
def gallery_section(request):
    if request.method == "GET":
        # Retrieve the first object from the HomepageGallerySection model
        content = HomepageGallerySection.objects.first()
        
        # Check if content is None
        if content is None:
            return Response({"message": "No gallery content found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the content
        serializer = GallerySectionContentSerializer(content)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def video(request):
    if request.method == "GET":
        items = Video.objects.all()
        serializer = VideoSerializer(items, many=True)
        return Response(serializer.data)
       


'''
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_quote(request):
    if request.method == "GET":
        return Response({
            "message": "Get a Quote endpoint is ready. Please send a POST request with the form data to submit.",
            "required_fields": ["name", "email", "servings_or_amount"],
            "optional_fields": ["mobile", "product_type", "serves", "date_of_event", "flavour", "filling"]
        }, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            quote = serializer.save()
            
            # Prepare email
            subject = f"New Quote Request from {quote.name}"
            message = f"""
            A new quote request has been submitted:
            
            Name: {quote.name}
            Email: {quote.email}
            Mobile: {quote.mobile or 'Not provided'}
            Product Type: {quote.product_type or 'Not specified'}
            Servings/Amount: {quote.servings_or_amount}
            Serves: {quote.serves or 'Not specified'}
            Date of Event: {quote.date_of_event or 'Not specified'}
            Flavour: {quote.flavour or 'Not specified'}
            Filling: {quote.filling or 'Not specified'}
            Time Submitted: {quote.time_submitted}
            """

            admin_email_obj = ContactUsEmail.objects.first()
            backup_emails = BackupEmail.objects.all()

            to_emails = [admin_email_obj.your_email] if admin_email_obj else []
            to_emails.extend([e.email for e in backup_emails])

            if not to_emails:
                return Response(
                    {"message": "Quote saved, but no admin email configured to send notification."},
                    status=status.HTTP_200_OK
                )

            try:
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    to=to_emails,
                    reply_to=[quote.email]  # Set Reply-To header to customer's email
                )
                email.send()
                return Response(
                    {"message": "Quote submitted successfully and notification sent."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as error:
                print(f"Email sending error: {str(error)}")  # Log the error
                return Response(
                    {"message": "Quote saved but there was a problem sending email notification."},
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
@api_view(['GET'])
def get_videos(request):
    if request.method == "GET":
        user = request.user
        try:
            user_profile = UserVideo.objects.get(user=user)
            videos = user_profile.videos.all()
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        except UserVideo.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)

'''
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_quote(request):

    if request.method == "POST":
        serializer = QuoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Quote data logged"}, status=status.HTTP_200_OK)
        return Response({"serializer_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_quote(request):
    if request.method == "GET":
        return Response({
            "message": "Get a Quote endpoint is ready. Please send a POST request with the form data to submit.",
            "required_fields": ["name", "email", "servings_or_amount"],
            "optional_fields": ["mobile", "product_type", "serves", "date_of_event", "flavour", "filling"]
        }, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        print("Received POST request to log_quote view")  # Log the request

        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            quote = serializer.save()
            
            # Prepare email
            subject = f"New Quote Request from {quote.name}"
            message = f"""
            A new quote request has been submitted:
            
            Name: {quote.name}
            Email: {quote.email}
            Mobile: {quote.mobile or 'Not provided'}
            Product Type: {quote.product_type or 'Not specified'}
            Servings/Amount: {quote.servings_or_amount}
            Serves: {quote.serves or 'Not specified'}
            Date of Event: {quote.date_of_event or 'Not specified'}
            Flavour: {quote.flavour or 'Not specified'}
            Filling: {quote.filling or 'Not specified'}
            Time Submitted: {quote.time_submitted}
            """

            admin_email_obj = ContactUsEmail.objects.first()
            backup_emails = BackupEmail.objects.all()

            # Prevent duplicate admin emails
            to_emails = list(set([admin_email_obj.your_email] if admin_email_obj else []))
            backup_emails_set = set([e.email for e in backup_emails])
            to_emails.extend(list(backup_emails_set))  # Extend with unique emails

            print(f"Email will be sent to: {to_emails}")  # Debugging line to confirm recipients

            if not to_emails:
                return Response(
                    {"message": "Quote saved, but no admin email configured to send notification."},
                    status=status.HTTP_200_OK
                )

            try:
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    to=to_emails,
                    reply_to=[quote.email]  # Set Reply-To header to customer's email
                )
                
                # Log before sending email
                print(f"Attempting to send email to: {to_emails}")  # Debugging line to confirm send

                email.send()
                print("Email sent successfully!")  # Debugging line to confirm successful send
                return Response(
                    {"message": "Quote submitted successfully and notification sent."},
                    status=status.HTTP_201_CREATED
                )
            except Exception as error:
                print(f"Email sending error: {str(error)}")  # Log the error
                return Response(
                    {"message": "Quote saved but there was a problem sending email notification."},
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def log_quote(request):

    if request.method == "POST":
        serializer = QuoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Quote data logged"}, status=status.HTTP_200_OK)
        return Response({"serializer_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
############### Checkout with Stripe ###############
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    
    # Get the cart items from the request
    cart_items = request.data.get('items', [])
    
    # Transform cart items into line items for Stripe checkout
    line_items = []
    
    # Retrieve video list if any 
    video_items = []
    cake_items = []
    cakes = []
    cupcakes = []
    for item in cart_items:

        try:
            # Convert the price to a float and then to an integer (cents)
            price = int(float(item.get('price', 0)) * 100)
        except ValueError:
            # Handle the case where the price is not a valid number
            # You may want to log an error or take appropriate action here
            price = 0
        
        # Get price_id for product
        gotPrice = False
        cake_id = item.get("cakeId")
        if cake_id != None:
            try:
                cake = CakeVariant.objects.get(id=cake_id)
                if (cake.price_id):
                    line_item = {
                        'price': cake.price_id,
                        'quantity': item.get('quantity', 1),
                    }
                    gotPrice = True

            except CakeVariant.DoesNotExist:
                cake = Product.objects.get(id=cake_id)
                if (cake.price_id):
                    line_item = {
                        'price': cake.price_id,
                        'quantity': item.get('quantity', 1),
                    }
                    gotPrice = True

            except Product.DoesNotExist:
                return Response({'error': 'CakeVariant and Product not found'}, status=404)

        video_id = item.get("videoId")
        if video_id != None:
            video = get_object_or_404(Video, id=video_id)
            if (video.price_id):
                line_item = {
                    'price': video.price_id,  # Stripe price ID associated with the product
                    'quantity': item.get('quantity', 1),
                }
                gotPrice = True


        if not gotPrice:
            line_item = {
                'price_data': {
                    'currency': 'aud',
                    'product_data': {
                        'name': item.get('name', 'Product'),
                    },
                    'unit_amount': price,  # Amount in cents
                },
                'quantity': item.get('quantity', 1),
            }
        # add to the list if not null
        video_item = item.get("videoId")
        if video_item != None:
            video_items.append(video_item)
        else:
            cake_items.append(item.get('cakeId'))
            if item.get("type") == "cake":
                cakes.append(item.get('cakeId'))
            else:
                cupcakes.append(item.get('cakeId'))
            
        line_items.append(line_item)

    # Calculate total amount
    total_amount = Decimal(sum(Decimal(item['price']) * int(item['quantity']) for item in cart_items))

    # Constants for service fees
    F_fixed = Decimal('0.30')  # Fixed fee after VAT/GST is included
    F_percent = Decimal('0.0175')  # Percent fee after VAT/GST is included

    # Calculate the amount to charge the customer including fees
    P_charge = (total_amount + F_fixed) / (1 - F_percent)
    
    # Add service fees as a display item
    service_fees_item = {
        'price_data': {
            'currency': 'aud',
            'unit_amount': int((P_charge-total_amount) * 100),  # Convert to cents
            'product_data': {
                'name': 'Service Fees',
                'description': 'Service Fees for the transaction',
            },
        },
        'quantity': 1,
    }
    # Serialize the video array to json
    
    video_items_json = json.dumps(video_items)
    cake_items_json = json.dumps(cakes)
    cupcakes_items_json = json.dumps(cupcakes)
    
   
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[*line_items, service_fees_item],
        mode='payment',
        allow_promotion_codes=True,
        # Return back to the frontend with correspond path when payment success or cancelled
        success_url = f"{settings.FRONTEND_APP_URL}/success?checkout_session={{CHECKOUT_SESSION_ID}}&user={request.data.get('email')}&code={video_items_json}&i={cake_items_json}&x={cupcakes_items_json}",
        cancel_url= f"{settings.FRONTEND_APP_URL}/online-store",
        customer = request.data.get('customer_id')
    )

    return Response({'id': checkout_session.id, 'total_amount_with_fees': round(P_charge, 2)})


############### Payment views ###############
@api_view(['POST'])
def purchase_videos(request, video_id):
    if request.method == "POST":
        user = request.user
        try:
            # Retrieve the video object by its ID
            video = Video.objects.get(id=video_id)

            user_profile = UserVideo.objects.get(user=user)
            
            # Add the video to the user's videos list (assuming a ManyToMany relationship)
            user_profile.videos.add(video)
            
            return Response({'message': 'Video added to user videos list'}, status=200)
        except UserVideo.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)

@api_view(['GET'])
@permission_classes(
    [AllowAny]
)  ###### Add this to allow users to access despite not being logged in
def get_displayed_promotion(request):
    if request.method == "GET":
        promotion = get_object_or_404(StripePromotion, is_displayed=True)
        data = {
            'code': promotion.code,
            'description': promotion.description,
            'only_logged_in_users': promotion.only_logged_in_users,
            'only_first_purchase_of_user': promotion.only_first_purchase_of_user,
            'display_after': promotion.display_after
        }
        return Response(data, status=200)
    
@api_view(['GET'])
def get_user_firstOrderBoolean(request):
    if request.method == "GET":
        user = request.user
        try:
            user_firstOrder = UserFirstOrder.objects.get(user=user)
            madeFirstOrder = user_firstOrder.madeFirstOrder
            return Response({"madeFirstOrder": madeFirstOrder}, status=200)
        except UserVideo.DoesNotExist:
            return Response({'message': 'User not found in UserFirstOrder.'}, status=404)

@api_view(['POST'])
def set_user_firstOrder_true(request):
    if request.method == "POST":
        user = request.user
        try:
            user_firstOrder = UserFirstOrder.objects.get(user=user)
            user_firstOrder.madeFirstOrder = True
            user_firstOrder.save()
            return Response({"madeFirstOrder": True}, status=200)
        except UserVideo.DoesNotExist:
            return Response({'message': 'User not found in UserFirstOrder.'}, status=404)

@api_view(['POST'])
def process_order(request):
    if request.method == "POST":
        serializer = UserPurchaseSerializer(data=request.data, context={'user': request.user, 'request_data': request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_orders(request):
    if request.method == "GET":
        user = request.user
        queryset = UserPurchase.objects.filter(user=user)
        serializer = UserPurchaseSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_data = {
        'id': video.id,
        'title': video.title,
        'price': video.price,
    }
    return Response(video_data, status=200)

@api_view(['GET'])
def get_cake(request, cake_id):
    cake = get_object_or_404(CakeVariant, id=cake_id)
    cake_data = {
        'id': cake.id,
        'name': cake.product_name,
        'price': cake.price,
        'price_id': cake.price_id
    }
    return Response(cake_data, status=200)

@api_view(['GET'])
def get_cupcake(request, cake_id):
    cake = get_object_or_404(Product, id=cake_id)
    cake_data = {
        'id': cake.id,
        'name': cake.name,
        'price': cake.price,
        'price_id': cake.price_id
    }
    return Response(cake_data, status=200)
    
@api_view(['GET'])
def get_customer_id(request):
    if request.method == "GET":
        user = request.user
        try:
            user_customer_id = UserCustomerID.objects.get(user=user)
            serializer = UserCustomerIDSerialiser(user_customer_id)
            return Response(serializer.data)
        except UserCustomerID.DoesNotExist:
            # Handle the case where the UserCustomerID does not exist for the user.
            return Response({"detail": "UserCustomerID does not exist for this user."}, status=status.HTTP_404_NOT_FOUND)

# Retrive transaction
@api_view(['GET'])
def get_stripe_session(request, session_id):
    stripe_key = settings.STRIPE_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {stripe_key}",
    }

    try:
        response = requests.get(f"https://api.stripe.com/v1/checkout/sessions/{session_id}", headers=headers)
        response.raise_for_status()
        session_data = response.json()
        return Response(session_data)
    except Exception as e:
        return Response({"error": str(e)})