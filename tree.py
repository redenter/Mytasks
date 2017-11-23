class Tree:

    def __init__(self, id, parent=None, prop=None):
        self.parent = parent
        self.prop = prop if prop is not None else {}
        self.id = id
        self.children = []

    def insert(self, child, parentId=None):
        parent = self.find(parentId) 
       # if parent is not None:
       #     print("insert: id"+str(id) +"parentId:" + str(parent.id))
        child.parent = parent

        if parent is None:
            self.children.append(child)
        else:
            parent.children.append(child)

    # does a simple search as the insert does 
    # is a straightforward addition to the tree
    def find(self, id=None):
        if id is None:
            return None

        t = self
        if t.id == id:
            return t
        if t.children is None or t.children==[]:
            return None

        for ch in self.children:
            t = ch.find(id)
            if t is not None:
                return t

    def display(self, tr=None):
        if tr is None:
            t = self
        else:
            t = tr

        print(t.id)
        if t.prop is not None or t.prop != {}:
            for key, value in t.prop.items():
                print(str(key) + ":" + str(value))

        for ch in t.children:
            t.display(ch)


    # deletes the entire subtree associated with the id.
    # use carefully
    def delete(self, id):
        if self.id == id:
            return
        t = self.find(id)
        parent = t.parent
        parent.children.remove(t)

