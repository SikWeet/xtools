class ColorUtils:
	"""
	Utility class for working with colors.
	"""

	@staticmethod
	def hex_to_rgb(hex_color: str) -> tuple:
		"""
		Converts a HEX color string to an RGB tuple.

		:param hex_color: The HEX color string (e.g., '#FFFFFF').
		:return: The RGB tuple (R, G, B).
		"""
		hex_color = hex_color.lstrip('#')
		return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

	@staticmethod
	def rgb_to_hex(r: int, g: int, b: int) -> str:
		"""
		Converts RGB values to a HEX color string.

		:param r: Red component (0-255).
		:param g: Green component (0-255).
		:param b: Blue component (0-255).
		:return: The HEX color string (e.g., '#FFFFFF').
		"""
		return f'#{r:02x}{g:02x}{b:02x}'

	@staticmethod
	def hex_to_hsl(hex_color: str) -> tuple:
		"""
		Converts a HEX color string to an HSL tuple.

		:param hex_color: The HEX color string (e.g., '#FFFFFF').
		:return: The HSL tuple (H, S, L).
		"""
		r, g, b = ColorUtils.hex_to_rgb(hex_color)
		r, g, b = r / 255.0, g / 255.0, b / 255.0
		mx = max(r, g, b)
		mn = min(r, g, b)
		diff = mx - mn
		l = (mx + mn) / 2

		if diff == 0:
			h = s = 0
		else:
			s = diff / (2 - mx - mn) if l > 0.5 else diff / (mx + mn)
			if mx == r:
					h = (g - b) / diff + (6 if g < b else 0)
			elif mx == g:
					h = (b - r) / diff + 2
			else:
					h = (r - g) / diff + 4
			h /= 6

		return round(h * 360), round(s * 100), round(l * 100)
