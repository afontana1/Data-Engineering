[![License](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![UnitTest and MyPy CI](https://github.com/mbrav/design_patterns_python/actions/workflows/unittest.yml/badge.svg?branch=main)](https://github.com/mbrav/design_patterns_python/actions/workflows/unittest.yml)
[![wakatime](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/2133ea0a-1269-478f-99d6-e6645f69c2ff.svg)](https://wakatime.com/badge/user/54ad05ce-f39b-4fa3-9f2a-6fe4b1c53ba4/project/2133ea0a-1269-478f-99d6-e6645f69c2ff)
[![tokei](https://tokei.rs/b1/github/mbrav/design_patterns_python?category=lines)](https://tokei.rs/b1/github/mbrav/design_patterns_python)


# Design Patterns

A collection of design patterns in Python

## Classification of Design Patterns

Design Patterns are categorized mainly into three categories: *Creational Design Pattern*, *Structural Design Pattern*, and *Behavioral Design Pattern*. These are differed from each other on the basis of their level of detail, complexity, and scale of applicability to the entire system being design.

There are also two types of patterns - *idioms* and *architectural* patterns.

### 1. Creational Design Patterns

As the name suggests, creation design patters provide objects or a creation mechanism that enhance the flexibilities and reusability of existing code. They reduce the dependency and controlling how the user interacts with our class so the user would not have to deal with their construction. Below are the various creational design patterns:

- **Factory Method** ([creational/factory.py](design_patterns/creational/factory.py) - Defines an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses. The pattern has creational purpose and applies to classes where deals with relationships through inheritence ie. they are static-fixed at compile time. In contrast to *Abstract Factory*, Factory Method contain method to produce only one type of product.

- **Abstract Factory** ([creational/abstract_factory.py](design_patterns/creational/abstract_factory.py)) - Abstract factory pattern has creational purpose and provides an interface for creating families of related or dependent objects without specifying their concrete classes. Pattern applies to object and deal with object relationships, which are more dynamic. In contrast to *Factory Method*, Abstract Factory pattern produces family of types that are related, ie. it has more than one method of types it produces.

- **Builder** ([creational/builder.py](design_patterns/creational/builder.py)) - A generative design pattern, which allows you to copy objects without going into details of their implementation. It decouples the creation of a complex object and its representation, so that the same process can be reused to build objects from the same family. This is useful when you must separate the specification of an object from its actual representation (generally for abstraction).
  
- **Prototype** ([creational/prototype.py](design_patterns/creational/prototype.py)) - This patterns aims to reduce the number of classes required by an application. Instead of relying on subclasses it creates objects by copying a prototypical instance at run-time. This is useful as it makes it easier to derive new kinds of objects, when instances of the class have only a few different combinations of state, and when instantiation is expensive.

- **Singleton**([creational/singleton.py](design_patterns/creational/singleton.py)) - Singleton design pattern make sure that only one instance of an object is created.

### 2. Structural Design Patterns

Structural Design Patterns are mainly responsible for assembling objects and classes into a larger structure allowing these structures to be flexible and efficient. They essential for enhancing the readability and maintainability of our code. They also ensure that functionalities are properly separated and encapsulated, as well as reducing the number of interfaces between interdependent objects.

- **Adapter** ([structural/adapter.py](design_patterns/structural/adapter.py)) - The Adapter pattern provides a different interface for a class. We can think about it as a cable adapter that allows you to charge a phone somewhere that has outlets in a different shape. Following this idea, the Adapter pattern is useful to integrate classes that couldn't be integrated due to their incompatible interfaces.

- **Bridge** ([structural/bridge.py](design_patterns/structural/bridge.py)) - Decouples an abstraction from its implementation.

- **Composite** ([structural/composite.py](design_patterns/structural/composite.py)) - The composite pattern describes a group of objects that is treated the same way as a single instance of the same type of object. The intent of a composite is to "compose" objects into tree structures to represent part-whole hierarchies. Implementing the composite pattern lets clients treat individual objects and compositions uniformly.

- **Decorator** ([structural/decorator.py](design_patterns/structural/decorator.py)) - The Decorator pattern is used to dynamically add a new feature to an object without changing its implementation. It differs from inheritance because the new feature is added only to that particular object, not to the entire subclass.

- **Facade** ([structural/facade.py](design_patterns/structural/facade.py)) - The Facade pattern is a way to provide a simpler unified interface to a more complex system. It provides an easier way to access functions of the underlying system by providing a single entry point. This kind of abstraction is seen in many real life situations. For example, we can turn on a computer by just pressing a button, but in fact there are many procedures and operations done when that happens (e.g., loading programs from disk to memory). In this case, the button serves as an unified interface to all the underlying procedures to turn on a computer.

- **Flyweight** ([structural/flyweight.py](design_patterns/structural/flyweight.py)) - This pattern aims to minimise the number of objects that are needed by a program at run-time. A Flyweight is an object shared by multiple contexts, and is indistinguishable from an object that is not shared. The state of a Flyweight should not be affected by it's context, this is known as its intrinsic state. The decoupling of the objects state from the object's context, allows the Flyweight to be shared.

- **Proxy** ([structural/proxy.py](design_patterns/structural/proxy.py)) - Proxy is used in places where you want to add functionality to a class without changing its interface. The main class is called `Real Subject`. A client should use the proxy or the real subject without any code change, so both must have the same interface. Logging and controlling access to the real subject are some of the proxy pattern usages.

### 3. Behavioral Design Patterns (TODO)

Behavior Design Patterns are responsible for how one class communicates with others.

*Chain of Responsibility* - It representatives the command to a chain of processing object.

- **Command** ([behavioral/command.py](design_patterns/behavioral/command.py)) - It generates the objects which encapsulate actions of parameters.

- **Interpreter** ([behavioral/interpretor.py](design_patterns/behavioral/interpretor.py)) - It implements a specialized language.

- **Iterator** ([behavioral/iterator.py](design_patterns/behavioral/iterator.py)) - It accesses all the element of an object sequentially without violating its underlying representation.

- **Mediator** ([behavioral/mediator.py](design_patterns/behavioral/mediator.py)) - It provides the loose coupling between classes by being the only class that has detailed knowledge of their existing methods.

- **Memento** ([behavioral/memento.py](design_patterns/behavioral/memento.py)) - It restores an object in the previous state.

- **Observer** ([behavioral/observer.py](design_patterns/behavioral/observer.py)) - It allows a number of observer objects to see an event.

- **State** ([behavioral/state.py](design_patterns/behavioral/state.py)) - It allows an object to modify its behavior when it's internal states changes.

- **Strategy** ([behavioral/strategy.py](design_patterns/behavioral/strategy.py)) - It provides one of the families of algorithm to be selected at the runtime.

- **Template Method** ([behavioral/template.py](design_patterns/behavioral/template.py)) - It allows the subclasses to provide concrete behavior. It also defines the skeleton of an algorithm as an abstract class.

- **Visitor** ([behavioral/visitor.py](design_patterns/behavioral/visitor.py)) - It separates an algorithm from an object structure by moving the hierarchy of methods into one object.

## Application Structure Patterns

- **Layered** -  Layered is a classic pattern, but usually leads to monolit drawbacks where it is hard to separate different logic into separate parts.

- **Microkernel** - The microkernel consists of a "Core" which is augmented by extension parts. The core itself is independent from its extensions.

- **Command Query Responsibility Segregation (CQRS)** - Reduces the amount of complex queries and allows for creation of scenario-specific queries, but requires synchronization. The model is separated into read logic and write logic.

- **Event sourcing** - Stores everything in the current state. All events are things that happen in the past.  The advantage is that it is possible to trace, audit and replay events. There is no need to update database. The disadvantage, is that it becomes hard to identify which events are new, and which ones are replays, which makes it non-trivial.

## Additional resources

- [python-patterns.guide](https://python-patterns.guide/)
- [faif/python-patterns](https://github.com/faif/python-patterns)
