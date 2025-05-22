import reflex as rx

class AuthState(rx.State):
    auth_token: str = rx.Cookie(name="auth_token", max_age=15*24*60*60)  #15天有效期

    def is_authenticated(self):
        return self.auth_token is not None
    
    def get_user_id(self):
        pass