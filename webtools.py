#!/usr/bin/env python
import sys, os, re, types, shutil

def rmfile(filename,raiseError=1):
    " if file exists, remove it "
    if os.path.isfile(filename): 
        os.remove(filename)
        if os.path.isfile(filename): 
            if raiseError == 1:
                raise (RuntimeError, 'ERROR: Cannot remove %s' % filename)
            else:
                return(1)
    return(0)

def imagestring4web(imagename,width=None,height=None):
    #imstring = '<img src="%s"' % os.path.basename(imagename)
    imstring = '<img src="%s"' % imagename
    if height != None:
        if type(height) is int: height = str(height)
        imstring += '; height=%s' % height
    if width != None:
        if type(width) is int: width = str(width)
        imstring += '; width=%s' % width
    imstring +='>'
    return(imstring)

def vidstring4web(vidname,width=None,height=None):
    """ 
    Function for linking a video to an html table. 
    Give it a directory/file and dimensions in pix.
    """
    #imstring = '<img src="%s"' % os.path.basename(imagename)
    vidstring = '<embed src="%s" autostart="true" loop="true"' % vidname
    if height != None:
        if type(height) is int: height = str(height)
        vidstring += '; height=%s' % height
    if width != None:
        if type(width) is int: width = str(width)
        vidstring += ' width=%s' % width
    vidstring +='> </embed>'
    return(vidstring)

def addlink2string(s,link,target=None):
    line = '<a '
    if target != None:
        line += 'target="%s"' % target
    line += 'href="%s">%s</a>' % (link,s)
    return(line)

def addtag2string(s,tag,target=None):
    line = '<a name="%s"></a>%s' % (tag,s)
    return(line)

