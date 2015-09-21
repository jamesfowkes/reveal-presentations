import sys
import argparse

def get_args():
	parser = argparse.ArgumentParser(description='Produce reveal presentations from individual slides')

	parser.add_argument('--folders', type=str, required=True,
		help='Comma-separated list of folders to get slides from')

	parser.add_argument('--banner_image', type=str, required=True,
		help='Path to the banner image to use')

	parser.add_argument('--title', type=str, required=True,
		help='The presentation title')

	parser.add_argument('--outfile', type=str, required=True,
		help='Name of the new presentation')

	return parser.parse_args()