# import wxPython
import wx

class Example(wx.Frame):
	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw)

		# function to get response after click
		def onButton(event):
			print("Button")
			st.SetLabel("GeeksforGeeks")

		# static text
		st = wx.StaticText(self, label ="Welcome to ")

		# create b{button.label}utton
		button = wx.Button(self, wx.ID_ANY, 'Test', (10, 40))

		# bind onButton() function with button
		button.Bind(wx.EVT_BUTTON, onButton)

def main():
	app = wx.App()
	ex = Example(None)
	ex.Show()
	app.MainLoop()

if __name__ == '__main__':
	main()

