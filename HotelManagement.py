from enum import Enum

# Enum gives us a simple way to name a fixed list of options.
# =============================================================================
# Interview-Based Design Notes (as code comments)
# =============================================================================
# Problem Statement:
#   Design a hotel management system to register guests, manage rooms of various
#   types, handle reservations, check-in/check-out, and process payments
#   safely in a multi-threaded environment.
#
# Functional Requirements:
#   1. Guest registry: add & look up guests (ID, name, contact info).
#   2. Room catalog: track RoomType (SINGLE, DOUBLE, DELUXE, SUITE) and
#      RoomStatus (AVAILABLE, BOOKED, OCCUPIED).
#   3. Booking flow:
#      - Reserve a room   (AVAILABLE → BOOKED)
#      - Check in         (BOOKED   → OCCUPIED)
#      - Check out        (OCCUPIED → AVAILABLE)
#      - Cancel reservation (CONFIRMED → CANCELLED, then free room)
#   4. Payment abstraction: support multiple payment methods behind a common
#      interface.
#   5. Concurrency: prevent race conditions on rooms & reservations.
#
# Non-Functional Requirements:
#   - Thread safety via locks at both object & system levels.
#   - Single source of truth (one front-desk instance).
#   - Extensible for new room types, payment methods, business rules.
#
# Key Design Patterns:
#   • Singleton       – only one HotelManagementSystem instance
#   • Factory/ID Gen  – centralized reservation ID creation
#   • Strategy        – Payment interface for pluggable methods
#   • Mutex Locking   – protect shared data & state transitions
#
# Typical Workflow:
#   1. book_room(guest, room, in_date, out_date)
#   2. check_in(reservation_id)
#   3. check_out(reservation_id, payment)
#   4. cancel_reservation(reservation_id)
#
# Concurrency & Data Integrity:
#   - Global HMS lock for map mutations.
#   - Per-room & per-reservation locks for state changes.
#
# Scalability & Next Steps:
#   - Partitioning or sharding to reduce lock contention.
#   - Swap in a thread-safe database for persistence.
#   - Add features: waitlists, loyalty programs, overbooking rules.

class RoomType(Enum):
    SINGLE = "SINGLE"   # A room with one bed
    DOUBLE = "DOUBLE"   # A room with two beds
    DELUXE = "DELUXE"   # A nicer-than-normal room
    SUITE  = "SUITE"    # A super fancy, multi-room space

class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"  # Nobody is staying yet
    BOOKED    = "BOOKED"     # Someone reserved it, but hasn’t arrived
    OCCUPIED  = "OCCUPIED"   # Guest is checked in and using it

# Now we define what a Room actually is:
class Room:
    def __init__(self, id: str, type: RoomType, price: float):
        self.id     = id            # e.g. "101A" — the room’s label
        self.type   = type          # one of the RoomType values above
        self.price  = price         # cost per night
        self.status = RoomStatus.AVAILABLE  # start out empty
        from threading import Lock
        self.lock   = Lock()        # a little “mutex” so two people can’t book at once

    def book(self):
        with self.lock:             # grab the lock so nobody else can change status now
            if self.status == RoomStatus.AVAILABLE:
                self.status = RoomStatus.BOOKED  # flip from “free” → “reserved”
            else:
                # if it wasn’t free, complain loudly
                raise ValueError("Room is not available for booking.")

    def check_in(self):
        with self.lock:
            if self.status == RoomStatus.BOOKED:
                self.status = RoomStatus.OCCUPIED  # flip from “reserved” → “in use”
            else:
                raise ValueError("Room is not booked.")

    def check_out(self):
        with self.lock:
            if self.status == RoomStatus.OCCUPIED:
                self.status = RoomStatus.AVAILABLE  # flip from “in use” → “free”
            else:
                raise ValueError("Room is not occupied.")


