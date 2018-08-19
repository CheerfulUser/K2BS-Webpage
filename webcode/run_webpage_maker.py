import argparse

# Help string to be shown using the -h option
descStr = """
Wrapper for the K2BS website making code, give it a results location and a save location.
"""

# Parse the command line options
parser = argparse.ArgumentParser(description=descStr,
                             formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("data_directory", metavar="Direcrory of data", nargs=1,
                    help="Direcrory of data to make webpages from.")

parser.add_argument("path", metavar="Path to save directory", nargs=1,
                    help="The website pages will be saved in this directory.")

location = ['length/','brightness/','category/','sub_category/','events/','event/']
location = [path + s for s in location]


from K2BS_website import *

Make_individual_event_page(data_directory,location)
Make_candidate_webpage(data_directory,location)
Make_category_pages(location)
Make_brightness_pages(location)
Make_length_pages(location)
Make_homepage(location)