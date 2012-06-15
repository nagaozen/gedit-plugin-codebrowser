# -*- coding: utf-8 -*-

# gEdit CodeBrowser plugin
# Copyright (C) 2011 Fabio Zendhi Nagao
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import os

pixbufs = {
    "class": None,
    "class_priv": None,
    "class_prot": None,
    "const": None,
    "const_priv": None,
    "const_prot": None,
    "enum": None,
    "enum_priv": None,
    "enum_prot": None,
    "event": None,
    "event_priv": None,
    "event_prot": None,
    "exception": None,
    "exception_priv": None,
    "exception_prot": None,
    "field": None,
    "field_priv": None,
    "field_prot": None,
    "interface": None,
    "interface_priv": None,
    "interface_prot": None,
    "macro": None,
    "macro_priv": None,
    "macro_prot": None,
    "method": None,
    "method_priv": None,
    "method_prot": None,
    "namespace": None,
    "namespace_priv": None,
    "namespace_prot": None,
    "object": None,
    "object_priv": None,
    "object_prot": None,
    "proc": None,
    "proc_priv": None,
    "proc_prot": None,
    "prop": None,
    "prop_priv": None,
    "prop_prot": None,
    "struct": None,
    "struct_priv": None,
    "struct_prot": None,
    "typedef": None,
    "typedef_priv": None,
    "typedef_prot": None,
    "union": None,
    "union_priv": None,
    "union_prot": None,
    
    "database": None,
    "db_index": None,
    "db_procedure": None,
    "db_table": None,
    "db_trigger": None,
    "db_type": None,
    "db_template": None,
    "db_view": None,
    
    "default": None,
    "patch": None
}

def populate(plugin):
    for key in pixbufs:
        filename = os.path.join( plugin.get_install_dir(), "codebrowser", "pixmaps", "%s.png" %key )
        pixbufs[key] = gtk.gdk.pixbuf_new_from_file(filename)

# ex:ts=4:et:

