#
# Copyright (c) 2014 iAchieved.it LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

import wx

from binascii import hexlify

from srp import User, NG_1024

def upperHexLong(longvalue):
    return hexlify(long_to_bytes(longvalue)).upper()

class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(350, 400))

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # Labels
        l0 = wx.StaticText(panel, -1, "SRP-6a")
        l0.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        l0.SetSize(l0.GetBestSize())
        
        l1 = wx.StaticText(panel, -1, "Parameters")
        l1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        l1.SetSize(l1.GetBestSize())

        normalLabelFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        lModulusN = wx.StaticText(panel, -1, "Modulus (N) = ")
        lModulusN.SetFont(normalLabelFont)
        lModulusN.SetSize(lModulusN.GetBestSize())

        self.tModulusN = wx.TextCtrl(self, value="N", size=(512,-1))

        lGeneratorG = wx.StaticText(panel, -1, "Generator (g) = ")
        lGeneratorG.SetFont(normalLabelFont)

        self.tGeneratorG = wx.TextCtrl(self, value="g", size=(256,-1))

        lMultiplierK = wx.StaticText(panel, -1, "Multiplier (k) = ")
        lMultiplierK.SetFont(normalLabelFont)

        self.tMultiplierK = wx.TextCtrl(self, value="k", size=(128,-1))

        l2 = wx.StaticText(panel, -1, "Password Database (server-side)")
        l2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        l2.SetSize(l2.GetBestSize())

        l3 = wx.StaticText(panel, -1, "Authentication Protocol")
        l3.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        l3.SetSize(l3.GetBestSize())

        btn = wx.Button(panel, -1, "Close")
        funbtn = wx.Button(panel, -1, "Just for fun...")

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, btn)
        self.Bind(wx.EVT_BUTTON, self.OnFunButton, funbtn)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(l0, 0, wx.ALL, 10)
        sizer.Add(l1, 0, wx.ALL, 10)
        sizer.Add(lModulusN, 0, wx.ALL, 10)
        sizer.Add(self.tModulusN, 0, wx.ALL, 10)
        sizer.Add(lGeneratorG, 0, wx.ALL, 10)
        sizer.Add(self.tGeneratorG, 0, wx.ALL, 10)
        sizer.Add(lMultiplierK, 0, wx.ALL, 10)
        sizer.Add(self.tMultiplierK, 0, wx.ALL, 10)
        sizer.Add(l2, 0, wx.ALL, 10)
        sizer.Add(l3, 0, wx.ALL, 10)
        sizer.Add(btn, 0, wx.ALL, 10)
        sizer.Add(funbtn, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
        panel.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print "See ya later!"
        self.Close()

    def OnFunButton(self, evt):
        """Event handler for the button click."""
        self.user = User("alice", "password123", ng_type=NG_1024)

        (N, g, k) = self.user.get_ngk()

        self.tModulusN.Clear() # Clear it 
        self.tModulusN.WriteText(upperHexLong(N)) # Set it

        self.tGeneratorG.Clear()
        self.tGeneratorG.WriteText(upperHexLong(g))

        self.tMultiplierK.Clear()
        self.tMultiplierK.WriteText(upperHexLong(k))

        

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "SRP-6a")
        self.SetTopWindow(frame)

        frame.Show(True)
        return True


app = MyApp(redirect=True)
app.MainLoop()

