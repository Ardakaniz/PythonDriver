import serial
import serial.tools.list_ports

class LLDriver():
	_opDic = {
		'FILL_REGS':    b'\x02',

		'DBG:LED':      b'\x10',
		'DBG:SHIFTREG': b'\x11',
	}

	def __init__(self, st_port=None):
		self.ser = serial.Serial()
		self.ser.baudrate = 921600

		ports = serial.tools.list_ports.comports()

		if st_port is None:
			for port in ports:
				# If there are multiple serial ports, we'll just use the first one
				if port.description == "STMicroelectronics STLink Virtual COM Port":
					st_port = port.device
					break

			if st_port is None:
				raise Exception("No STLink found, please select one")

		self.ser.port = st_port
		self.ser.open()

	def __del__(self):
		if self.ser.is_open:
			self.ser.close()

	def list_ports():
		return list(serial.tools.list_ports.comports())

	def commands(name = None):
		if name is None:
			return list(LLDriver._opDic.keys())
		else:
			return LLDriver._opDic[name]

	def send_command(self, command, *kwargs):
		if command not in LLDriver._opDic:
			raise Exception("Command not found")
		if not self.ser.is_open:
			raise Exception("Serial port not open")

		cmd = b'\xAA' + LLDriver._opDic[command]
		for arg in kwargs:
			cmd += bytes(arg)
		cmd += b'\xAA'
		return self.ser.write(cmd)

	def read(self, size=None, flush=True):
		"""
		Reads from the µc.

		Parameters:
			size: The number of bytes to read. If None, reads everything.
			flush: If True, flushes the input buffer if non-empty after {size} bytes have been read.
		
		Returns:
			The bytes read.
		"""
		if size is None:
			out = b'';
			while self.ser.in_waiting:
				out += self.ser.read()
			return out
		
		# else
		out = self.ser.read(size)
		if flush:
			while self.ser.in_waiting:
				self.set.read()
		return out