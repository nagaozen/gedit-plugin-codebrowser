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
import os
import re
import subprocess
import tempfile

def iif(condition, trueVal, falseVal):
    if condition:
        return trueVal
    else:
        return falseVal

class ParserInterface:
    
    def parse(self, doc):
        pass
    
    def cellrenderer(self, tvc, crt, ts, piter):
        pass
    
    def pixbufrenderer(self, tvc, crp, ts, piter):
        crp.set_property("pixbuf", "default")
    

class CTagsParser(ParserInterface):
    
    def parse(self, doc):
        code = doc.get_text(*doc.get_bounds())
        lang = doc.get_language()
        
        if not lang:
            return None
        
        lang = self.__get_lang(lang.get_id())
        
        if not lang:
            return None
        
        tags = self.__generate_tags(code, lang)
        ts = self.__tags_to_ts(tags)
        
        return ts
    
    def cellrenderer(self, tvc, crt, ts, piter):
        text = ts.get_value(piter, 0)
        crt.set_property("foreground-gdk", gtk.gdk.Color(0, 0, 0))
        crt.set_property("text", text)
    
    def pixbufrenderer(self, tvc, crp, ts, piter):
        try:
            icon = ts.get_value(piter, 3)
        except:
            icon = "default"
        crp.set_property("pixbuf", iconlib.pixbufs[icon])
    
    def __generate_tags(self, code, lang):
        hdl_code, tmp_code = tempfile.mkstemp()
        hdl_tags, tmp_tags = tempfile.mkstemp()
        
        os.close(hdl_code)
        os.close(hdl_tags)
        
        f = open(tmp_code, 'w')
        f.write(code)
        f.close()
        
        cmd = "ctags --fields=-fst+Kn --sort=no --language-force=%s -f %s %s" %(lang, tmp_tags, tmp_code)
        subprocess.Popen(cmd, shell=True).wait()
        
        os.remove(tmp_code)
        
        return tmp_tags
    
    #
    # NOTE: CTags file format info at <http://ctags.sourceforge.net/ctags.html#TAG FILE FORMAT>
    #
    
    def __tags_to_ts(self, tags):
        ts = gtk.TreeStore(str, str, int, str)
        ts.set_sort_column_id(2, gtk.SORT_ASCENDING)
        
        scopes = []
        indent = "INDENT_UNIT_IS_UNKNOWN"
        
        f = open(tags, 'r')
        for line in f.readlines():
            data = self.__get_line_data(line)
            
            if data:
                tagname    = data[0]
                tagfile    = data[1]
                tagaddress = data[2]
                tagkind    = data[3]
                tagline    = data[4]
                
                if ( indent == "INDENT_UNIT_IS_UNKNOWN" ) and ( tagaddress.startswith(' ') or tagaddress.startswith('\t') ):
                    indent = self.__detect_indent_unit(tagaddress)
                
                lvl = tagaddress.count(indent)
                scopes = scopes[:lvl]
                
                parent = None
                if lvl > 0 and len(scopes) > 0:
                    parent = scopes[len(scopes) - 1]
                
                scopes.append( ts.append(parent , [ tagname, tagfile, tagline, tagkind ]) )
        f.close()
        
        os.remove(tags)
        
        return ts
    
    def __get_line_data(self, line):
        if line.startswith("!_"):
            return None
        
        tagaddress = re.findall(r'\/\^.*\$/;"', line)
        if len(tagaddress) > 0:
            tagaddress = tagaddress.pop()
        else:
            tagaddress = ""
        
        line = re.sub(r'\/\^.*\$/;"', 'TAG_ADDRESS_REMOVED', line)
        tokens = line.strip().split('\t')
        
        tokens[2] = tagaddress[2:len(tokens[2])-4]# ignores regexp and vim compat hacks and get only the ... in /^...$/;"
        tokens[3] = self.__get_type(tokens[0], tokens[2], tokens[3])
        tokens[4] = int(tokens[4].strip().split(":").pop())
        
        return tokens
    
    def __detect_indent_unit(self, line):
        indent = []
        for c in line:
            if c.isspace():
                indent.append(c)
            else:
                break
        return ''.join(indent)
    
    def __get_type(self, tagname, tagaddress, tagkind):
        maps = {
            "array"            : "enum",
            "class"            : "class",
            "constant"         : "const",
            "component"        : "struct",
            "database"         : "database",
            "db_index"         : "db_index",
            "db_procedure"     : "db_procedure",
            "db_table"         : "db_table",
            "db_trigger"       : "db_trigger",
            "db_type"          : "db_type",
            "db_template"      : "db_template",
            "define"           : "typedef",
            "enum constant"    : "enum",
            "enum"             : "enum",
            "enumerator"       : "enum",
            "event"            : "event",
            "externvar"        : "field",
            "feature"          : "method",
            "field"            : "field",
            "format"           : "method",
            "function"         : "method",
            "interface"        : "interface",
            "jsfunction"       : "method",
            "label"            : "proc",
            "local"            : "field",
            "macro"            : "macro",
            "member"           : "method",
            "method"           : "method",
            "module"           : "namespace",
            "mxtag"            : "default",
            "namelist"         : "enum",
            "namespace"        : "namespace",
            "object"           : "object",
            "package"          : "namespace",
            "property"         : "prop",
            "prototype"        : "method",
            "record"           : "struct",
            "set"              : "field",
            "singleton method" : "method",
            "struct"           : "struct",
            "subroutine"       : "proc",
            "table"            : "table",
            "type"             : "struct",
            "typedef"          : "typedef",
            "union"            : "union",
            "variable"         : "field"
        }
        
        try:
            tagkind = maps[tagkind]
            if tagname.startswith("_") or ( tagaddress.lower().find("private") > -1 ):
                tagkind = "%s_priv"%tagkind
            elif tagaddress.lower().find("protected") > -1:
                tagkind = "%s_prot"%tagkind
        except:
            print "<<CodeBrowser>> Warning: Failed to find %s map. Cascading to default." % tagkind
            tagkind = "default"
        
        return tagkind
    
    def __get_lang(self, lang):
        maps = {
            "ant"            : "ant",
            "asm"            : "asm",
            "asp"            : "asp",
            "awk"            : "awk",
            "basic"          : "basic",
            "beta"           : "beta",
            "c"              : "c",
            "c-sharp"        : "c#",
            "cpp"            : "c++",
            "cobol"          : "cobol",
            "dosbatch"       : "dosbatch",
            "eiffel"         : "eiffel",
            "erlang"         : "erlang",
            "flex"           : "flex",
            "fortran"        : "fortran",
            "html"           : "html",
            "java"           : "java",
            "js"             : "js",
            "lisp"           : "lisp",
            "lua"            : "lua",
            "makefile"       : "make",
            "matlab"         : "matlab",
            "objective-caml" : "ocaml",
            "pascal"         : "pascal",
            "perl"           : "perl",
            "php"            : "php",
            "python"         : "python",
            "rexx"           : "rexx",
            "ruby"           : "ruby",
            "scheme"         : "scheme",
            "sh"             : "sh",
            "slang"          : "slang",
            "sml"            : "sml",
            "sql"            : "sql",
            "tcl"            : "tcl",
            "texinfo"        : "tex",
            "vera"           : "vera",
            "verilog"        : "verilog",
            "vhdl"           : "vhdl",
            "vim"            : "vim",
            "yacc"           : "yacc"
        }
        
        try:
            ctags_lang = maps[lang]
        except:
            ctags_lang = None
        
        return ctags_lang
    

# ex:ts=4:et:

