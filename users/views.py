from django.core.mail import send_mail
from django.conf import settings
import json

# Create your views here.
from django.shortcuts import render, redirect
from .models import UserProfile, SubcriptionInfo
from .forms import UserProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay


def calculate_subscription_amount(subscription_type):
    amount_map = {
        'monthly': 50*100,
        'yearly': 600*100,
    }
    return amount_map[subscription_type]


def calculate_subscription_end_date(subscription_type):
    if subscription_type == 'monthly':
        return timezone.now() + timezone.timedelta(days=30)  # 30 days subscription
    elif subscription_type == 'yearly':
        return timezone.now() + timezone.timedelta(days=365)  # 365 days subscription
    else:
        raise ValueError("Invalid subscription type")
    

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
    
    try:
        client = razorpay.Client(auth=("rzp_test_D1XgJg5irfvjg1", "9VRwJqkvPzeqiD21h2Q6qwKb"))
        payment = client.order.create({'amount': calculate_subscription_amount(subscription_type), "currency": "INR", "payment_capture": "1"})

        # Fetch existing or create a new SubscriptionInfo instance
        subscription_info = SubcriptionInfo.objects.create(
            user=request.user,
            activation_date=timezone.now(),
            expiry_date=calculate_subscription_end_date(subscription_type),
            amount=calculate_subscription_amount(subscription_type)/100,
            order_id=payment['id'],
            paid=False,
            subscription_type=subscription_type,
            )
        

    except Exception as e:
        print(f"Error: {e}")
        print(calculate_subscription_amount(subscription_type))
    paydict= {
            "order_id":payment["id"],
            "amount":payment["amount"]/100,
            "username":user_profile.user.username,
            "email": user_profile.user.email,
            "activation_date": timezone.now(),
            "expiry_date": calculate_subscription_end_date(subscription_type),
            "subscription_type": subscription_type,
        }

    return render(request, "users/pay.html", {"payment" :paydict})


def join(request):
    return render(request, "users/join.html")


@csrf_exempt
def redirect1(request):
    if request.method =="POST":
        data= request.POST
        order_id= data["razorpay_order_id"]
        payment_id= data["razorpay_payment_id"]

        order= SubcriptionInfo.objects.get(order_id=order_id)

        if order_id == order.order_id:
            order.paid = True
            order.payment_id= payment_id
            order.save()

            user= order.user
            user_profile = UserProfile.objects.get(user=user)

            user_profile.is_subscriber = True
            subscription_type= order.subscription_type
            user_profile.subscription_start_date = timezone.now()

            if subscription_type == 'monthly':
                user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=30)  # 30 days subscription
            else:
                user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=365)  # 365 days subscription

            user_profile.save()

    return render(request, "main/index.html")


@csrf_exempt
def redirect(request):
    if request.method =="POST":
        data= request.POST
        if 'error[code]' in data:
            error_code= request.POST.get('error[code]')
            error_description= request.POST.get('error[description]')
            meta=   request.POST.get('error[metadata]')
            parsed_dict = json.loads(meta)
            payment_id = parsed_dict.get('payment_id')
            order_id = parsed_dict.get('order_id')
            data= {"code": error_code, "description": error_description, "payment_id":payment_id, "order_id":order_id}
            user_email = user.email
            subject = 'Payment Failed'
            message = 'Payment Failed.Money will be refunded to you eithin a week if deducted'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user_email]

            send_mail(subject, message, from_email, recipient_list)
            return render(request, "users/payment_error.html", {"data": data})
        else:

            order_id= data["razorpay_order_id"]
            payment_id= data["razorpay_payment_id"]
            data= {"id": order_id}

            order= SubcriptionInfo.objects.get(order_id=order_id)

            if order_id == order.order_id:
                order.paid = True
                order.payment_id= payment_id
                order.save()

                user= order.user
                user_profile = UserProfile.objects.get(user=user)

                user_profile.is_subscriber = True
                subscription_type= order.subscription_type
                user_profile.subscription_start_date = timezone.now()

                if subscription_type == 'monthly':
                    user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=30)  # 30 days subscription
                else:
                    user_profile.subscription_end_date = timezone.now() + timezone.timedelta(days=365)  # 365 days subscription

                user_profile.save()
                user_email = user.email
                subject = 'Payment Successful - Subscription Confirmed'
                message = 'Thank you for your payment. Your subscription has been confirmed.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user_email]

                send_mail(subject, message, from_email, recipient_list)


    return render(request, "users/payment_success.html", {"data":data})
