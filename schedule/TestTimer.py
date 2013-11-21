# -*- coding: utf-8 -*-
from Timer import Timer


class TestTimer(Timer):


	def __init__(self, fn, args=(), sleep=0):

		super(TestTimer, self).__init__(fn, args, sleep)


	def say(self):

		print "hello TestTimer"