class Guest:
    def __init__(self, guest_id: str, name: str, email: str, phone_number: str):
        self._id           = guest_id     # internal storage of the guest’s ID
        self._name         = name         # guest’s name
        self._email        = email        # guest’s email
        self._phone_number = phone_number # guest’s phone

    @property
    def id(self) -> str:
        return self._id      # let other code ask guest.id safely

    @property
    def name(self) -> str:
        return self._name    # let other code ask guest.name

    @property
    def email(self) -> str:
        return self._email   # let other code ask guest.email

    @property
    def phone_number(self) -> str:
        return self._phone_number  # let other code ask guest.phone_number


class ReservationStatus(Enum):
    CONFIRMED = "CONFIRMED"  # reservation is active
    CANCELLED = "CANCELLED"  # reservation was cancelled

class Reservation:
    def __init__(self, id: str, guest: Guest, room: Room, check_in_date: date, check_out_date: date):
        self.id            = id            # e.g. "RES4F7A1C2"
        self.guest         = guest         # which Guest object
        self.room          = room          # which Room object
        self.check_in_date = check_in_date # date they arrive
        self.check_out_date= check_out_date# date they leave
        self.status        = ReservationStatus.CONFIRMED  # starts confirmed
        from threading import Lock
        self.lock          = Lock()        # to prevent two cancellations at once

    def cancel(self):
        with self.lock:
            if self.status == ReservationStatus.CONFIRMED:
                self.status = ReservationStatus.CANCELLED
                # making them leave immediately frees the room
                self.room.check_out()
            else:
                raise ValueError("Reservation is not confirmed.")


from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass  # abstract: subclasses must fill this in

class CreditCardPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        # pretend to talk to a credit card gateway
        return True  # always succeeds for now

class CashPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        # pretend to collect cash
        return True  # always succeeds for now


from threading import Lock
from typing import Dict, Optional
import uuid

# The big front-desk brain for the entire hotel:
class HotelManagementSystem:
    _instance = None   # will hold the one-and-only HMS object

    def __new__(cls):
        if cls._instance is None:
            cls._instance           = super().__new__(cls)
            cls._instance.guests       = {}  # guest_id -> Guest
            cls._instance.rooms        = {}  # room_id  -> Room
            cls._instance.reservations = {}  # res_id   -> Reservation
            cls._instance.lock         = Lock()  # to guard any operation
        return cls._instance

    def add_guest(self, guest: Guest):
        self.guests[guest.id] = guest  # register this guest by their ID

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        return self.guests.get(guest_id)  # return guest or None

    def add_room(self, room: Room):
        self.rooms[room.id] = room  # register this room

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def book_room(self, guest: Guest, room: Room, check_in_date: date, check_out_date: date) -> Optional[Reservation]:
        with self.lock:
            if room.status == RoomStatus.AVAILABLE:
                room.book()  # flip room to BOOKED
                reservation_id = self._generate_reservation_id()
                reservation = Reservation(reservation_id, guest, room, check_in_date, check_out_date)
                self.reservations[reservation_id] = reservation
                return reservation  # give back the new reservation
            return None  # couldn’t book, room was busy

    def cancel_reservation(self, reservation_id: str):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation:
                reservation.cancel()             # mark it CANCELLED + free the room
                del self.reservations[reservation_id]  # forget that reservation

    def check_in(self, reservation_id: str):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            # only allow if it’s still CONFIRMED
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                reservation.room.check_in()  # flip room to OCCUPIED
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def check_out(self, reservation_id: str, payment: Payment):
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                room   = reservation.room
                nights = (reservation.check_out_date - reservation.check_in_date).days
                amount = room.price * nights  # calculate total cost
                if payment.process_payment(amount):
                    room.check_out()       # flip room to AVAILABLE
                    del self.reservations[reservation_id]  # remove the finished stay
                else:
                    raise ValueError("Payment failed.")
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def _generate_reservation_id(self) -> str:
        # make a random 8-character hex string prefixed with "RES"
        return f"RES{uuid.uuid4().hex[:8].upper()}"
