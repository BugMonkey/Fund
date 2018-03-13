from io import BytesIO
import requests as rq
from fund_worm import parse_fund as fw
import wx


class fund_window(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "基金网站的数据", size=(450, 400))
        self.panel = wx.Panel(self, -1)
        self.show_textctr()

    def show_pic(self, pic):
        # 网络图片地址
        if pic:
            bmp = wx.Image(BytesIO(rq.get(pic).content), wx.BITMAP_TYPE_ANY, -1)
            bmp = bmp.ConvertToBitmap(-1)
            self.bmp.SetBitmap(bmp)

    def show_textctr(self):

        self.l1 = wx.StaticText(self.panel, pos=(0, 0), label="基金代码 ：")
        self.t1 = wx.TextCtrl(self.panel, pos=(100, 0), style=wx.TE_PROCESS_ENTER)
        self.t1.Bind(wx.EVT_TEXT_ENTER, self.OnEnterPressed)
        self.lname = wx.StaticText(self.panel, pos=(0, 30), label="基金名称 ：")
        self.tname = wx.StaticText(self.panel, pos=(100, 30))
        self.lupanddown = wx.StaticText(self.panel, pos=(0, 60), label="涨跌 ：")
        self.tvalue = wx.StaticText(self.panel, pos=(100, 60))
        self.tper = wx.StaticText(self.panel, pos=(200, 60))
        self.bmp = wx.StaticBitmap(parent=self.panel, pos=(0, 80))

    def OnEnterPressed(self, event):
        parser = fw(event.GetString())
        fund_info = parser.start_parse()
        self.show_result(fund_info)
        self.panel.Refresh()

    def show_result(self, info):
        if info.name:
            self.tname.SetLabel(info.name)
            if info.name == '不存在的基金':
                return
            else:
                if info.rise_fall:
                    fund_z = info.rise_fall()[0]
                    fund_l = info.rise_fall()[1]

                    if '-' in fund_z:
                        self.tvalue.SetForegroundColour((0, 255, 0))
                        self.tper.SetForegroundColour((0, 255, 0))
                    else:
                        self.tvalue.SetForegroundColour((255, 0, 0))
                        self.tper.SetForegroundColour((255, 0, 0))
                    self.tvalue.SetLabel(fund_z)
                    self.tper.SetLabel(fund_l)

                if info.pic:
                    self.show_pic(info.pic)


if __name__ == "__main__":
    app = wx.App()
    frame = fund_window()
    frame.Show()
    app.MainLoop()