class htmltable:
    def __init__(self,Ncols,font=None,fontscale=None,fontsize=None,color=None,bgcolor=None,cellpadding=2,cellspacing=2,border=1,
                 width='100%',height=None,textalign='center',verticalalign='top',optionalarguments=''):
        self.Ncols = Ncols
        self.font  = font
        self.fontscale  = fontscale
        self.fontsize  = fontsize
        self.color      = color
        self.bgcolor    = bgcolor
        self.cellpadding = cellpadding
        self.cellspacing = cellspacing
        self.border      = border
        self.width       = width
        self.height      = height
        self.textalign   = textalign
        self.verticalalign=verticalalign
        self.optionalarguments  = optionalarguments
        self.tabletitle = None
        self.body = []

    def startrow(self,style = ''):
        self.body.append('<tr %s>' % style)
    def endrow(self):
        self.body.append('</tr>\n')

    def addcol(self,colval,link=None, verticalalign=None, textalign=None,
               colspan=None,rowspan=None,
               bold=None, italic=None, underline = None, 
               width=None, height=None, 
               color = None, bgcolor = None, font=None, fontscale=None, fontsize=None):
        if colval is None:
            colval = '-'  # placeholder!
            
        if link != None:
            colval = '<a href="%s">%s</a>' % (link,colval)

        pre   = ''
        after = ''
        #if textalign != None:
        #    pre   += '<%s>'  % (textalign)
        #    after  = '</%s>' % (textalign) + after
        if font != None:
            pre   += '<span style="font-family: %s;">' % (font)
            after  = '</span>' + after
        if fontsize != None:
            if type(fontsize) is str: fontsize = int(fontsize)
            pre   += '<font size=%d>' % (fontsize)
            after  = '</font>' + after
        if fontscale != None:
            pre   += '<font size="%s">' % (fontscale)
            after  = '</font>' + after
        if bold != None and bold != 0:
            pre   += '<b>'
            after  = '</b>'
        if  underline != None and underline != 0:
            pre   += '<u>'
            after  = '</u>'
        if italic != None and italic != 0:
            pre   += '<b>'
            after  = '</b>'
        if color != None:
            if type(color) is int: color = str(color)
            pre   += '<font color=%s>' % (color)
            after  = '</font>' + after
            
        line = '<td'
        if textalign != None:
            line += ' ALIGN="%s"' % textalign            
        if width != None:
            if type(width) is int: width = str(width)
            line += ' WIDTH="%s"' % width            
        if height != None:
            if type(height) is int: height = str(height)
            line += ' HEIGHT="%s"' % height            
        if verticalalign != None:
            line += ' VALIGN="%s"' % verticalalign            
        if bgcolor != None:
            if type(bgcolor) is int: bgcolor = str(bgcolor)
            line += ' BGCOLOR="%s"' % (bgcolor)
        if colspan != None:
            line += ' colspan="%d"' % (colspan)
        if rowspan != None:
            line += ' rowspan="%d"' % (rowspan)
        #if line != '<td':
        #    line += ' NOSAVE'
        line += '>'
        line += pre + colval + after + '</td>'
            
        self.body.append(line)

    def add_sorttablescript_before_header(self):
        return('<script type="text/javascript" src="sortable.js"></script>')

    def settabletitle(self,tabletitle,align='center',fontsize_pt=None,color='white',bgcolor='blue'):
        if tabletitle==None:
            self.tabletitle = None
        
        s = '<div '
        if align!=None: s+='align="%s"; ' % align
        s+= 'style="'
        if fontsize_pt!=None: s+='font-size: %dpt;' % fontsize_pt
        if color!=None: s+='color:%s;' % color
        if bgcolor!=None: s+='background-color:%s;' % bgcolor
        s+= '">'

        self.tabletitle = [s]
        self.tabletitle.append(tabletitle)
        self.tabletitle.append('</div>')
        return(0)

    def gettable(self, sortable=False):

        tableinitstring = '<table '
        # sortable columns?
        if sortable:
            tableinitstring += 'class="sortable" id="anyid" '
        # note: you also have to put the call 

        tableinitstring += 'style="'
        if self.textalign!=None:tableinitstring+='text-align: %s;' % (self.textalign)
        if self.width!=None:tableinitstring+='width: %s;' % (self.width)
        if self.font!=None:tableinitstring+='font-family: %s;' % (self.font)
        if self.fontscale!=None:tableinitstring+='font size: %s;>' % (self.fontscale)
        if self.fontsize!=None:
            tableinitstring+='font size: %d;>' % (int(self.fontsize))
        tableinitstring += '"'
        if self.color!=None:tableinitstring+='color="%s" ' % (self.color)
        if self.bgcolor!=None:tableinitstring+='bgcolor="%s" ' % (self.bgcolor)
        
        tableinitstring += ' COLS=%d BORDER=%d CELLSPACING=%d CELLPADDING=%d %s ' % (self.Ncols,self.border,self.cellspacing,self.cellpadding,self.optionalarguments)
        tableinitstring += '>'


        t=[]
        # Is there a title?
        if self.tabletitle != None: t.extend(self.tabletitle)

        # initialize the table
        t.append(tableinitstring)

        if sortable:
            t.append('<script type="text/javascript" src="sortable.js"></script>')

        # add the body
        t.extend(self.body)

        # close the table
        t.append('</table>')
        t.append('')

        return(t)

        
class webpageclass:
    def __init__(self):
        self.lines=[]
    def substituteplaceholder(self, pattern2find, newlines,count=0):
        import types
        patternobject = re.compile(pattern2find)
        if type(newlines) is str:
            s = newlines
        elif type(newlines) is list:
            s = '\n'.join(newlines)
        else:
            raise(RuntimeError,'Error: unknown type,  dont know how to deal with ',newlines)
        for i in range(len(self.lines)):
            self.lines[i] = patternobject.sub(s,self.lines[i])
        
    def loaddefaultpage(self,filename):
        if not os.path.isfile(filename):
            raise(RuntimeError,'ERROR: could not find file '+filename)
        self.lines = open(filename).readlines()

    def savepage(self,filename):
        # Makesure the directory exists
        dir = os.path.dirname(filename)
        if not os.path.exists(dir):  os.makedirs(dir)  # This is a recursive mkdir
        rmfile(filename)
        f = open(filename,'w')
        f.writelines(self.lines)
        f.close()
