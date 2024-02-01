
#Linked List
class Node:
    """
    Parameters:
    - data (int)
    Returns:
    dict: new Node
    """
    def __init__(self,data):
        self.data = data
        self.next=None

class LinkedList:
    def __init__(self):
        self.head=None
    def is_empty(self):
        return self.head is  None
    def append(self,data):

        p=self.head
        t= Node(data)
        if p is None:
            self.head = t
            return  self.head
        while p.next is not None:
            p=p.next
       
        p.next=t
        return self.head
    def remove(self,key):
        f=self.head
        s=None
        if f is None:
            return False
        if self.head.data  ==key:
            self.head = self.head.next
            return True
            
        while key != f.data:
            s=f
            f=f.next
        if s is not None:
            s.next= f.next
            return True
             
    def print(self):
        p = self.head
        while p is not None:
            print(f" {p.data}")
            p=p.next


 


if __name__ == '__main__':
    ll= LinkedList()
    ll.append(20)
    ll.append(34)
    ll.append(21)
    ll.append(14)
    ll.remove(14)
    ll.print()