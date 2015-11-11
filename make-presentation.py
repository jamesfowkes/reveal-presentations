from xml.dom import minidom
from config_reader import Config

import args

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
	if 'banner_image' in config:
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

def replace_title(dom, new_title):
	old_title_node = dom.getElementsByTagName('title').item(0)
	parent = old_title_node.parentNode
	new_title_node = dom.createElement('title')
	new_title_text_node = dom.createTextNode(new_title)
	new_title_node.appendChild(new_title_text_node)
	parent.replaceChild(new_title_node, old_title_node)

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

def run():

	_args = args.get_args()

	config = Config.get_from_stream( open(_args.config, 'r'))
	
	original_dom = load_html_template()

	replace_title(original_dom, config.title)
	add_css(original_dom, config.css)

	for slide_folder in config.folders:
		add_to_template(slide_folder, original_dom, config)

	imp = minidom.getDOMImplementation('')
	dt= imp.createDocumentType('html', 
		'-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')

	make_closing_tags(original_dom)

	with open(config.output_filename(), 'w') as f:
		original_dom.writexml(f, "", "  ")

if __name__ == "__main__":
	run()
