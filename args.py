import sys
import argparse

def get_args():
	parser = argparse.ArgumentParser(description='Produce reveal presentations from individual slides')

	parser.add_argument('--config', type=str, required=True,
		help='Filename of the config file describing the presentation')

	return parser.parse_args()