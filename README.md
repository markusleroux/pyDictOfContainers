# pyDictOfContainers
A dictionary of containers that automates deleting keys when the nested container is empty.

When a key-value pair is added to the dictionary, the value is type-checked against the Container generic class (it must implement a __len__ method).
If it quackes like a duck, a class is created which subclasses type(value). An object of this class is used to store the data from the value, as well
as references to the dictionary and the key. If the newly created object is modified in such a way that its length becomes zero, the key-value pair
are automatically removed from the dictionary.

## Wrapped Value

When a new value is added to the dictionary, a class is created that subclasses the type of the value. This class factory is implemented as a metaclass,
and uses a simple dictionary-based cache when generating new classes. A decorator is used to modify the methods of the subclass during class creation.
This means that the signatures of the method of the new class are modified only once, and that the overhead of modifying these methods is incurred at
class creation.

Critically, **the value is copied when stored in a DictOfContainers.** This is to avoid unexpected behaviours, where modifications to the value outside
of the dictionary context do not use the decorator because they are not aware of the modifications which have been made to the type of the object. While
deletion from the dictionary after modification in any context would be convenient (at the very least for the sake of completeness), I am not aware of
a way of providing such functionality. I have retained the moniker *Wrapped to emphasize that the behaviour of the new value is, in almost all contexts,
identical.
