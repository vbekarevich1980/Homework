# Task 5.5
# Implement a decorator `remember_result` which remembers last result of function it decorates and prints it before
# next call.
#
# ```python
# @remember_result
# def sum_list(*args):
# 	result = ""
#	for item in args:
#		result += item
#	print(f"Current result = '{result}'")
#	return result
#
# sum_list("a", "b")
# >>> "Last result = 'None'"
# >>> "Current result = 'ab'"
# sum_list("abc", "cde")
# >>> "Last result = 'ab'"
# >>> "Current result = 'abccde'"
# sum_list(3, 4, 5)
# >>> "Last result = 'abccde'"
# >>> "Current result = '12'"
# ```

def remember_result(function_to_decorate):

	def wrapper(*args, **kwargs):
		if hasattr(function_to_decorate, 'last_result'):
			print(f"Last result = '{function_to_decorate.last_result}'")
		else:
			print(f"Last result = 'None'")
		function_to_decorate.last_result = function_to_decorate(*args, **kwargs)
	return wrapper


@remember_result
def sum_list(*args):

	result = 0
	for item in args:
		if type(item) is str:
			result = ''
	for item in args:
		if type(result) is str:
			item = str(item)
		result += item
	print(f"Current result = '{result}'")
	return result


sum_list("a", "b")
sum_list("abc", "cde")
sum_list(3, 4, 5)
sum_list('3', 4, 5)
