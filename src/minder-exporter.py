#!/usr/bin/env python3

# Copyright (c) 2024 Stefan Venz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
                           'linktype':"curved",
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
                      treesize=self.treesize, color=self.color, summarized=self.summarized,
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
        self.text=text + f" (id:{self.node_id})"

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

    def get_node_id(self):
        return self.node_id

    def get_node_posx(self):
        return self.posx

    def get_node_posy(self):
        return self.posy

    def get_node_width(self):
        return self.width

    def get_node_height(self):
        return self.height

    def get_node_side(self):
        return self.side

    def get_node_fold(self):
        return self.fold

    def get_node_tree_size(self):
        return self.treesize

    def get_node_color(self):
        return self.color

    def get_node_colorroot(self):
        return self.colorroot

    def get_node_style(self):
        return self.node_style

    def get_node_data(self):
        #TODO read all the data from a node in to a minder node
        node_data = {}
        node_data['id'] = self.get_node_id()
        node_data['style'] = self.get_node_style()
        node_data['color'] = self.get_node_color()
        return node_data

    def set_color(self):
        """
        Change color of an existing node
        """
        pass


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

        _add_entry(minder, 'images')
        ET.indent(_add_entry(minder, 'nodes'), space='  ', level=0)
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
                ET.indent(minder, space="  ", level=2)
                child_node.create_node()
                self.last_id = str(int(self.last_id) + 1)

    def get_node_by_id(self, tree, node_id:str='0'):

        if isinstance(node_id, int):
            node_id = str(node_id)
        elif not isinstance(node_id, str):
            raise TypeError(f"The search id needs to be of type int or str! Provided type is {type(node_id)}")

        minder = tree.getroot()
        nodes = minder.findall('.//node')

        for node in nodes:
            n_id = node.attrib['id']
            if node_id == n_id:
                return node

        raise KeyError(f"No node found with id {id}")

    def get_node_by_string(self, tree, name:str=''):
        """
        Return IDs of all nodes matching the given name

        Args:
            tree (): XML tree
            name (str, optional): Name to search in tree, if none is given, return all nodes. Defaults to ''.

        Returns:
            Dictionary: Return a dictionary with id:name
        """
        matched_nodes = {}
        minder = tree.getroot()
        nodes = minder.findall('.//node')
        print(f"nodes: {nodes}")

        for node in nodes:
            n_text = node.find(f"nodename/text")
            data = n_text.attrib['data']

            if name in data:
                matched_nodes[node.attrib['id']] = data
            pass

        print(f"{matched_nodes}")
        return matched_nodes

    def get_parent(self, node_id):
        #TODO: get the parent ID of a current node
        if isinstance(node_id, int):
            node_id = str(node_id)
        elif not isinstance(node_id, str):
            raise TypeError(f"The search id needs to be of type int or str! Provided type is {type(node_id)}")

    def write_to_file(self, tree, file_name, xml_declaration=True ,
                      encoding='utf-8', method="xml"):
#        try:
        tree.write(file_name, xml_declaration=xml_declaration,
                   encoding=encoding, method=method)
#        except Exception as e:
#            sys.exit(f"Failed to create minder file: {e}")

if __name__ == '__main__':
    # Create mindmap and get the tree
    mm = mind_map()
    tree = mm.generate_mindmap_metadata()

    # Create nodes
    mm.create_root_node(tree, 'Test-root-node', 'Note Test Test')
    mm.create_new_node(tree, '0', 'First Child Node', note='Child node note test')
    mm.create_new_node(tree, '0', 'Second Child Node', note='Second Child node note test')
    mm.create_new_node(tree, '1', 'First GrandChild Node', note='GrandChild node note test', color='#68b723')
    mm.create_new_node(tree, '1', 'New GrandChild Node', note='New GrandChild node note test', color='#68b723')
    mm.create_new_node(tree, '2', 'Brand New GrandChild Node', note='New GrandChild node note test', color='#68b723')
    mm.create_new_node(tree, '3', "ggchild")

    mm.get_node_by_string(tree,"Child")


    # write file
    mm.write_to_file(tree, 'big_generated.minder', xml_declaration=True, encoding='utf-8',
               method="xml")
    #tree.write('big_generated.minder', xml_declaration=True,encoding='utf-8',
    #           method="xml")
