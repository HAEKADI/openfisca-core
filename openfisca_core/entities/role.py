from openfisca_core.commons import Rolifiable


class Role(Rolifiable):

    def __init__(self, description, entity):
        self.entity = entity
        self.key = description['key']
        self.label = description.get('label')
        self.plural = description.get('plural')
        self.doc = description.get('doc', "")
        self.max = description.get('max')
        self.subroles = None

    def __repr__(self):
        return "Role({})".format(self.key)
