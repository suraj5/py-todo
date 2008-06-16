import wx

def createMenuItem(parent, menu, label, status=None, handler=None, id=-1, kind=wx.ITEM_NORMAL):
    """
    Create a specific menu item.  If no label is provided, a separator will be
    added automatically.  If no handler is specified, the menu item will remain
    unbound and will probably serve no real purpose.  Otherwise, the menu item
    will be bound to the specified handler.
    """

    if not label:
        menu.AppendSeparator()
    else:
        item = menu.Append(id, label, status, kind)
        if handler:
            parent.Bind(wx.EVT_MENU, handler, item)

def createMenu(parent, menu_data):
    """
    Create a menu for the menu bar.  This will iterate through all child nodes
    and either create a sub menu, or it will simply add a new menu item.
    """

    menu = wx.Menu()
    for item in menu_data:
        if item and len(item) == 2:
            # create a sub menu
            label = item[0]
            submenu = createMenu(parent, item[1])

            menu.AppendMenu(-1, label, submenu)
        else:
            createMenuItem(parent, menu, *item)
    return menu

def buildMenuBar(parent, menus):
    """
    Create the menu bar itself.  Iterate through a collection of data about a
    menu.  These data much follow a fairly specific format in order to be useful.
    """

    menubar = wx.MenuBar()

    for menu_data in menus:
        label, data = menu_data
        menubar.Append(createMenu(parent, data), label)

    return menubar
