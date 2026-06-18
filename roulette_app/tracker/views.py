import os
import json
from django.shortcuts import render
import google.generativeai as genai
from PIL import Image

from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import FriendGroup, Bill, Debt
from django.db.models import Sum, Count

def home(request):
    extracted_data = None
    
    # Configure Gemini using the secure .env file
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)

    # If the user submits a form with a receipt image...
    if request.method == 'POST' and request.FILES.get('receipt'):
        receipt_file = request.FILES['receipt']
        img = Image.open(receipt_file)
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = """
            Analyze this receipt carefully. Return a strictly formatted JSON object containing:
            1. "store_name": The name of the store.
            2. "items": A list of objects, each with "name" (string) and "price" (number).
            3. "total": The final total amount paid (number).
            Do not include markdown.
            """
            response = model.generate_content([prompt, img])
            extracted_data = json.loads(response.text.strip())
            
        except Exception as e:
            extracted_data = {"error": str(e)}

    # Send the data to an HTML template (which we will build next)
    return render(request, 'tracker/index.html', {'data': extracted_data})

def save_split(request):
    if request.method == 'POST':
        # Load the JSON data sent from Javascript
        data = json.loads(request.body)
        
        # 1. Get or create a default group for your squad
        group, _ = FriendGroup.objects.get_or_create(name="My Squad")
        
        # 2. Save the Bill record
        bill = Bill.objects.create(
            group=group,
            store_name=data.get('store_name', 'Unknown Store'),
            total_amount=data.get('total_amount', 0)
        )
        
        # 3. Save individual Debts
        for friend_name, amount in data.get('payouts', {}).items():
            # Create a user profile for the friend if they don't exist yet
            user, _ = User.objects.get_or_create(username=friend_name)
            group.members.add(user) # Ensure they are in the squad
            
            is_loser = (friend_name == data.get('loser'))
            
            # Save the permanent debt record!
            Debt.objects.create(
                bill=bill,
                payer=user,
                amount_owed=amount,
                was_roulette_loser=is_loser
            )
            
        return JsonResponse({"status": "success", "message": "Saved to Supabase!"})
    
    return JsonResponse({"status": "error"}, status=400)

def dashboard(request):
    # 1. High-level Stats
    total_bills = Bill.objects.count()
    total_money = Bill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # 2. Unluckiest Friends (Group by payer, count how many times they lost)
    unluckiest = Debt.objects.filter(was_roulette_loser=True) \
        .values('payer__username') \
        .annotate(losses=Count('id')) \
        .order_by('-losses')[:5]
        
    # 3. The Debt Board (Group by payer, sum total amount owed)
    all_debts = Debt.objects.values('payer__username') \
        .annotate(total_owed=Sum('amount_owed')) \
        .order_by('-total_owed')

    context = {
        'total_bills': total_bills,
        'total_money': total_money,
        'unluckiest': unluckiest,
        'all_debts': all_debts
    }
    
    return render(request, 'tracker/dashboard.html', context)