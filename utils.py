from sqlalchemy.orm import Session, class_mapper

def serialize_object(model):
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)