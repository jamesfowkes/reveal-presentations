from xml.dom import minidom
import configparser

from jinja2 import Template

import args
import logging

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
	
def process_dom(dom, config):
	if 'banner_image' in config['Global Config']:
		for img_node in dom.getElementsByTagName("img"):
			if img_node.getAttribute("id") == "banner_img":
				img_node.setAttribute("src", config.banner_image)

def add_to_template(slide_folder, original_dom, config):
	try:
		dom = minidom.parse(slide_folder+"/slides.html")
		process_dom(dom, config)
	except Exception as e:
		print("Error when parsing {}: {}".format(slide_folder, e))
		return
		
	slides_div = get_slides_div(original_dom)

	sections = dom.getElementsByTagName("sections")[0]
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
		template_config[k] = v
		logging.info("%s = %s", k, v)

	return (config, template_config)

def add_slides(original_dom, config):
	for slide_folder in get_folders(config['Global Config']['folders']):
		add_to_template(slide_folder, original_dom, config)

def run():

	_args = args.get_args()

	(config, template_config) = get_config(_args.config)

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
