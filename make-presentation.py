""" 
Usage:
	make-presentation.py <config_filename>


"""


import docopt
import logging

from xml.dom import minidom
import configparser

from jinja2 import Template


def external_links_config_processor(v):
	parts = [part.strip() for part in v.split(", ")]
	titles = parts[0::2]
	urls = parts[1::2]
	return [{"title":title, "url": url} for title, url in zip(titles, urls)]

template_config_processors = {
	"external_links": external_links_config_processor
}

def make_closing_tags(dom):
	for node in dom.getElementsByTagName("script"):
		node.appendChild(dom.createTextNode(''))		

	for node in dom.getElementsByTagName("iframe"):
		node.appendChild(dom.createTextNode(''))		
	
def load_html_template():
	dom = minidom.parse("slides/presentation-template.html")
	return dom

def get_slides_div(dom):
	divs = dom.getElementsByTagName("div")
	for div in divs:
		try:
			if div.getAttribute("class") == "slides":
				return div
		except:
			pass

def get_slides_dom(slide_folder):
	
	filepath = slide_folder+"/slides.html"
	try:
		dom = minidom.parse(filepath)
	except Exception as e:
		print("Error when parsing {}: {}".format(filepath, e))
		dom = None

	return dom

def add_to_template(slide_folder, original_dom, config):
		
	slides_dom = get_slides_dom(slide_folder)
	slides_div = get_slides_div(original_dom)

	sections = slides_dom.getElementsByTagName("sections")[0]
	for section in sections.childNodes:
		if type(section) == minidom.Element:
			slides_div.appendChild(section)

def add_css(dom, css):

	if type(css) != list:
		css = [css]

	for css_file in css:
		head_node = dom.getElementsByTagName("head")[0]
		css_node = dom.createElement("link")
		css_node.setAttribute("href", css_file)
		css_node.setAttribute("id", "theme")
		css_node.setAttribute("rel", "stylesheet")
		head_node.appendChild(css_node)

def get_output_filename(config):
	title = config['Template']['title']
	title = title.lower()
	title = title.replace(" ", "-")
	return title + ".html"

def get_folders(config):
	folders = [folder.strip() for folder in config.split(",")]
	return folders

def get_config(config_file):

	template_config = {}

	config = configparser.ConfigParser()
	config.read(config_file)

	logging.info("Global config:")
	for k, v in config['Global Config'].items():
		logging.info("%s = %s", k, v)

	logging.info("Template config:")
	for k, v in config['Template'].items():
		try:
			template_config[k] = template_config_processors[k](v)
			logging.info("%s = %s (special processing)", k, template_config[k])
		except KeyError:
			logging.info("%s = %s", k, v)
			template_config[k] = v


	return (config, template_config)

def add_slides(original_dom, config):
	for slide_folder in get_folders(config['Global Config']['folders']):
		logging.info("Adding slides from {}".format(slide_folder))
		add_to_template(slide_folder, original_dom, config)

def run():

	args = docopt.docopt(__doc__)

	(config, template_config) = get_config(args["<config_filename>"])

	original_dom = load_html_template()

	add_css(original_dom, config['Global Config']['css'])

	add_slides(original_dom, config)
	
	imp = minidom.getDOMImplementation('')
	dt= imp.createDocumentType('html', 
		'-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')

	make_closing_tags(original_dom)

	xml = original_dom.toxml()

	template = Template(xml)

	with open(get_output_filename(config), 'w') as f:
		f.write(template.render(conf=template_config))

if __name__ == "__main__":

	logging.basicConfig(level=logging.INFO)
	run()
