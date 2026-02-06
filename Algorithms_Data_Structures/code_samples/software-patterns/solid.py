"""
SOLID Principles in Python — A Detailed, Runnable Example

This single script demonstrates all 5 SOLID principles with one cohesive mini-domain:
"notifications" for an order system.

SOLID stands for:
- S: Single Responsibility Principle (SRP)
- O: Open/Closed Principle (OCP)
- L: Liskov Substitution Principle (LSP)
- I: Interface Segregation Principle (ISP)
- D: Dependency Inversion Principle (DIP)

The goal is not to be “framework-y”, but to show pragmatic, readable Python that makes
each principle obvious.

You can run this file directly:
    python solid_example.py

Design overview:
- Domain objects: Customer, Order
- SRP: Separate responsibilities into focused classes (validation, formatting, sending, etc.)
- OCP: Add new notification channels without changing existing orchestration logic
- LSP: Swap one notifier for another without breaking correctness
- ISP: Small interfaces (protocols) instead of one fat “Notifier” interface
- DIP: High-level orchestration depends on abstractions (protocols), not concrete classes
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable, Optional


# =============================================================================
# Domain Model
# =============================================================================

@dataclass(frozen=True)
class Customer:
    """
    A simple domain object.

    Note:
        This class is intentionally "dumb": it holds data and minimal domain meaning.
        This helps SRP: the object is not responsible for validation, notification, etc.
    """
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


@dataclass(frozen=True)
class Order:
    """
    Another simple domain object.

    SRP note:
        Order does not send notifications, validate customers, or log anything.
        It represents the concept of an order.
    """
    order_id: str
    customer: Customer
    total_usd: float


# =============================================================================
# SOLID: S — Single Responsibility Principle (SRP)
# =============================================================================

class OrderValidator:
    """
    SRP — Single Responsibility Principle

    Principle meaning:
        "A class should have one reason to change."
        In practice: keep each class focused on one job.

    What this class does:
        - Validates Orders
        - Raises ValueError with clear messages when invalid

    What it does NOT do:
        - It does not format messages
        - It does not send messages
        - It does not log
        - It does not decide which channel to use

    Why this is SRP:
        If validation rules change, you change *this* class only.
        You don't touch notification logic, message formatting, etc.
    """

    def validate(self, order: Order) -> None:
        if order.total_usd < 0:
            raise ValueError("Order total cannot be negative.")
        if not order.order_id.strip():
            raise ValueError("Order must have a non-empty order_id.")
        if not order.customer.customer_id.strip():
            raise ValueError("Customer must have a non-empty customer_id.")


class NotificationMessageFactory:
    """
    SRP — Single Responsibility Principle

    Principle meaning recap:
        Keep message creation separate from sending.

    What this class does:
        - Converts domain data into a human-friendly message

    Why:
        If message wording changes, you only update this factory.
        Sending logic stays untouched.
    """

    def order_confirmation(self, order: Order) -> str:
        return (
            f"Hi {order.customer.name}, your order {order.order_id} "
            f"has been confirmed. Total: ${order.total_usd:.2f}."
        )


class SimpleLogger:
    """
    SRP — Single Responsibility Principle

    Logging is a separate concern. This is intentionally minimal.

    In real systems you might use 'logging' module or structured logging.
    The point here is: don't bury logging responsibilities in other classes.
    """

    def info(self, message: str) -> None:
        print(f"[INFO] {message}")

    def warning(self, message: str) -> None:
        print(f"[WARN] {message}")


# =============================================================================
# SOLID: I — Interface Segregation Principle (ISP)
# =============================================================================

@runtime_checkable
class MessageSender(Protocol):
    """
    ISP — Interface Segregation Principle

    Principle meaning:
        "Clients should not be forced to depend on methods they do not use."

    How we apply it:
        Instead of one giant interface like:
            class Notifier:
                def send_email(...)
                def send_sms(...)
                def send_push(...)
                def schedule(...)
                def cancel(...)
                def get_status(...)
        ...we define small role-based interfaces.

    This protocol defines ONE capability: sending a plain text message to a destination.
    Different senders can implement this with different destination semantics.
    """

    def send(self, destination: str, message: str) -> None:
        """
        Send `message` to `destination`.

        Implementations decide what "destination" means:
        - Email sender: destination is an email address
        - SMS sender: destination is a phone number
        - Push sender: destination might be a device token
        """
        ...


@runtime_checkable
class DestinationResolver(Protocol):
    """
    ISP — Another small interface.

    Responsibility:
        Given a Customer, resolve the channel destination (email, phone, token, ...).

    Why this is ISP:
        Some parts of the system only need "resolve destination"
        and should not be forced to implement "send", "format", etc.
    """

    def resolve(self, customer: Customer) -> str:
        """Return the destination string for this channel (or raise ValueError)."""
        ...


# =============================================================================
# Concrete channel pieces (small, composable parts)
# =============================================================================

class EmailDestinationResolver:
    """
    Resolves a customer's email address.

    SRP:
        Only responsible for extracting/validating destination for email channel.
    """

    def resolve(self, customer: Customer) -> str:
        if not customer.email:
            raise ValueError("Customer has no email address.")
        return customer.email


class PhoneDestinationResolver:
    """
    Resolves a customer's phone number.

    SRP:
        Only responsible for extracting/validating destination for SMS channel.
    """

    def resolve(self, customer: Customer) -> str:
        if not customer.phone:
            raise ValueError("Customer has no phone number.")
        return customer.phone


class ConsoleEmailSender:
    """
    A pretend email sender that prints to console.

    This is a stand-in for a real integration (SMTP, SendGrid, SES, etc.)
    """

    def send(self, destination: str, message: str) -> None:
        print(f"[EMAIL to {destination}] {message}")


class ConsoleSmsSender:
    """
    A pretend SMS sender that prints to console.

    Stand-in for Twilio, Nexmo, etc.
    """

    def send(self, destination: str, message: str) -> None:
        print(f"[SMS to {destination}] {message}")


# =============================================================================
# SOLID: O — Open/Closed Principle (OCP)
# =============================================================================

class NotificationChannel(Protocol):
    """
    OCP — Open/Closed Principle

    Principle meaning:
        "Software entities should be open for extension, but closed for modification."

    How we apply it:
        The orchestrator will talk to channels via this abstraction.

        To add a new channel (e.g., Push, WhatsApp, Slack),
        you create a new class implementing `notify(order, message)`.

        You do NOT modify the orchestrator logic.
    """

    def notify(self, order: Order, message: str) -> None:
        """Deliver the message to the order's customer via this channel."""
        ...


