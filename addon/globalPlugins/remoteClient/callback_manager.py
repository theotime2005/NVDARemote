from logging import getLogger

logger = getLogger('callback_manager')
from collections import defaultdict

import wx


class CallbackManager:
	"""A simple way of associating multiple callbacks to events and calling them all when that event happens"""

	def __init__(self):
		self.callbacks = defaultdict(list)

	def registerCallback(self, event_type, callback):
		"""Registers a callback as a callable to an event type, which can be anything hashable"""
		self.callbacks[event_type].append(callback)

	def unregisterCallback(self, event_type, callback):
		"""Unregisters a callback from an event type"""
		self.callbacks[event_type].remove(callback)

	def callCallbacks(self, type, *args, **kwargs):
		"""Calls all callbacks for a given event type with the provided args and kwargs"""
		for callback in self.callbacks[type]:
			try:
				wx.CallAfter(callback, *args, **kwargs)
			except Exception as e:
				logger.exception("Error calling callback %r" % callback)
		for callback in self.callbacks['*']:
			try:
				wx.CallAfter(callback, type, *args, **kwargs)
			except Exception as e:
				logger.exception("Error calling callback %r" % callback)
