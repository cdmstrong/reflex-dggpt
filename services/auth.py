import reflex as rx

class AuthState(rx.State):
    auth_token: str 
    id_token_json: str = rx.LocalStorage()
    
    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)

    @rx.event
    def check_auth(self):
        # 这里检查 cookie 或 token 是否有效，并设置 authenticated
        self.authenticated = self.is_authenticated()  # 你需要实现 check_auth 函数
        if not self.authenticated:
            return rx.redirect("/login")

    def is_authenticated(self):
        if self.auth_token is None:
            return False
        # 解密cookie
