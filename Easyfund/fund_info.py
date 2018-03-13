class fund_info():

    # 基金名称

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def set_raise_and_per(self, value, per):
        self._value = value
        self._per = per

        # 涨跌幅

    def rise_fall(self):
        return self._value, self._per

    @property
    def pic(self):
        return self._pic

    @pic.setter
    def pic(self, value):
        self._pic = value
