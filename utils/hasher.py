from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


class Hasher:
    @staticmethod
    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
