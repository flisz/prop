from .base import Model
from project.db import db


class Item(Model):
    """
    Base Model Provides:
        pk (primary key)
        created_at (creation date)
    """
    summary = db.Column(db.String(), nullable=False)
    details = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    list_pk = db.Column(db.Integer, db.ForeignKey('list.pk'), nullable=False)

    def __repr__(self):
        return f'<Item {self.pk} details: {self.details} summary: {self.summary} active: {self.active} list_pk: {self.list_pk}>'

    @property
    def dictionary(self):
        return {
            'pk': self.pk,
            'created_at': self.created_at,
            'summary': self.summary,
            'details': self.details,
            'active': self.active,
            'list_pk': self.list_pk
        }
