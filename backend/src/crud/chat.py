from sqlalchemy.orm import aliased
from pydantic import BaseModel
# from src.crud.database import getdb
from src.crud.models import User, Message


class Chat(BaseModel):
    pass


# async def get_chat(patient: int):
#     async with getdb() as session:
#         sender_user = aliased(User)
#         receiver_user = aliased(User)
#
#         # Query to get messages between a specific sender and receiver
#         result = (
#             session.query(Message, sender_user, receiver_user)
#             .join(sender_user, Message.sender == sender_user.id)
#             .join(receiver_user, Message.receiver == receiver_user.id)
#             .filter(sender_user.id == patient)
#             .filter(receiver_user.id == patient)
#             .all()
#         )