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
import iconlib

class CodeBrowser(gtk.VBox):
    
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        
        gtk.VBox.__init__(self)
        iconlib.populate(self._plugin)
        
        sw = gtk.ScrolledWindow()
        self._browser = gtk.TreeView()
        self._tvc = gtk.TreeViewColumn()
        self._crp = gtk.CellRendererPixbuf()
        self._crt = gtk.CellRendererText()
        
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.add(self._browser)
        
        self._on_row_activated_id = self._browser.connect("row-activated", self.on_row_activated)
        self._browser.props.has_tooltip = True
        self._browser.connect("query-tooltip", self.on_query_tooltip)
        self._browser.get_selection().connect("changed", self.on_selection_changed, self._browser)
        
        self._browser.set_headers_visible(False)
        self._browser.append_column(self._tvc)
        
        self._tvc.pack_start(self._crp, False)
        self._tvc.pack_start(self._crt, False)
        
        self.pack_start(sw)
        self.show_all()
    
    def deactivate(self):
        self._browser.disconnect(self._on_row_activated_id)
        
        if self._browser.get_model():
            self._browser.get_model().clear()
        
        self._crt = None
        self._crp = None
        self._tvc = None
        self._browser = None
        
        self._plugin = None
        self._window = None
    
    def set_model(self, ts, parser = None):
        self._browser.set_model(ts)
        
        if parser:
            self._tvc.set_cell_data_func(self._crp, parser.pixbufrenderer)
            self._tvc.set_cell_data_func(self._crt, parser.cellrenderer)
        self._browser.queue_draw()
        self._browser.expand_all()
    
    def on_row_activated(self, tv, path, tvc):
        model = tv.get_model()
        piter = model.get_iter(path)
        line  = model.get_value(piter, 2)
        
        self._window.get_active_document().goto_line(line - 1)
        self._window.get_active_view().scroll_to_cursor()
    
    def on_query_tooltip(self, widget, x, y, keyboard_tip, tooltip):
        if not widget.get_tooltip_context(x, y, keyboard_tip):
            return False
        else:
            model, path, piter = widget.get_tooltip_context(x, y, keyboard_tip)
            info = model.get(piter, 0, 2, 3)
            name = info[0]
            line = info[1]
            kind = info[2]
            tooltip.set_markup("<b>(%s) <span foreground='#B8CFE7'>%s</span></b> @ line: %s "%(kind, name, line))
            widget.set_tooltip_row(tooltip, path)
            return True
    
    def on_selection_changed(self, selection, tv):
        tv.trigger_tooltip_query()
    

# ex:ts=4:et:

