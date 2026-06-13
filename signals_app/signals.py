import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestModel, SignalLog

@receiver(post_save, sender=TestModel)
def my_signal_handler(sender, instance, created, **kwargs):
    # --- Proof for Question 1 (Synchronous) ---
    print("LOG: Signal Execution - STARTED")
    time.sleep(5)  # Significant delay to prove the caller waits
    
    # --- Proof for Question 2 (Thread) ---
    current_thread = threading.get_ident()
    print(f"LOG: Signal is running in Thread ID: {current_thread}")
    
    # --- Proof for Question 3 (Transaction) ---
    # We create a log entry here. If signals were in a separate transaction, 
    # this would persist even if the caller rolls back. 
    SignalLog.objects.create(message=f"Signal Log for {instance.name}")
    
    print("LOG: Signal Execution - FINISHED")
