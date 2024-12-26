
# Chord Class

class Chord:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __repr__(self):
        return f"Chord(name={self.name}, notes={self.notes})"
    
    def get_notes(self):
        return self.notes