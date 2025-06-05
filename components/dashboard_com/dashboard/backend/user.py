from sqlalchemy import update
from Model.User import User
from sqlmodel import select
import reflex as rx


class UserManagerState(rx.State):
    user_list: list[User] = []

    def get_data(self):
        with rx.session() as session:
            res = session.exec(select(User)).all()
            self.user_list = res


    @rx.event
    def upgrade_to_admin(self, user_id: int):
        with rx.session() as session:
            user = update(User).where(User.user_id == user_id).values(is_admin=True)
            session.exec(user)
            session.commit()
            self.get_data()
            rx.toast.success("升级成功")

    @rx.event
    def downgrade_to_user(self, user_id: int):
        with rx.session() as session:
            user = update(User).where(User.user_id == user_id).values(is_admin=False)
            session.exec(user)
            session.commit()
            self.get_data()
            rx.toast.success("降级成功")
