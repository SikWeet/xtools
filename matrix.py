import random
from typing import Literal
import numpy as np

class Matrix:
	@staticmethod
	def generate(rows: int, cols: int, 
					fill_type: Literal['zero', 'one', 'identity', 'random', 'sequence', 'numpy_zero', 'numpy_random'] = 'zero', value_range=(1, 10)):
		"""
		Generates a matrix of the specified size and fill type.

		:param rows: Number of lines
		:param cols: Number of columns
		:param fill_type: Fill type (zero, one, identity, random, sequence)
		:param value_range: Value range (random only)
		:return: Generated matrix (list of lists)
		"""
		if fill_type == "zero":
			return [[0] * cols for _ in range(rows)]

		elif fill_type == "one":
			return [[1] * cols for _ in range(rows)]

		elif fill_type == "identity":
			if rows != cols:
				raise ValueError("A unit matrix can only be created for square dimensions!")
			return [[1 if i == j else 0 for j in range(cols)] for i in range(rows)]

		elif fill_type == "random":
			return [[random.randint(value_range[0], value_range[1]) for _ in range(cols)] for _ in range(rows)]

		elif fill_type == "sequence":
			return [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]

		elif fill_type == "numpy_zero":
			return np.zeros((rows, cols), dtype=int).tolist()

		elif fill_type == "numpy_random":
			return np.random.randint(value_range[0], value_range[1] + 1, (rows, cols)).tolist()

		else:
			raise ValueError("Unsupported fill type!")
	
	@staticmethod
	def transpose(matrix):
		return [list(row) for row in zip(*matrix)]

	@staticmethod
	def sum_matrices(matrixA, matrixB):
		"returns the sum of two matrices"
		return [[matrixA[i][j] + matrixB[i][j] for j in range(len(matrixA[0]))] for i in range(len(matrixA))]

	@staticmethod
	def multiply_by_scalar(matrix, scalar):
		"returns the matrix multiplied by a number"
		return [[x * scalar for x in row] for row in matrix]

	@staticmethod
	def multiply_matrices(A, B):
		"returns the multiplied two matrices"
		return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

	@staticmethod
	def rotate_90(matrix):
		"returns a 90 degree rotated matrix"
		return [list(row) for row in zip(*matrix[::-1])]

	@staticmethod
	def is_symmetric(matrix):
		"returns a logical value, checks the matrix for symmetry"
		return matrix == Matrix.transpose(matrix)

	@staticmethod
	def get_max_element(matrix):
		"returns the maximum value of the matrix"
		return max(max(row) for row in matrix)

	@staticmethod
	def print_matrix(matrix):
		for row in matrix:
			print(" ".join(map(str, row)))