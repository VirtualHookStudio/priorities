from app.src.aws.dynamodb_access import DynamoDBAccess

class User:
    id: str
    permission: int
    name: str
    email: str
    password: str
    date_birth: str

    def __init__(self, user):
        self.id = user.get('id', '')
        self.permission = user.get('permission', 0)
        self.name = user.get('name', '')
        self.email = user.get('email', '')
        self.password = user.get('password', '')
        self.date_birth = user.get('date_birth', '')

        if 'method' in user and user['method'] == "CREATE":
            dynamodbaccess = DynamoDBAccess()
            
            dynamodbaccess.put_item({
                'id': self.id,
                'permission': self.permission,
                'name': self.name,
                'email': self.email,
                'password': self.password,
                'date_birth': self.date_birth
            })
    
    def get_user(self):
        return {
            'id': self.id,
            'permission': self.permission,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'date_birth': self.date_birth
        }