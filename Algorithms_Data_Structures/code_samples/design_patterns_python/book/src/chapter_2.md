# Chapter 2: Creational Design Patterns

As the name suggests, creation design patters provide objects or a creation mechanism that enhance the flexibilities and reusability of existing code. They reduce the dependency and controlling how the user interacts with our class so the user would not have to deal with their construction. Below are the various creational design patterns:

- **Factory Method** ([creational/factory.py](../design_patterns/creational/factory.py)) - Defines an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses. The pattern has creational purpose and applies to classes where deals with relationships through inheritence ie. they are static-fixed at compile time. In contrast to *Abstract Factory*, Factory Method contain method to produce only one type of product.

- **Abstract Factory** ([creational/abstract_factory.py](design_patterns/creational/abstract_factory.py)) - Abstract factory pattern has creational purpose and provides an interface for creating families of related or dependent objects without specifying their concrete classes. Pattern applies to object and deal with object relationships, which are more dynamic. In contrast to *Factory Method*, Abstract Factory pattern produces family of types that are related, ie. it has more than one method of types it produces.

- **Builder** ([creational/builder.py](design_patterns/creational/builder.py)) - A generative design pattern, which allows you to copy objects without going into details of their implementation. It decouples the creation of a complex object and its representation, so that the same process can be reused to build objects from the same family. This is useful when you must separate the specification of an object from its actual representation (generally for abstraction).
  
- **Prototype** ([creational/prototype.py](design_patterns/creational/prototype.py)) - This patterns aims to reduce the number of classes required by an application. Instead of relying on subclasses it creates objects by copying a prototypical instance at run-time. This is useful as it makes it easier to derive new kinds of objects, when instances of the class have only a few different combinations of state, and when instantiation is expensive.

- **Singleton**([creational/singleton.py](design_patterns/creational/singleton.py)) - Singleton design pattern make sure that only one instance of an object is created.
