import time
from typing import List

# Represents a single locker unit
class Locker:
    def __init__(self, locker_id: int, size: str):
        # Assign unique ID to the locker
        self.locker_id = locker_id
        # Size can be 'small', 'medium', or 'large'
        self.size = size
        # Tracks whether this locker is currently occupied
        self.is_occupied = False
        # Stores the parcel assigned to this locker
        self.parcel = None
        # Stores expiration timestamp for pickup window
        self.expiry_time = None

    # Assigns a parcel to this locker with a time limit
    def assign_parcel(self, parcel, pickup_duration_secs):
        self.is_occupied = True
        self.parcel = parcel
        self.expiry_time = time.time() + pickup_duration_secs

    # Frees the locker for reuse
    def free(self):
        self.is_occupied = False
        self.parcel = None
        self.expiry_time = None


# Represents a parcel that needs to be stored
class Parcel:
    def __init__(self, parcel_id: int, size: str, user):
        # Unique ID for the parcel
        self.parcel_id = parcel_id
        # Size of the parcel to match locker sizes
        self.size = size
        # User who owns the parcel
        self.user = user


# Represents the customer who will pick up the parcel
class User:
    def __init__(self, user_id: int, name: str, contact: str):
        self.user_id = user_id
        self.name = name
        self.contact = contact


# Responsible for sending notifications to users
class NotificationService:
    def send_notification(self, user: User, message: str):
        # Simulate sending notification (print for now)
        print(f"Notification to {user.name} ({user.contact}): {message}")


# Holds a collection of lockers
class LockerBank:
    def __init__(self, lockers: List[Locker]):
        self.lockers = lockers

    # Finds the first available locker that matches the parcel size
    def find_available_locker(self, size: str):
        for locker in self.lockers:
            if locker.size == size and not locker.is_occupied:
                return locker
        return None


# Handles the logic for assigning lockers
class LockerAssignmentService:
    def __init__(self, locker_bank: LockerBank, notifier: NotificationService):
        self.locker_bank = locker_bank
        self.notifier = notifier

    # Assigns a parcel to an appropriate locker and notifies user
    def assign_locker_to_parcel(self, parcel: Parcel, pickup_duration_secs: int = 30):
        # Search for available locker
        locker = self.locker_bank.find_available_locker(parcel.size)
        if not locker:
            print("No available locker for size:", parcel.size)
            return None

        # Assign the parcel to the locker
        locker.assign_parcel(parcel, pickup_duration_secs)

        # Notify user of locker assignment
        self.notifier.send_notification(parcel.user,
            f"Parcel {parcel.parcel_id} assigned to Locker {locker.locker_id}. Pickup within {pickup_duration_secs} seconds.")
        return locker


# Main class that coordinates the entire locker system
class LockerSystem:
    def __init__(self, locker_bank: LockerBank, assignment_service: LockerAssignmentService):
        self.locker_bank = locker_bank
        self.assignment_service = assignment_service

    # User drops off a parcel (gets a locker assigned)
    def drop_off_parcel(self, parcel: Parcel):
        return self.assignment_service.assign_locker_to_parcel(parcel)

    # User picks up a parcel from locker by ID
    def pick_up_parcel(self, locker_id: int):
        for locker in self.locker_bank.lockers:
            if locker.locker_id == locker_id and locker.is_occupied:
                # Check if pickup is within the allowed time
                if time.time() > locker.expiry_time:
                    print(f"Locker {locker_id} expired. Parcel removed.")
                    locker.free()
                    return False
                print(f"Parcel {locker.parcel.parcel_id} picked up from Locker {locker_id}")
                locker.free()
                return True
        print("Invalid locker or empty.")
        return False
