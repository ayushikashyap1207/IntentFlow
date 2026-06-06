import os
from supabase import create_client, Client

class SupabaseManager:
    def __init__(self):
        """
        Initializes the connection client using project environment configurations.
        """
        self.url = os.environ.get("SUPABASE_URL", "https://your-mock-url.supabase.co")
        self.key = os.environ.get("SUPABASE_KEY", "your-mock-anon-key")
        
        print(f"Connecting to Supabase Instance Endpoint: {self.url[:25]}...")
        self.client: Client = create_client(self.url, self.key)

    def log_behavior_sequence(self, class_name, sequence_matrix, confidence_score):
        """
        Saves the predicted behavior class, raw prediction confidence score, 
        and flattens the coordinate tracking points to store as a sequence vector record.
        """
        # Flatten the matrix sequence array down to a flat list for standard DB storage
        flattened_vector = sequence_matrix.flatten().tolist()
        
        data_payload = {
            "behavior_class": class_name,
            "confidence": float(confidence_score),
            "sequence_vector": flattened_vector
        }
        
        # Simulated database wire pipeline insertion for local tracking test phase
        print(f"📦 Storing behavior record for [{class_name}] ({len(flattened_vector)} coordinates)...")
        
        # In the next live integration step, this executes:
        # self.client.table("behavior_logs").insert(data_payload).execute()
        return True
