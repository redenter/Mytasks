from __future__ import print_function
import datetime

def deb(stmt):
    log = open('log.txt', 'a')
    print(str(datetime.datetime.now()) + ':          ' + stmt, file = log)


class Tree:

    def __init__(self, id, parent=None, prop=None):
        self.parent = self if parent is None else parent
        self.prop = prop if prop is not None else {}
        self.id = id
        self.children = []

    def insert(self, child, parentId=None):
        deb('tree.insert: count of children= ' + str(len(self.children)))
        parent = self.find(parentId) 
       # if parent is not None:
       #     print("insert: id"+str(id) +"parentId:" + str(parent.id))

        # could potentially refactor here. Parent can no longer be None
        if parent is None or parent==self:
            child.parent = self
            self.children.append(child)
        else:
            child.parent = parent
            parent.children.append(child)
        #if parent.parent is not None:
        #    deb('tree.insert:: parent is ' + parent.id + ':grandpa:' + parent.parent.id)
        #deb('tree.insert:: child is ' + child.id + ':parent:' + child.parent.id)

    # does a simple search as the insert does 
    # is a straightforward addition to the tree
    def find(self, id=None):
        if id is None:
            return None

        t = self
        deb('tree.find: searching :'+str(self.id))

        if t.id == id:
            deb('tree.find found id:' + str(id))
            return t

        if t.children is None or t.children==[]:
            deb('tree.find: no children for :'+str(t.id))
            return None

        for ch in self.children:
            t = ch.find(id)
            if t is not None:
                deb('tree.find found id:' + str(t.id))
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

    # append the prop to all subtree's props
    def addPropToSubtree(self, id, prop):
        t = self.find(id)
        t.prop.update(prop)

        for ch in t.children:
            ch.addPropToSubtree(ch.id, prop)


    # deletes the entire subtree associated with the id.
    # use carefully
    def delete(self, id):
        if self.id == id:
            return
        deb('tree.delete: trying to find:'+str(id))
        t = self.find(id)
        deb('tree.delete: t.id = '+str(t.id))
        parent = t.parent
        parent.children.remove(t)

