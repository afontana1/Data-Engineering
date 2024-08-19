from abc import ABC, abstractmethod

class Customer:
    """Customer object"""
    def __init__(self,age):
        self.__age = age
        
    def get_age(self):
        return self.__age
    
class IChannel(ABC):
    
    @abstractmethod
    def provide_broadcast(self):
        """broadcasting"""
        
class Channel(IChannel):
    
    def provide_broadcast(self):
        print("Broadcast started...")
        
class ProxyChannel(IChannel):
    
    def __init__(self,customer: Customer):
        self.customer = customer
        self.channel = Channel()
        
    def provide_broadcast(self):
        customer_age = self.customer.get_age()
        if customer_age > 18:
            self.channel.provide_broadcast()
            print("this service is registered for billing.")
        else:
            print("sorry, this service is not allowed for the customers under the age of 18.")