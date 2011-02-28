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
import gedit
from plugin import CodeBrowser
from parsers import *

class CodeBrowserWindowHelper:
    
    ICO = [
        # width height ncolors chars_per_pixel
        "16 16 16 1",
        # colors
        "  c None",
        "1 c #EEEEEC",# Tango Aluminium
        "2 c #D3D7CF",
        "3 c #BABDB6",
        "4 c #888A85",
        "5 c #555753",
        "6 c #2E3436",
        "a c #E9B96E",# Tango Chocolate
        "b c #C17D11",
        "c c #8F5902",
        "d c #729FCF",# Tango Sky Blue
        "e c #3465A4",
        "f c #204A87",
        "g c #AD7FA8",# Tango Plum
        "h c #75507B",
        "i c #5C3566",
        # pixels
        "aaa             ",
        "abc 123456666   ",
        "ccc             ",
        "                ",
        " 3 ddd          ",
        "  3def 123456666",
        " 3 fff          ",
        "                ",
        " 3 ggg          ",
        "  3ghi 1234566  ",
        " 3 iii          ",
        "    3           ",
        " 3  3 ddd       ",
        "    33def 123456",
        " 3    fff       ",
        "                ",
    ]
    
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        self._panel = self._window.get_side_panel()
        
        # Generate the side panel tab icon
        drawable = gtk.gdk.get_default_root_window()
        colormap = drawable.get_colormap()
        pixmap, mask = gtk.gdk.pixmap_colormap_create_from_xpm_d(drawable, colormap, None, self.ICO)
        
        image = gtk.Image()
        image.set_from_pixmap(pixmap, mask)
        
        # Create and assign widget to the panel
        self._codebrowser = CodeBrowser(self._plugin, self._window)
        self._panel.add_item(self._codebrowser, "Code Browser", image)
        
        self.parser = CTagsParser()
    
    def deactivate(self):
        self._panel.remove_item(self._codebrowser)
        self._codebrowser.deactivate()
        self._codebrowser = None
        
        self._panel  = None
        self._window = None
        self._plugin = None
    
    def update_ui(self):
        doc = self._window.get_active_document()
        if doc:
            parser = self.parser
            ts = parser.parse(doc)
            self._codebrowser.set_model(ts, parser)
        else:
            self._codebrowser.set_model(None)
    

class CodeBrowserPlugin(gedit.Plugin):
    
    WINDOW_DATA_KEY = "CodeBrowserPluginWindowData"
    
    def __init__(self):
        gedit.Plugin.__init__(self)
    
    def activate(self, window):
        helper = CodeBrowserWindowHelper(self, window)
        window.set_data(self.WINDOW_DATA_KEY, helper)
    
    def deactivate(self, window):
        window.get_data(self.WINDOW_DATA_KEY).deactivate()
        window.set_data(self.WINDOW_DATA_KEY, None)
    
    def update_ui(self, window):
        window.get_data(self.WINDOW_DATA_KEY).update_ui()
    

# ex:ts=4:et:

