from datetime import datetime
from enum import Enum
from threading import Lock

# Enumerations
class SeatType(Enum):
    ECONOMY = "Economy"
    BUSINESS = "Business"
    FIRST = "First"

class SeatStatus(Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"

class BookingStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "PayPal"

class PaymentStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"

# Core Classes
class Aircraft:
    def __init__(self, tail_number, model, total_seats):
        self.tail_number = tail_number
        self.model = model
        self.total_seats = total_seats

class Flight:
    def __init__(self, flight_number, source, destination, departure_time, arrival_time, aircraft):
        self.flight_number = flight_number
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft = aircraft
        self.seats = [Seat(f"{i+1}", SeatType.ECONOMY) for i in range(aircraft.total_seats)]

class Seat:
    def __init__(self, seat_number, seat_type):
        self.seat_number = seat_number
        self.seat_type = seat_type
        self.status = SeatStatus.AVAILABLE

class Passenger:
    def __init__(self, passenger_id, name, email, phone):
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone

class Booking:
    def __init__(self, booking_number, flight, passenger, seat, price):
        self.booking_number = booking_number
        self.flight = flight
        self.passenger = passenger
        self.seat = seat
        self.price = price
        self.status = BookingStatus.CONFIRMED

class Payment:
    def __init__(self, payment_id, method, amount):
        self.payment_id = payment_id
        self.method = method
        self.amount = amount
        self.status = PaymentStatus.SUCCESS

# Search
class FlightSearch:
    @staticmethod
    def search_flights(flights, source, destination, date):
        return [f for f in flights if f.source == source and f.destination == destination and f.departure_time.date() == date.date()]

# Managers
class BookingManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.bookings = []
        return cls._instance

    def create_booking(self, flight, passenger, seat_number, price):
        for seat in flight.seats:
            if seat.seat_number == seat_number and seat.status == SeatStatus.AVAILABLE:
                seat.status = SeatStatus.BOOKED
                booking = Booking(len(self.bookings) + 1, flight, passenger, seat, price)
                self.bookings.append(booking)
                return booking
        return None

    def cancel_booking(self, booking):
        booking.status = BookingStatus.CANCELLED
        booking.seat.status = SeatStatus.AVAILABLE

class PaymentProcessor:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def process_payment(self, booking, method):
        payment = Payment(len(booking.flight.seats) + 1, method, booking.price)
        return payment

# Main System
class AirlineManagementSystem:
    def __init__(self):
        self.flights = []
        self.passengers = []
        self.booking_manager = BookingManager()
        self.payment_processor = PaymentProcessor()

    def add_flight(self, flight):
        self.flights.append(flight)

    def register_passenger(self, passenger):
        self.passengers.append(passenger)

    def search_and_book(self, source, destination, date, passenger, seat_number, price, method):
        available_flights = FlightSearch.search_flights(self.flights, source, destination, date)
        if available_flights:
            booking = self.booking_manager.create_booking(available_flights[0], passenger, seat_number, price)
            if booking:
                payment = self.payment_processor.process_payment(booking, method)
                return booking, payment
        return None, None