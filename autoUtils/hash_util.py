import hashlib


def md5(text: str):
    """MD5加密"""
    return hashlib.md5(text.encode()).hexdigest()


def sha1(text: str):
    """生成sha1摘要"""
    return hashlib.sha1(text.encode()).hexdigest()


def sha256(text: str):
    """生成SHA256摘要"""
    return hashlib.sha256(text.encode()).hexdigest()


# print(
#     sha256(
#         "f1b1db8a-a5b7-4e5d-ae07-948604f1baa0100002bffe656-957f-42a9-a5aa-58605592d4941697537321658"
#     )
# )
