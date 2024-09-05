#!/usr/bin/env python3
"""
TODO: calculate text length in pixel from str length
TODO: read style from config file yaml/toml/ini
TODO: allow setting styles from api
TODO: Add Node styles -> and corrosponding functions
TODO: Exception and error handling -> everything that could throw an exception or a user could miss/mix up
TODO: 
"""
parent_etag = "3708655056"
etag = "986967105"
minder_version = "1.16.4"

import xml.etree.ElementTree as ET
def _add_entry(parent_tree_Elem, identfier, **data):
    if data:
        print(data)
    return ET.SubElement(parent_tree_Elem, identfier, data)

class minder_node:
    def __init__(self, parent, node_id, posx, posy, width, height, color='', colorroot=False):
        """_summary_

        Args:
            parent (_type_): _description_
            node_id (_type_): _description_
            posx (_type_): _description_
            posy (_type_): _description_nodes.findall
            width (_type_): _description_
            height (_type_): _description_
            color (str, optional): _description_. Defaults to ''.
            colorroot (bool, optional): _description_. Defaults to False.
        """
        self.parent=parent
        self.node_id=node_id
        self.posx=posx
        self.posy=posy
        self.width=width
        self.height=height
        self.side="right"
        self.fold="false"
        self.treesize="46"
        self.summarized="false"
        self.layout="Horizontal"
        self.color=color
        if colorroot == True:
            self.colorroot="true"
        else:
            self.colorroot="false"
        self.node_style = {'branchmargin':"100",
                           'branchradius':"25",
                           'linktype':"straight",
                           'linkwidth':"4",
                           'linkarrow':"false",
                           'linkdash':"solid",
                           'nodeborder':"underlined",
                           'nodewidth':"200",
                           'nodeborderwidth':"4",
                           'nodefill':"false",
                           'nodemargin':"8",
                           'nodepadding':"6",
                           'nodefont':"Sans 11",
                           'nodemarkup':"true"}
        self.text=''
        self.image=''
        self.note=''
        self.tree_elem=''
            
    def create_node(self):
        self.tree_elem = ET.SubElement(self.parent, 'node', id=self.node_id, posx=self.posx, 
                      posy=self.posy, width=self.width, height=self.height,
                      side=self.side, fold=self.fold,
                      treesize=self.treesize, summarized=self.summarized,
                      layout=self.layout)
        nname = _add_entry(self.tree_elem, 'nodename', maxwidth="200") #ET.SubElement(self.tree_elem, 'nodename', maxwidth="200")
        ET.SubElement(nname, 'text', data =self.text)
        nnote = ET.SubElement(self.tree_elem, 'nodenote')
        nnote.text = self.note
        return self.tree_elem

    
    def set_text(self, text):
        self.text=text
        
    def set_image(self, image:str):
        self.image=image
        
    def set_note(self, note:str=''):
        self.note=note

    def set_side(self, side:str="left"):
        """
        Set side value of a node

        Args:
            side (str, optional): side of a node, either left, or right. Defaults to left.

        Returns:
            str: current value of side of a node
        """
        if not 'right' == side or not 'left' == side:
            # TODO: thow exception
            print("side not left or right")
            pass
        self.side = side
        return self.side
    
    def set_fold(self, fold:bool=True):
        """
        Switch between fold stages

        Args:
            fold (bool, optional): Set the fold value of a node. Defaults to True.

        Returns:
            bool: return current state of the fold variable of a node
        """
        self.fold = fold
        return fold


class mind_map:
    
    def __init__(self):
        self.node_map = {}
        self.last_id = ''

    
    def _add_styles(self, treeElem):
        """
        Add the styles block for minder 
        """
        styles = ET.SubElement(treeElem, 'styles')
        for level in range(11):
            self._add_style(level, treeElem=styles)
            
    def _add_style(self, parent_tree_Elem, level):
        """
        Add a style to the styles Block
        """
        ET.SubElement(parent_tree_Elem, 'style', level=f"{level}", 
                      isset="false", branchmargin="100", 
                      branchradius="25", linktype="straight", 
                      linkwidth="4", linkarrow="false",
                      linkdash="solid", nodeborder="rounded",
                      nodewidth="200", nodeborderwidth="4",
                      nodefill="false", nodemargin="10",
                      nodepadding="10", nodefont="Sans 11", 
                      nodemarkup="true", connectiondash="dotted",
                      connectionlwidth="2", connectionarrow="fromto",
                      connectionpadding="3", connectionfont="Sans 10",
                      connectiontwidth="100", calloutfont="Sans 12",
                      calloutpadding="5", calloutptrwidth="20",
                      calloutptrlength="20")
            
    def generate_mindmap_metadata(self):
        """
        create the base structure for the minder mind map xml file
        """
        print("generate xml file")
        minder = ET.Element('minder', version=minder_version, parent_etag=parent_etag, etag=etag)
        _add_entry(minder, 'theme', name="default", label="Light", index="-1")
        styles = _add_entry(minder, 'styles')
        for level in range(11):
            self._add_style(styles, level)
        #self._add_styles(minder)
        _add_entry(minder, 'images')
        _add_entry(minder, 'nodes')
        _add_entry(minder, 'groups')
        _add_entry(minder, 'stickers')
        _add_entry(minder, 'nodelinks', id="0")
        tree = ET.ElementTree(minder)
        ET.indent(tree, space='  ', level=0)
        return tree
    
    def create_root_node(self, tree, text:str, note:str='', image:str=''):
        """
        create the root node 
        """
        minder = tree.getroot()
        nodes = minder.find('nodes')

        if self.node_map == {}:
            root_id = "0"

        root_node = minder_node(nodes, root_id, "100", "100", "100", "46")
        text = text + f" (id:{root_id})"
        root_node.set_text(text)
        root_node.set_note(note)
        root_node.create_node()

        self.node_map[root_id] = { root_id:root_node }
        self.last_id = root_id
        
    def create_new_node(self,
                        tree,
                        parent,
                        text:str='', 
                        color:str='#f9c440',
                        image:str='',
                        note:str=''):
        """
        Create a new node in an existing mind map
        """
        # Add node check -> check if parent is a ET Element or an id or name
        minder = tree.getroot()
        nodes = minder.findall('.//node')
        print(nodes)
        
        for node in nodes:
            n_id = node.attrib['id']
        
            if n_id == parent:
                if not node.find('nodes'):
                    print("no nodes entry found")
                    _add_entry(node,'nodes')
                    posx = str(int(node.attrib['posx']) + 100)
                    posy = node.attrib['posy']
                    print(f"position {posx}:{posy}")
                    
                                   
                print(f"node found Node id {n_id} == {parent}")
#                child_node = minder_node(node, )
        
    
    def get_node_name_by_id(self, tree, id:str=''):
        pass
    
    def get_nodes_id_by_name(self, tree, name:str=''):
        """
        Return IDs of all nodes matching the given name

        Args:
            tree (): XML tree
            name (str, optional): Name to search in tree, if none is given, return all nodes. Defaults to ''.

        Returns:
            Dictionary: Return a dictionary with id:name
        """
        nodes = {}        
        return nodes
    
    def set_color():
        """
        Change color of an existing node
        """
        pass
    
if __name__ == '__main__':
    # Create mindmap and get the tree
    mm = mind_map()
    tree = mm.generate_mindmap_metadata()
    
    # Create nodes
    mm.create_root_node(tree, 'Test-root-node', 'Note Test Test')
    mm.create_new_node(tree, '0', 'First Child Node', note='Child node note test')
    
    # write file    
    tree.write('big_generated.minder', xml_declaration=True,encoding='utf-8',
               method="xml")
