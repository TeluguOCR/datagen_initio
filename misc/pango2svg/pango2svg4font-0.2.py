#!/usr/bin/python
# vim:ts=8:sw=4:expandtab:encoding=utf-8
'''
Pango2SVG4Font Copyright Hashao 2009.
Draw text to a SVG file, with a given font file using pango.
Release under GNU GPL License version 3.0 or later.

ChangeLog:
2009-02-14:
    * Use Ink extent of the layout. might not be the best choice but
      it looks more tidy.
    * Optional margin parameter to draw_svg().
    * Version 0.2.

2009-02-12:
    * Use max of ink and logical size so that we don't cut off some inks.
    * Add a 5 pixel margin.
    * Remove dependency on freetype (not really, fontconfig depends on freetype).
    
2009-02-11:
    * Initial release.
    * Version 0.1
'''
__version__ = "0.1"

import sys
import ctypes
import cairo
import pango
import pangocairo

'''Load font. Derived from:
    http://www.cairographics.org/freetypepython/
    http://code.google.com/p/serif/source/browse/fontview/trunk/src/font-model.c
'''
_initialized = False
_fontconfig_so= None
_fc_current = None
class FontConfigError(Exception):
    pass

def load_font(filename, faceindex=0):
    '''Load a font file to Fontcofig so pango can see it.
    @return: list of font face properties in the font file. The pattern is a
             dictionary of the form:
                 {"family": [family_names...],
                  "style": [style_names...]
                 }

    Basically, it use ctypes to call some fontconfig and freetype functions.
    1. load the font to fontconfig so that pango can see it.
    2. find font pattern datas using fontconfig.

    '''
    global _initialized
    global _fc_current
    global _fontconfig_so

    # load dll and Co.
    if not _initialized:

        # find shared objects

        # initialize FontConfig
        _fontconfig_so = ctypes.CDLL("libfontconfig.so")
        _fontconfig_so.FcConfigGetCurrent.restype = ctypes.c_void_p
        _fc_current = _fontconfig_so.FcConfigGetCurrent();

        _initialized = True

    # load to fontconfig:
    patterns = [] # our return value
    if not _fontconfig_so.FcConfigAppFontAddFile(_fc_current, filename):
        raise FontConfigError, "Failed to Add font file %s." % filename

    # find font face patterns
    fcpattern = ctypes.c_void_p()
    fcblanks = ctypes.c_void_p()
    count = ctypes.c_int()
    fcpattern = _fontconfig_so.FcFreeTypeQuery(filename, faceindex, fcblanks,
            ctypes.byref(count))
    # _fontconfig_so.FcPatternPrint(fcpattern)
    _fontconfig_so.FcPatternDestroy(fcpattern)

    # loop over all the font faces
    FC_FAMILY = "family"
    FC_STYLE = "style"
    for i in range(count.value):
        fcpattern = _fontconfig_so.FcFreeTypeQuery(filename, i, fcblanks,
                ctypes.byref(count))
        _fontconfig_so.FcNameUnparse.restype = ctypes.c_char_p
        
        # loop over all the family names for different locales until we hit a None
        families = []
        pid = 0
        while True:
            family = ctypes.c_char_p()
            _fontconfig_so.FcPatternGetString(fcpattern, FC_FAMILY, pid, 
                    ctypes.byref(family))
            pid += 1
            if not family.value:
                break
            families.append(family.value)

        styles = []
        pid = 0
        while True:
            style = ctypes.c_char_p()
            _fontconfig_so.FcPatternGetString(fcpattern, FC_STYLE, pid, 
                    ctypes.byref(style))
            pid += 1
            if not style.value:
                break
            styles.append(style.value)

        patterns.append({'family': families, 'style': styles})
        # clean up
        _fontconfig_so.FcPatternDestroy(fcpattern)
    return patterns

def setup_cairocontext(surface, fontdesc):
    '''Setup the standard cairocontext so we don't repeat the typing.
    @return: (pango.cairoContext, pango.layout)
    '''
    ctx = cairo.Context(surface)
    cr = pangocairo.CairoContext(ctx)
    layout = cr.create_layout()
    layout.set_font_description(fontdesc)
    return cr, layout

def get_size(txt, fontdesc):
    '''Calculate text dimension when draw in a dummy cairo surface.
    @return: ink extent (x, y, w, h)
    '''
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1,1)
    cr, layout = setup_cairocontext(surface, fontdesc)
    layout.set_text(txt)
    cr.update_layout(layout)
    extents = layout.get_pixel_extents()
    
    surface.finish() #  destroy surface.
    return extents[0]

def draw_svg(extent, txt, fontdesc, fd, margin=2):
    '''Actual draw text to the given svg file handler.'''
    x0, y0, w, h = extent
    w = w + 2*margin
    h = h + 2*margin
    surface = cairo.SVGSurface(fd, w, h)
    cr, layout = setup_cairocontext(surface, fontdesc)

    cr.save()
    #cr.set_source_rgb(1, 1, 1); cr.paint() # Paint white background
    cr.set_source_rgb(0, 0, 0) # black ink color!
    if margin:
        cr.translate(margin, margin)
    cr.translate(-x0, -y0)

    layout.set_text(txt)
    cr.show_layout(layout) # actual draw text to the context.

    cr.restore()
    surface.finish() # 

def create_pango_font_desc(fname, size, faceindex=0):
    '''Create pango font description given a font file.
    @Return: font description list for all the font faces in the font file.
    '''
    patterns = load_font(fname, faceindex)

    descs = []
    for p in patterns:
        family = p['family'][0]
        style = p['style'][0]
        desc = pango.FontDescription("%s, %s %dpx" % (family, style, size))
        descs.append(desc)
    return descs

def txt2svg4font(output, txt, fontfile, fontsize, faceindex=0):
    '''Convenient function to do everything (load font, calculate size,
    generate svg file...).

    @return: the font description used to draw the string.

    All in One function!
    '''
    fontdescs = create_pango_font_desc(fontfile, fontsize, faceindex)
    fontdesc = fontdescs[faceindex]
    extent = get_size(txt, fontdesc)
    fd = open(output, 'w')
    draw_svg(extent, txt, fontdesc, fd)
    return fontdesc

def main():
    if len(sys.argv) != 3:
        print "Pango2SVG4Font (version: %s)" % __version__
        print "Print text to a SVG file, using whatever font file!"
        print 'Usage: %s fontfile.ttf "UTF-8 text"' % sys.argv[0]
        return 2

    fontfile = sys.argv[1]
    txt = sys.argv[2]
    output = 'fun.svg'
    desc = txt2svg4font(output, txt, fontfile, 48, 0)
    print desc
    print "Output: %s" % output

if __name__ == '__main__':
    main()

