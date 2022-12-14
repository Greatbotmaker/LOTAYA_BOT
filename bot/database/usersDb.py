from .mongoDb import MongoDb
from ..config import Config 

class UsersDb(MongoDb):
    def __init__(self):
        super().__init__()
        self.col = self.get_collection("users")
        self.grp = self.db.groups

        

    def new_user_data(self):
        return dict(
            blocked=False,
            last_broadcast_id=0,
            broadcast_info={},
            last_broadcast_msg_id=0,
            pending_broadcast="",
            ban_status=dict(is_banned=False, ban_reason=""),
        )
    
    def new_group(self, id, title, username):
        return dict(
            id = id,
            title = title,
            username = username,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    async def handle_user(self, user_id: int, name: str):
        user = await self.col.update_one(
            {"_id": user_id},
            {"$set": {"name": name}, "$setOnInsert": self.new_user_data()},
            upsert=True,
        )  # type: ignore
        if user.upserted_id:
            return True
        return False

    async def bulk_write(self, data):
        return await self.col.bulk_write(data)  # type: ignore

    async def update_settings(self, user_id, settings):
        return await self.col.update_one({"_id": user_id}, {"$set": settings}, upsert=True)  # type: ignore

    async def total_users_count(self):
        count = await self.col.count_documents({})  # type: ignore
        return count

    async def get_all_users(self):
        return self.col.find({"blocked": False})  # type: ignore

    async def get_pending_users(self, bc_id: int):
        query_filter = {"last_broadcast_id": {"$lt": bc_id}, "blocked": False}
        return self.col.find(query_filter)  # type: ignore

    async def ban_user(self, user_id: int, ban_reason: str = "No Reason"):
        ban_status = dict(is_banned=True, ban_reason=ban_reason)
        await self.col.update_one({"_id": user_id}, {"$set": {"ban_status": ban_status}})  # type: ignore

    async def remove_ban(self, user_id: int):
        ban_status = dict(is_banned=False, ban_reason="")
        await self.col.update_one({"_id": id}, {"$set": {"ban_status": ban_status}})  # type: ignore

    async def get_ban_status(self, user_id: int):
        default = dict(is_banned=False, ban_reason="")
        user = await self.col.find_one({"_id": user_id})  # type: ignore
        if not user:
            return default
        return user.get("ban_status", default)

    async def get_banned_users(self):
        users = self.col.find({"ban_status.is_banned": True})  # type: ignore
        b_users = [user["_id"] async for user in users]
        return b_users

    async def delete_user(self, user_id: int):
        await self.col.delete_many({"_id": int(user_id)})  # type: ignore

    async def update_blocked(self, user_id: int, is_blocked: bool):
        await self.col.update_one({"_id": user_id}, {"$set": {"blocked": is_blocked}})  # type: ignore

    async def add_to_pending(self, user_id: int, msg_id: int, info: dict = {}):
        await self.col.update_one(
            {"_id": user_id}, {"$set": {"pending_broadcast": msg_id, "broadcast_info": info}}
        )  # type: ignore

    async def remove_pending(self, user_id: int):
        await self.col.update_one(
            {"_id": user_id}, {"$set": {"pending_broadcast": "", "broadcast_info": {}}}
        )  # type: ignore

    async def broadcast_id(self, user_id: int, broadcast_id: int):
        await self.col.update_one({"_id": user_id}, {"$set": {"last_broadcast_id": broadcast_id}})  # type: ignore

    async def update_broadcast_msg(self, user_id: int, msg_id: int):
        await self.col.update_one({"_id": user_id}, {"$set": {"last_broadcast_msg_id": msg_id}})  # type: ignore
        
        
        
    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    


    async def add_chat(self, chat, title, username):
        chat = self.new_group(chat, title, username)
        await self.grp.insert_one(chat)
    

    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    

    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    


    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})
    
    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']
    

usersDB = UsersDb()

