import mongoengine as me

class User(me.Document):
    meta = {
        'collection': 'users'
    }
    # firstname = me.StringField()
    # lastname = me.StringField()
    # email = me.StringField()

    username = me.StringField()
    password = me.StringField()
    
    status = me.BooleanField()
    
    def to_json(self):
        return {"firstname": self.firstname,
                "lastname": self.lastname}
    