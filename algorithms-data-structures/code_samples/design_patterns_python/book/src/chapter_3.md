# Chapter 3: Structural Design Patterns

Structural Design Patterns are mainly responsible for assembling objects and classes into a larger structure allowing these structures to be flexible and efficient. They essential for enhancing the readability and maintainability of our code. They also ensure that functionalities are properly separated and encapsulated, as well as reducing the number of interfaces between interdependent objects.

- **Adapter** ([structural/adapter.py](design_patterns/structural/adapter.py)) - The Adapter pattern provides a different interface for a class. We can think about it as a cable adapter that allows you to charge a phone somewhere that has outlets in a different shape. Following this idea, the Adapter pattern is useful to integrate classes that couldn't be integrated due to their incompatible interfaces.

- **Bridge** ([structural/bridge.py](design_patterns/structural/bridge.py)) - Decouples an abstraction from its implementation.

- **Composite** ([structural/composite.py](design_patterns/structural/composite.py)) - The composite pattern describes a group of objects that is treated the same way as a single instance of the same type of object. The intent of a composite is to "compose" objects into tree structures to represent part-whole hierarchies. Implementing the composite pattern lets clients treat individual objects and compositions uniformly.

- **Decorator** ([structural/decorator.py](design_patterns/structural/decorator.py)) - The Decorator pattern is used to dynamically add a new feature to an object without changing its implementation. It differs from inheritance because the new feature is added only to that particular object, not to the entire subclass.

- **Facade** ([structural/facade.py](design_patterns/structural/facade.py)) - The Facade pattern is a way to provide a simpler unified interface to a more complex system. It provides an easier way to access functions of the underlying system by providing a single entry point. This kind of abstraction is seen in many real life situations. For example, we can turn on a computer by just pressing a button, but in fact there are many procedures and operations done when that happens (e.g., loading programs from disk to memory). In this case, the button serves as an unified interface to all the underlying procedures to turn on a computer.

- **Flyweight** ([structural/flyweight.py](design_patterns/structural/flyweight.py)) - This pattern aims to minimise the number of objects that are needed by a program at run-time. A Flyweight is an object shared by multiple contexts, and is indistinguishable from an object that is not shared. The state of a Flyweight should not be affected by it's context, this is known as its intrinsic state. The decoupling of the objects state from the object's context, allows the Flyweight to be shared.

- **Proxy** ([structural/proxy.py](design_patterns/structural/proxy.py)) - Proxy is used in places where you want to add functionality to a class without changing its interface. The main class is called `Real Subject`. A client should use the proxy or the real subject without any code change, so both must have the same interface. Logging and controlling access to the real subject are some of the proxy pattern usages.
