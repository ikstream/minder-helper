#!/usr/bin/env python3
"""
TODO: calculate text length in pixel from str length
TODO: read style from config file yaml/toml/ini
TODO: allow setting styles from api
TODO: Add Node styles -> and corrosponding functions
TODO: Exception and error handling -> everything that could throw an exception or a user could miss/mix up
TODO: 
"""
import xml.etree.ElementTree as ET
import sys

parent_etag = "3708655056"
etag = "986967105"
minder_version = "1.16.4"

def _add_entry(parent_tree_Elem, identfier, **data):

    if data:
        print(data)

    try:
        entry = ET.SubElement(parent_tree_Elem, identfier, data)
        ET.indent(entry, space='  ', level=1)
        return entry
    except Exception as e:
        sys.exit(f"Failed to create tree subelement: {e}")


class minder_node:
    def __init__(self, parent, node_id, posx, posy, width="100", height="46", color='', colorroot="false"):
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
        self.colorroot = colorroot 
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
        self.tree_elem = _add_entry(self.parent, 'node', id=self.node_id, posx=self.posx, 
                      posy=self.posy, width=self.width, height=self.height,
                      side=self.side, fold=self.fold,
                      treesize=self.treesize, color= self.color, summarized=self.summarized,
                      layout=self.layout)
        _add_entry(self.tree_elem, 'style',
                   branchmargin=f"{self.node_style['branchmargin']}",
                   branchradius=f"{self.node_style['branchradius']}",
                   linktype=f"{self.node_style['linktype']}",
                   linkwidth=f"{self.node_style['linkwidth']}",
                   linkarrow=f"{self.node_style['linkarrow']}",
                   linkdash=f"{self.node_style['linkdash']}",
                   nodeborder=f"{self.node_style['nodeborder']}",
                   nodewidth=f"{self.node_style['nodewidth']}",
                   nodeborderwidth=f"{self.node_style['nodeborderwidth']}",
                   nodefill=f"{self.node_style['nodefill']}",
                   nodemargin=f"{self.node_style['nodemargin']}",
                   nodepadding=f"{self.node_style['nodepadding']}",
                   nodefont=f"{self.node_style['nodefont']}",
                   nodemarkup=f"{self.node_style['nodemarkup']}")
        n_name = _add_entry(self.tree_elem, 'nodename', maxwidth="200") #ET.SubElement(self.tree_elem, 'nodename', maxwidth="200")
        _add_entry(n_name, 'text', data =self.text)
        n_note = _add_entry(self.tree_elem, 'nodenote')
        n_note.text = self.note
        ET.indent(self.tree_elem, space='  ', level=1)
        return self.tree_elem

    
    def set_text(self, text):
        self.text=text + f"(id:{self.node_id})"
        
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
        side = side.lower()
        if 'right' == side or 'left' == side:
            self.side = side
            return self.side
        else:
            raise KeyError(f"side should be either 'left' or 'right' but is {side}")
    
    def set_fold(self, fold:str="true"):
        """
        Switch between fold stages

        Args:
            fold (str, optional): Set the fold value of a node (false/true). Defaults to true.

        Returns:
            str: return current state of the fold variable of a node
        """
        fold = fold.lower()
        if 'false' == fold or 'true' == fold:
            self.fold = fold
            return fold
        else:
            raise KeyError(f"fold should be either 'false' or 'true' but is {fold}")


class mind_map:
    
    def __init__(self):
        self.node_map = {}
        self.last_id = "0"

    def _add_styles(self, tree_elem):
        """
        Add the styles block for minder 
        """
        styles = _add_entry(tree_elem, 'styles')
        for level in range(11):
            self._add_style(level, tree_elem=styles)
            
    def _add_style(self, parent_tree_Elem, level):
        """
        Add a style to the styles Block
        """
        _add_entry(parent_tree_Elem, 'style', level=f"{level}", 
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
        Create the base structure for the minder mind map xml file
        
        Returns:
            _type_: XML tree structure for Minder file
        """
        print("generate xml file")
        minder = ET.Element('minder', version=minder_version, parent_etag=parent_etag, etag=etag)
        _add_entry(minder, 'theme', name="default", label="Light", index="-1")
        styles = _add_entry(minder, 'styles')
        for level in range(11):
            self._add_style(styles, level)
        #self._add_styles(minder)
        _add_entry(minder, 'images')
        ET.indent(_add_entry(minder, 'nodes'), space='  ', level=1)
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
        text = text
        root_node.set_text(text)
        root_node.set_note(note)
        r_node = root_node.create_node()
        ET.indent(r_node, space='  ', level=1)

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
            posx_offset = 0
            posy_offset = 50
        
            if n_id == parent:
                nodes_elem = node.find('nodes')
                if not nodes_elem:
                    print("no nodes entry found")
                    nodes_elem = _add_entry(node,'nodes')
                    posx_offset = 50
                    posy_offset = 0
                    # node.attrib['posy']
           
                posx = int(node.attrib['posx']) + posx_offset
                posy = int(node.attrib['posy']) + posy_offset
                print(f"node found Node id {n_id} == {parent}")
                child_node = minder_node(nodes_elem, str(int(self.last_id) + 1), posx=str(posx), posy=str(posy), color=color)
                child_node.set_text(text)
                child_node.set_note(note)
                child_node.create_node()
                self.last_id = str(int(self.last_id) + 1)
                
                
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
    mm.create_new_node(tree, '0', 'Second Child Node', note='Second Child node note test')
    mm.create_new_node(tree, '1', 'First GrandChild Node', note='GrandChild node note test', color='#68b723')
    
    # write file    
    tree.write('big_generated.minder', xml_declaration=True,encoding='utf-8',
               method="xml")