class DirectChannel:
    """
    A reusable channel implementation built from:
        - a DestinationResolver (ISP)
        - a MessageSender (ISP)

    SRP:
        This class coordinates just enough to send via one channel type.

    DIP:
        It depends on abstractions (Protocols), not concrete implementations.
    """

    def __init__(
        self,
        *,
        name: str,
        resolver: DestinationResolver,
        sender: MessageSender,
        logger: SimpleLogger,
    ) -> None:
        self._name = name
        self._resolver = resolver
        self._sender = sender
        self._logger = logger

    @property
    def name(self) -> str:
        return self._name

    def notify(self, order: Order, message: str) -> None:
        destination = self._resolver.resolve(order.customer)
        self._logger.info(f"Sending via {self._name} to {destination}")
        self._sender.send(destination, message)


# =============================================================================
# SOLID: L — Liskov Substitution Principle (LSP)
# =============================================================================

class SafeChannelWrapper:
    """
    LSP — Liskov Substitution Principle

    Principle meaning:
        If S is a subtype of T, then objects of type T can be replaced with objects
        of type S without altering correctness.

    What "correctness" means here:
        The orchestrator expects:
            - a channel has notify(order, message)
            - if it fails, it raises an exception (or handles internally)
        It should not silently "pretend it succeeded" in a misleading way.

    This wrapper is a "substitutable" NotificationChannel:
        - It implements the same interface as any channel
        - It preserves the essential contract:
            - either it notifies successfully
            - or it logs and re-raises (or could record failure in a well-defined way)

    Why this is LSP:
        You can replace a channel with SafeChannelWrapper(channel)
        and the rest of the system still behaves correctly and predictably.
    """

    def __init__(self, inner: NotificationChannel, logger: SimpleLogger) -> None:
        self._inner = inner
        self._logger = logger

    def notify(self, order: Order, message: str) -> None:
        try:
            self._inner.notify(order, message)
        except Exception as exc:
            self._logger.warning(
                f"Channel failed ({self._inner.__class__.__name__}): {exc}"
            )
            # Re-raise so the caller can decide what to do.
            raise


class BlackHoleChannel:
    """
    This is an example of what NOT to do (LSP violation),
    but we keep it here as a teaching artifact.

    It implements notify() but discards messages and claims success.
    If the system relies on the notification actually being sent,
    substituting this would break correctness.

    In other words:
        - Signature matches, but behavioral contract doesn't.
        - That violates LSP.

    We will NOT use this in our "good" orchestration run below.
    """

    def notify(self, order: Order, message: str) -> None:
        # Message is silently dropped -> violates typical expectations.
        return


