import mongoengine as me

class User(me.Document):
    meta = {
        'collection': 'users'
    }
    firstname = me.StringField()
    lastname = me.StringField()
    status = me.BooleanField()
    def to_json(self):
        return {"firstname": self.firstname,
                "lastname": self.lastname}
    


class Customer(me.Document):
    meta = {
        'collection': 'customers'
    }
    username = me.StringField()
    name = me.StringField()

    address = me.StringField()
    birthdate = me.DateTimeField()
    email = me.EmailField()

    active = me.EmailField()

    def to_json(self):
        return {"username": self.username,
                "name": self.name}