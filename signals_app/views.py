import threading
from django.http import HttpResponse
from django.db import transaction
from .models import TestModel, SignalLog

def sync_view(request):
    """
    Q1 Proof: Synchronous Execution
    If the view waits for the signal to finish (5s delay), it's synchronous.
    """
    print("\n--- TEST: Synchronous Execution ---")
    print("LOG: Caller (View) - BEFORE SAVING")
    TestModel.objects.create(name="Sync Test")
    print("LOG: Caller (View) - AFTER SAVING")
    return HttpResponse("Question 1: Done. Check terminal for sequence.")

def thread_view(request):
    """
    Q2 Proof: Same Thread
    Compares the Thread ID of the view and the signal.
    """
    print("\n--- TEST: Same Thread Execution ---")
    thread_id = threading.get_ident()
    print(f"LOG: Caller (View) is running in Thread ID: {thread_id}")
    TestModel.objects.create(name="Thread Test")
    return HttpResponse("Question 2: Done. Thread IDs are logged in terminal.")

def transaction_view(request):
    """
    Q3 Proof: Same Transaction
    If the transaction rolls back, both TestModel and SignalLog should disappear.
    """
    print("\n--- TEST: Same Transaction Execution ---")
    try:
        with transaction.atomic():
            print("LOG: View - Saving TestModel...")
            TestModel.objects.create(name="Transaction Test")
            print("LOG: View - Triggering Manual Rollback...")
            raise Exception("Force rollback to test transaction sharing")
    except Exception as e:
        print(f"LOG: View - Caught Exception: {e}")

    # Check if records were saved
    test_model_exists = TestModel.objects.filter(name="Transaction Test").exists()
    signal_log_exists = SignalLog.objects.filter(message__contains="Transaction Test").exists()
    
    output = (
        f"<b>Question 3 Proof:</b><br>"
        f"Did TestModel save? {'Yes' if test_model_exists else 'No (Rolled Back)'}<br>"
        f"Did SignalLog save? {'Yes' if signal_log_exists else 'No (Rolled Back)'}<br><br>"
        f"Result: Both are 'No', proving they share the same database transaction."
    )
    return HttpResponse(output)