# =============================================================================
# SOLID: D — Dependency Inversion Principle (DIP)
# =============================================================================

class OrderConfirmationService:
    """
    DIP — Dependency Inversion Principle

    Principle meaning:
        1) High-level modules should not depend on low-level modules.
           Both should depend on abstractions.
        2) Abstractions should not depend on details.
           Details should depend on abstractions.

    High-level module here:
        OrderConfirmationService — the application workflow:
            validate -> create message -> notify via channels

    Low-level modules:
        - ConsoleEmailSender, ConsoleSmsSender
        - EmailDestinationResolver, PhoneDestinationResolver
        - SimpleLogger

    The DIP move:
        - This service depends on abstractions for channels (NotificationChannel)
          and on small SRP services (validator, message factory).
        - It does not construct concrete senders inside.
        - Construction/injection happens at the composition root (main()).
    """

    def __init__(
        self,
        *,
        validator: OrderValidator,
        message_factory: NotificationMessageFactory,
        channels: Iterable[NotificationChannel],
        logger: SimpleLogger,
    ) -> None:
        self._validator = validator
        self._message_factory = message_factory
        self._channels = list(channels)
        self._logger = logger

    def confirm(self, order: Order) -> None:
        """
        Confirm an order and send notifications.

        SRP note:
            This method is an "application service" — it coordinates steps.
            It delegates details (validation, formatting, sending) elsewhere.

        OCP note:
            Adding a new notification channel does NOT change this method.
            You extend the system by providing a new channel implementation.

        LSP note:
            Any channel that obeys the NotificationChannel contract can be used here.
        """
        self._validator.validate(order)
        message = self._message_factory.order_confirmation(order)

        failures = 0
        for channel in self._channels:
            try:
                channel.notify(order, message)
            except Exception:
                failures += 1

        if failures:
            self._logger.warning(
                f"Order {order.order_id}: {failures} notification channel(s) failed."
            )
        else:
            self._logger.info(f"Order {order.order_id}: all notifications sent.")


# =============================================================================
# Composition Root
# =============================================================================

def main() -> None:
    """
    The composition root is where you wire concrete implementations together.

    This keeps constructors clean and supports:
    - Testing (swap ConsoleEmailSender for a fake)
    - OCP (add channels without changing business logic)
    - DIP (high-level code doesn't create low-level details)
    """
    logger = SimpleLogger()

    # SRP-focused services:
    validator = OrderValidator()
    message_factory = NotificationMessageFactory()

    # Low-level details (could be swapped for real integrations):
    email_sender = ConsoleEmailSender()
    sms_sender = ConsoleSmsSender()

    # Destinations:
    email_resolver = EmailDestinationResolver()
    phone_resolver = PhoneDestinationResolver()

    # Channels (OCP: you can add more without touching OrderConfirmationService):
    email_channel: NotificationChannel = DirectChannel(
        name="email",
        resolver=email_resolver,
        sender=email_sender,
        logger=logger,
    )
    sms_channel: NotificationChannel = DirectChannel(
        name="sms",
        resolver=phone_resolver,
        sender=sms_sender,
        logger=logger,
    )

    # LSP: wrap channels with a substitutable safety wrapper.
    safe_email_channel = SafeChannelWrapper(email_channel, logger)
    safe_sms_channel = SafeChannelWrapper(sms_channel, logger)

    # High-level orchestration depends on abstractions:
    service = OrderConfirmationService(
        validator=validator,
        message_factory=message_factory,
        channels=[safe_email_channel, safe_sms_channel],
        logger=logger,
    )

    # Demo data:
    customer = Customer(
        customer_id="C-100",
        name="Ava",
        email="ava@example.com",
        phone="+15555550123",
    )
    order = Order(order_id="O-9001", customer=customer, total_usd=49.99)

    service.confirm(order)

    print("\n--- Demonstrating a failure scenario (missing phone) ---\n")
    customer_no_phone = Customer(
        customer_id="C-101",
        name="Noah",
        email="noah@example.com",
        phone=None,
    )
    order2 = Order(order_id="O-9002", customer=customer_no_phone, total_usd=19.99)

    # The SMS resolver will raise ValueError; SafeChannelWrapper logs and re-raises,
    # and the service counts the failure.
    service.confirm(order2)


if __name__ == "__main__":
    main()
