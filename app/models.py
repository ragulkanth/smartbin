from app import db

class BinStatus(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'binstatus'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    level = db.Column(db.Integer, default = 0)

    def __init__(self, ip):
        """initialize with name."""
        self.ip = ip

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return BinStatus.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<BinStatus: {}>".format(self.ip)
