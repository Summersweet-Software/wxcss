# wxcss

> [!IMPORTANT]
> wxcss its not affiliated with the developers of WxWidgets or WxPython
> It simply works _with_ WxPython and is a library to extend it. Thats it.
> The developers of WxWidgets/WxPython will not assist you with bugs in this library.

Wxcss is a very basic package that adds a handful of helper methods that allow you to style widgets using css.

## Why write wxcss?

The reason is simple. I hate using wxpython.

I know that sounds really weird since I am making a wxpython extension. Genuinely though, one of my biggest annoyances with wxpython was the styling. Its the one hold-out I had in fully embracing wxpython over pyqt/pyside. Its what made me _hate_ it. When, really, its not all that bad of a library.

I feel like wxcss at least makes an attempt to solve this problem. It makes me joyful to mess with UI like how I am when working with pyqt/pyside. I hope this package can do the same for you!

## Demo

![Demonstration gif](docs/demo.gif)

> Gif showing multiple edits being made to the css and them being applied once the application is reloaded.

## Basic API

```python

import wxcss
# ... wx imports

class AppFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # * Load the css
        with open("data/default.css", "r") as f:
            css_data = f.read()
            wxcss.apply_css(css_data, self)

        # css loading needs to happen before this call.
        self.Layout()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = AppFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
```

### Apply CSS class to Window/Widget

```python
import wxcss

class MyWidget(wx.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        wxcss.set_class(self, "my-css-class")
```

## Working CSS Features

Below will show you a css example containing all available changeable css properties

```css
/* applied to Frame and Window objects*/
Frame,
Window {
  background-color: #ffffff;
  color: #000000; /*modifies "foreground" attribute"*/
  font-family: papyrus;
  font-size: 10px;
  font-weight: heavier;
  font-style: italic;
  text-decoration: underline;
}

TextCtrl,
StaticText {
  content: "some example text";

  /*The following are very laggy!
    I plan to make these use cython or c for a speedup if possible
  */
  margin: 10px;
  margin-left: 10px;
  margin-right: 12px;

  padding: 20px;
}

/*classes and class element selectors are allowed. Combinators are not supported :( */
Window.some-class {
  min-width: 50px;
  max-width: 100px;
  width: 80x;

  min-height: 50px;
  max-height: 100px;
  height: 80px;

  /* This is still being completed and is buggy/non-functional */
  border-width: 15px;
}
```
