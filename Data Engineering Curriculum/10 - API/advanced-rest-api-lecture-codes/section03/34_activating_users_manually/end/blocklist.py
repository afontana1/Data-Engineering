"""
blocklist.py

This file just contains the blocklist of the JWT tokens–it will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""

BLOCKLIST = set()
