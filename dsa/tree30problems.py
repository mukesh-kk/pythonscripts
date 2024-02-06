# Tree

class Node:
    def __init__(self,data=0,left=None,right=None):
        self.left=left
        self.data=data
        self.right=right
class Tree:
    def __init__(self) -> None:
        self.head= Node()
    def get_head(self):
        return self.head
    def add_child(self, child):
        self.left=child
        self.right=child
    def print(self,head):
        if(head is not None):
            head=head.left
            print(head.data)
            head=head.right
