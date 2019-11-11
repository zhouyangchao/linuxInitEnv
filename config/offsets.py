import gdb
import gdb.types
import math

CACHELINE_LEN = 64

class Offsets(gdb.Command):
	def __init__(self):
		super (Offsets, self).__init__ ('offsets', gdb.COMMAND_DATA)

	def invoke(self, arg, from_tty):
		stype = gdb.lookup_type(arg)
		last_sz = 0
		padding = 0
		self.off_zeros = len(str(stype.sizeof))
		self.cl_zeros = len(str(int(math.ceil(stype.sizeof//CACHELINE_LEN))))

		print(arg + ' {')
		for field in stype.fields():
			field_byte = field.bitpos//8
			if field_byte > last_sz:
				print('[%s][%s]*   uint8_t padding%d[%d]' % ( \
					str(last_sz).zfill(self.off_zeros), \
					str(field_byte//CACHELINE_LEN).zfill(self.cl_zeros), \
					padding, field_byte - last_sz))
				padding += 1
			print('[%s][%s]    %s %s: %d' % ( \
				str(field_byte).zfill(self.off_zeros), \
				str(field_byte//CACHELINE_LEN).zfill(self.cl_zeros), \
				field.type, field.name, field.type.sizeof))
			last_sz = field.type.sizeof + field_byte
		if stype.sizeof != last_sz:
			print('[%s][%s]*   uint8_t padding%d:[%d]' % ( \
				str(last_sz).zfill(self.off_zeros), \
				str(last_sz//CACHELINE_LEN).zfill(self.cl_zeros), \
				padding, stype.sizeof - last_sz))
		print('}')
		print('sizeof(%s) = %d' % (arg, stype.sizeof))


class OffsetsDepth(gdb.Command):
	def __init__(self):
		super (OffsetsDepth, self).__init__ ('offsets_depth', gdb.COMMAND_DATA)

	def print_subfield(self, f, depth=2):
		if f.type.code != gdb.TYPE_CODE_STRUCT and f.type.code != gdb.TYPE_CODE_UNION:
			return
		depth_str = "    " * depth
		for name, field in f.type.iteritems():
			field_byte = field.bitpos//8
			print('[%s][%s]%s%s %s: %d' % ( \
				str(field_byte).zfill(self.off_zeros), \
				str(field_byte//CACHELINE_LEN).zfill(self.cl_zeros), \
				depth_str, field.type, field.name, field.type.sizeof))
			self.print_subfield(field, depth+1)

	def invoke(self, arg, from_tty):
		stype = gdb.lookup_type(arg)
		last_sz = 0
		padding = 0
		self.off_zeros = len(str(stype.sizeof))
		self.cl_zeros = len(str(int(math.ceil(stype.sizeof//CACHELINE_LEN))))

		print(arg + ' {')
		for field in stype.fields():
			field_byte = field.bitpos//8
			if field_byte > last_sz:
				print('[%s][%s]*   uint8_t padding%d[%d]' % ( \
					str(last_sz).zfill(self.off_zeros), \
					str(field_byte//CACHELINE_LEN).zfill(self.cl_zeros), \
					padding, field_byte - last_sz))
				padding += 1
			print('[%s][%s]    %s %s: %d' % ( \
				str(field_byte).zfill(self.off_zeros), \
				str(field_byte//CACHELINE_LEN).zfill(self.cl_zeros), \
				field.type, field.name, field.type.sizeof))
			self.print_subfield(field)
			last_sz = field.type.sizeof + field_byte
		if stype.sizeof != last_sz:
			print('[%s][%s]*   uint8_t padding%d:[%d]' % ( \
				str(last_sz).zfill(self.off_zeros), \
				str(last_sz//CACHELINE_LEN).zfill(self.cl_zeros), \
				padding, stype.sizeof - last_sz))
		print('}')
		print('sizeof(%s) = %d' % (arg, stype.sizeof))

Offsets()
OffsetsDepth()
