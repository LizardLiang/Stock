import tkinter as tk


class drawer:
    def __init__(self):
        self.window = tk.Tk()
        self.draw_btn = tk.Button(self.window, text="Draw now")

    def _from_rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        return "#%02x%02x%02x" % rgb

    def draw_stock(self):
        pass

    def main_func(self):
        window = self.window
        window.title("demo")
        window.geometry("800x600")
        window.configure(bg=self._from_rgb((47, 49, 54)))

        draw_btn = self.draw_btn
        draw_btn.pack()
        window.mainloop()


if __name__ == "__main__":
    main_func()