"""
Simple in-memory database for testing without MongoDB
"""

from argon2 import PasswordHasher

# In-memory storage
activities_store = {}
teachers_store = {}

class MockCollection:
    def __init__(self, store):
        self.store = store
    
    def find(self, query=None):
        if query is None:
            return [{"_id": k, **v} for k, v in self.store.items()]
        
        # Simple query support for the features we need
        result = []
        for key, value in self.store.items():
            match = True
            
            if "schedule_details.days" in query:
                days_query = query["schedule_details.days"]
                if "$in" in days_query:
                    if "schedule_details" not in value or "days" not in value["schedule_details"]:
                        match = False
                    else:
                        activity_days = value["schedule_details"]["days"]
                        if not any(day in activity_days for day in days_query["$in"]):
                            match = False
            
            if match:
                result.append({"_id": key, **value})
        
        return result
    
    def find_one(self, query):
        results = list(self.find(query))
        return results[0] if results else None
    
    def insert_one(self, doc):
        doc_id = doc.pop("_id")
        self.store[doc_id] = doc
    
    def count_documents(self, query):
        return len(list(self.find(query)))
    
    def delete_one(self, query):
        # Simple implementation
        if "_id" in query:
            if query["_id"] in self.store:
                del self.store[query["_id"]]
    
    def update_one(self, query, update):
        # Simple implementation for $push operations
        if "_id" in query and query["_id"] in self.store:
            if "$push" in update:
                for field, value in update["$push"].items():
                    if field not in self.store[query["_id"]]:
                        self.store[query["_id"]][field] = []
                    self.store[query["_id"]][field].append(value)
            if "$pull" in update:
                for field, value in update["$pull"].items():
                    if field in self.store[query["_id"]] and isinstance(self.store[query["_id"]][field], list):
                        if value in self.store[query["_id"]][field]:
                            self.store[query["_id"]][field].remove(value)
    
    def aggregate(self, pipeline):
        # Very simple aggregation for getting unique days
        if len(pipeline) >= 2 and pipeline[0].get("$unwind") == "$schedule_details.days":
            unique_days = set()
            for value in self.store.values():
                if "schedule_details" in value and "days" in value["schedule_details"]:
                    for day in value["schedule_details"]["days"]:
                        unique_days.add(day)
            return [{"_id": day} for day in sorted(unique_days)]
        return []

# Create mock collections
activities_collection = MockCollection(activities_store)
teachers_collection = MockCollection(teachers_store)

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""

    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "difficulty": "Beginner"
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, heart-pounding battles, and unforgettable friendships! Join fellow otaku to discuss your favorite manga heroes, from shonen legends to shoujo romance. Whether you're into epic power-ups, plot twists that hit like a truck-kun, or just want to share your latest manga haul, this is your dojo!",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]