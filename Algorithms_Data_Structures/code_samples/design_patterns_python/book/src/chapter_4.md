# Chapter 4: Behavioral Design Patterns

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
