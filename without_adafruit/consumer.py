from sensorsLib import sensors

sen = sensors()
sen.start()
while True:

	print sen.get_queue()

sen.stop()

