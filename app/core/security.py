from hashlib import sha512

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)

    @staticmethod
    def formulate_key(values: list):
        return pwd_context.hash("".join(values))

    @staticmethod
    def verify_key(values: list, secret_key: str):
        return pwd_context.verify("".join(values), secret_key)

    @staticmethod
    def sha512_hash(value: str):
        return sha512(value.encode("utf-8")).hexdigest()
