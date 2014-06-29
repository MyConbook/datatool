from glob import glob
import zipfile
import os

class Maps(object):
	def __init__(self, options, version):
		self.maps_path = options.get_data_path("maps/")
		self.zip_path = options.get_output_path("maps.zip")
		self.options = options
		self.version = version

	def pack(self):
		if self.options.is_preview:
			return

		images = glob(self.maps_path + "*.png")
		with zipfile.ZipFile(self.zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
			for image in images:
				zip_file.write(image, os.path.basename(image))
