from datetime import datetime, timedelta
from threading import Lock
from typing import List, Dict

class Meeting:
    def __init__(self, title: str, start_time: datetime, end_time: datetime, attendees: List[str]):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.attendees = attendees

class MeetingRoom:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.bookings: List[Meeting] = []
        self.lock = Lock()

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        for meeting in self.bookings:
            if not (end_time <= meeting.start_time or start_time >= meeting.end_time):
                return False
        return True

    def book_meeting(self, meeting: Meeting) -> bool:
        with self.lock:
            if self.is_available(meeting.start_time, meeting.end_time):
                self.bookings.append(meeting)
                print(f"Meeting '{meeting.title}' booked in room {self.room_id}.")
                return True
            print(f"Room {self.room_id} is not available for meeting '{meeting.title}'.")
            return False

class MeetingScheduler:
    def __init__(self, rooms: List[MeetingRoom]):
        self.rooms = rooms
        self.user_meetings: Dict[str, List[Meeting]] = {}
        self.lock = Lock()

    def is_user_available(self, user: str, start_time: datetime, end_time: datetime) -> bool:
        for meeting in self.user_meetings.get(user, []):
            if not (end_time <= meeting.start_time or start_time >= meeting.end_time):
                return False
        return True

    def schedule_meeting(self, title: str, start_time: datetime, end_time: datetime, attendees: List[str]) -> bool:
        with self.lock:
            for room in self.rooms:
                if room.is_available(start_time, end_time):
                    if all(self.is_user_available(user, start_time, end_time) for user in attendees):
                        meeting = Meeting(title, start_time, end_time, attendees)
                        if room.book_meeting(meeting):
                            for user in attendees:
                                if user not in self.user_meetings:
                                    self.user_meetings[user] = []
                                self.user_meetings[user].append(meeting)
                            return True
                    else:
                        print("One or more users are not available for the selected time.")
                        return False
            print("No rooms are available for the selected time.")
            return False

# Sample usage
if __name__ == "__main__":
    room1 = MeetingRoom("RoomA")
    room2 = MeetingRoom("RoomB")
    scheduler = MeetingScheduler([room1, room2])

    now = datetime.now()
    scheduler.schedule_meeting("Design Discussion", now + timedelta(hours=1), now + timedelta(hours=2), ["Alice", "Bob"])
    scheduler.schedule_meeting("Code Review", now + timedelta(hours=1, minutes=30), now + timedelta(hours=2, minutes=30), ["Bob", "Charlie"])
