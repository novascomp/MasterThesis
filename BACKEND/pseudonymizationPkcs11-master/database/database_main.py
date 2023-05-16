def save_to_db(db, mapping):
    db.session.add(mapping)
    db.session.commit()
    db.session.flush()
