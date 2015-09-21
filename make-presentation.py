from xml.dom import minidom

import args

def make_closing_tags(dom):
	for node in dom.getElementsByTagName("script"):
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

	
def process_dom(dom, **kwargs):
	if 'banner_image' in kwargs.keys():
		for img_node in dom.getElementsByTagName("img"):
			if img_node.getAttribute("id") == "banner_img":
				img_node.setAttribute("src", kwargs['banner_image'])

def add_to_template(slide_folder, original_dom, **kwargs):
	dom = minidom.parse(slide_folder+"/slides.html")
	process_dom(dom, **kwargs)

	slides_div = get_slides_div(original_dom)
	slide_nodes = dom.getElementsByTagName("section")
	for slide_node in slide_nodes:
		slides_div.appendChild(slide_node)

def replace_title(dom, new_title):
	old_title_node = dom.getElementsByTagName('title').item(0)
	parent = old_title_node.parentNode
	new_title_node = dom.createElement('title')
	new_title_text_node = dom.createTextNode(new_title)
	new_title_node.appendChild(new_title_text_node)
	parent.replaceChild(new_title_node, old_title_node)
	
def run():

	_args = args.get_args()

	slide_folders = _args.folders.split(',')
	banner_image = _args.banner_image
	title = _args.title
	original_dom = load_html_template()

	replace_title(original_dom, title)
	for slide_folder in slide_folders:
		add_to_template(slide_folder, original_dom, banner_image=banner_image)

	imp = minidom.getDOMImplementation('')
	dt= imp.createDocumentType('html', 
		'-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')

	make_closing_tags(original_dom)

	with open(_args.outfile, 'w') as f:
		original_dom.writexml(f, "", "  ")

if __name__ == "__main__":
	run()
