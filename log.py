import logging

def logging_decorator(logger,string):
	def decorator(function):
		def wrapper(*args,**kwargs):
			result = function(*args,**kwargs)
			logger.debug(string)
			return result
		return wrapper
	return decorator
