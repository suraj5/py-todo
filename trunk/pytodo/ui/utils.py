import wx

def _prepare(name):
    return 'resources/%s.png' % name

def get_bmp(name):
    img = wx.Bitmap(_prepare(name), wx.BITMAP_TYPE_PNG)
    return img

def get_icon(name):
    return wx.Icon(_prepare(name), wx.BITMAP_TYPE_PNG)
