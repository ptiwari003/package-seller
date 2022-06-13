from django.shortcuts import render


class Node:
    def __init__(self, value, next_node=None, prev_node=None):
        self.value = value
        self.next = next_node
        self.prev = prev_node

    def __str__(self):
        return str(self.value)
    

class LinkedList:
    def __init__(self, values = None) -> None:
        self.head = None
        self.tail = None
        
        if values :
            self._add_multiple_values(values)
            
    
    def _add_multiple_values(self, values):
        for value in values:
            self._add_node_(value)
    

    def _add_node_(self, value):
        if self.head is None:
            self.tail = self.head = Node(value)
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next
        
        return self.tail    
    

    def _add_node_as_head_(self, value):
        if self.head is None:
            self.head = self.tail = Node(value)
        else:
            self.head = None(value, self.head)
        return self.head
    
    def __str__(self) -> str:
        return '--> '.join([str(node) for node in self])
    
    
    
    def __len__(self):
        count = 0
        node = self.head
        
        while self.head:
            count += 1
            node = node.next
        
        return count
    
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
            
    
    def values(self):
        return [node.value for node in self]
    
    
class DLL(LinkedList):
    
    def _add_node_(self, value):
        if self.head is None:
            self.tail = self.head = Node(value)
        else:
            self.tail.next = Node(value, None, self.tail)
            self.tail = self.tail.next
            
        return self    
            





def _render_agent_view(request):
    return render(request, 'base.html', {})