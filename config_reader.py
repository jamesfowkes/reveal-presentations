import sys
import logging

from io import StringIO

def get_logger():
	return logging.getLogger(__name__)

def get_key_from_split_vals(vals):
	key = vals[0].strip()
	return key

def get_values_from_split_vals(vals):

	values = [v.strip() for v in vals[1].split(",")]
	return values

class Config:

	SINGLE_ITEM_ATTRS = ['title', 'banner_image']

	def __init__(self, **kwargs):

		self.logger = get_logger()
		self._config_attrs = kwargs.keys()

		for k, v in kwargs.items():
			if k in self.SINGLE_ITEM_ATTRS:
				v = v[0]
			self.logger.info("Setting attribute {} to {}".format(k, v))
			setattr(self, k, v)

			
	@classmethod
	def get_from_stream(cls, stream):
		cfg = {}
		for line in stream.readlines():
			try:
				kv = line.split("=")
				key = get_key_from_split_vals(kv)
				value = get_values_from_split_vals(kv)
				cfg[key] = value
			except IndexError:
				pass

		return cls(**cfg)

	def output_filename(self):
		filename = self.title
		filename = filename.replace(" ", "_")
		filename = filename.lower()
		filename += ".html"
		return filename

	def __contains__(self, a):
		return a in self._config_attrs
		
soh = logging.StreamHandler(sys.stdout)
get_logger().addHandler(soh)
get_logger().setLevel(logging.INFO)

if __name__ == "__main__":
	example = """
	folders = arduino-intro
	banner_image = hackspace-banner.png
	title=Introduction to Arduino
	"""

	print(read_config(StringIO(example)))
