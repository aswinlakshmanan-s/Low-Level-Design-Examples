from typing import List, Dict
from enum import Enum
import uuid
from threading import Lock

# Enum for votes
class VoteType(Enum):
    UPVOTE = 1
    DOWNVOTE = -1

# Comment class
class Comment:
    def __init__(self, user_id: str, content: str):
        self.comment_id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content

# Answer class
class Answer:
    def __init__(self, user_id: str, content: str):
        self.answer_id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content
        self.votes: int = 0
        self.comments: List[Comment] = []

    def vote(self, vote_type: VoteType):
        self.votes += vote_type.value

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

# Question class
class Question:
    def __init__(self, user_id: str, title: str, description: str, tags: List[str]):
        self.question_id = str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.description = description
        self.tags = tags
        self.votes: int = 0
        self.answers: List[Answer] = []
        self.comments: List[Comment] = []

    def vote(self, vote_type: VoteType):
        self.votes += vote_type.value

    def add_answer(self, answer: Answer):
        self.answers.append(answer)

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

# User class
class User:
    def __init__(self, name: str):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.reputation: int = 0
        self.questions: List[str] = []
        self.answers: List[str] = []

    def update_reputation(self, delta: int):
        self.reputation += delta

# Main StackOverflow System
class StackOverflowSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.questions: Dict[str, Question] = {}
        self.lock = Lock()

    def register_user(self, name: str) -> User:
        user = User(name)
        self.users[user.user_id] = user
        return user

    def post_question(self, user_id: str, title: str, desc: str, tags: List[str]) -> Question:
        question = Question(user_id, title, desc, tags)
        self.questions[question.question_id] = question
        self.users[user_id].questions.append(question.question_id)
        return question

    def post_answer(self, user_id: str, question_id: str, content: str) -> Answer:
        answer = Answer(user_id, content)
        self.questions[question_id].add_answer(answer)
        self.users[user_id].answers.append(answer.answer_id)
        return answer

    def vote_question(self, question_id: str, vote_type: VoteType):
        with self.lock:
            self.questions[question_id].vote(vote_type)

    def vote_answer(self, question_id: str, answer_id: str, vote_type: VoteType):
        with self.lock:
            for ans in self.questions[question_id].answers:
                if ans.answer_id == answer_id:
                    ans.vote(vote_type)
                    break

    def search_by_tag(self, tag: str) -> List[Question]:
        return [q for q in self.questions.values() if tag in q.tags]

    def search_by_keyword(self, keyword: str) -> List[Question]:
        return [q for q in self.questions.values() if keyword.lower() in q.title.lower()]

    def show_question_details(self, question_id: str):
        q = self.questions[question_id]
        print(f"Title: {q.title}\nDescription: {q.description}\nTags: {q.tags}\nVotes: {q.votes}")
        for a in q.answers:
            print(f"\nAnswer by User {a.user_id}: {a.content}\nVotes: {a.votes}")
