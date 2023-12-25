from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def calculate_subscription_amount(subscription_type):
    amount_map = {
        'monthly': 1.00,
        'yearly': 1.00
    }
    return amount_map[subscription_type]

@login_required
def profile(request):
    
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Exclude subscription-related fields from the context
    context = {
        'user_profile': user_profile,
        
    }
    
    
    return render(request, 'users/profile.html', context)

def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Create a form instance and populate it with the user's data from the request
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()  # Save the updated user profile
            return redirect('profile')  # Redirect to the user's profile page
    else:
        # Display the form with the current user profile data
        form = UserProfileForm(instance=user_profile)

        context = {
            'form': form,
            # Exclude subscription fields in the template
        }
        return render(request, "users/edit_profile.html", context)
    
@login_required
def subscribe(request, subscription_type):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.is_subscriber and user_profile.subscription_end_date > timezone.now():
        return render(request, 'users/already_subscribed.html')

    # Validate the subscription type parameter
    if subscription_type not in ('monthly', 'yearly'):
        return redirect('profile')   # Redirect to the user's profile page with an error message if needed
       

    from instamojo_wrapper import Instamojo
    api = Instamojo(api_key= "test_1e634145b1355b72aa83faa1ef5",
                auth_token= "test_92e83bdeb7861354c09ae62a43f")
       

    try:
        response = api.payment_request_create(
            amount='9.0',
            purpose='Subscription Fee',
            send_email=True,
            email=user_profile.user.email,
            redirect_url='http://127.0.0.1/users/subscription-redirect/'
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    # print the long URL of the payment request.



    user_profile.is_subscriber = True
    user_profile.subscription_type = subscription_type
    user_profile.subscription_start_date = timezone.now()

    if subscription_type == 'monthly':
        user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=30)  # 30 days subscription
    else:
        user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=365)  # 365 days subscription

    user_profile.save()
    return redirect('profile')

def join(request):
    return render(request, "users/join.html")

def test(request):
    return render(request, "users/profile2.html")

def redirect1(request):
    return render(request, "users/profile.html")