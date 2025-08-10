import random
import colorsys


class ColorUtils:
	@staticmethod
	def random_hex() -> str:
		"""
		Generates a random HEX color.
		Returns:
			str: Random HEX color in format '#RRGGBB'.
		"""
		return "#{:06x}".format(random.randint(0, 0xFFFFFF))

	@staticmethod
	def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
		"""
		Converts HEX color to RGB tuple.

		Args:
			hex_color (str): HEX color in format '#RRGGBB'.

		Returns:
			tuple[int, int, int]: RGB representation (0-255).
		"""
		hex_color = hex_color.lstrip('#')
		return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

	@staticmethod
	def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
		"""
		Converts RGB tuple to HEX color.

		Args:
			rgb (tuple): RGB color as tuple of three integers (0-255).

		Returns:
			str: HEX color in format '#RRGGBB'.
		"""
		return "#{:02x}{:02x}{:02x}".format(*rgb)

	@staticmethod
	def lighten(hex_color: str, amount: float) -> str:
		"""
		Lightens a HEX color.

		Args:
			hex_color (str): HEX color.
			amount (float): Lighten factor (0.0 - no change, 1.0 - full white).

		Returns:
			str: Lightened HEX color.
		"""
		rgb = ColorUtils.hex_to_rgb(hex_color)
		h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
		l = min(1, l + amount)
		r, g, b = colorsys.hls_to_rgb(h, l, s)
		return ColorUtils.rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))

	@staticmethod
	def saturate(hex_color: str, amount: float) -> str:
		"""
		Changes saturation of a HEX color.

		Args:
			hex_color (str): HEX color.
			amount (float): Positive to increase, negative to decrease (-1.0 to 1.0).

		Returns:
			str: HEX color with changed saturation.
		"""
		rgb = ColorUtils.hex_to_rgb(hex_color)
		h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
		s = max(0, min(1, s + amount))
		r, g, b = colorsys.hls_to_rgb(h, l, s)
		return ColorUtils.rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))

	@staticmethod
	def gradient(start_hex: str, end_hex: str, steps: int) -> list[str]:
		"""
		Generates a gradient between two HEX colors.

		Args:
			start_hex (str): Start HEX color.
			end_hex (str): End HEX color.
			steps (int): Number of gradient colors.

		Returns:
			list[str]: List of HEX colors representing the gradient.
		"""
		start_rgb = ColorUtils.hex_to_rgb(start_hex)
		end_rgb = ColorUtils.hex_to_rgb(end_hex)

		gradient_list = []
		for i in range(steps):
			ratio = i / (steps - 1)
			r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
			g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
			b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
			gradient_list.append(ColorUtils.rgb_to_hex((r, g, b)))

		return gradient_list