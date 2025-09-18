import customtkinter


class Item(customtkinter.CTkFrame):
    def __init__(self, master, item_name, *args, **kwargs):
        super().__init__(master, *args, **kwargs, fg_color="#1A1A1A", corner_radius=10)

        self.isChecked = customtkinter.BooleanVar(value=False)

        self.label = customtkinter.CTkLabel(self, text=item_name, font=("Arial", 20), text_color="#F0F0F0")
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.columnconfigure(1, weight=1)

        self.checkbox = customtkinter.CTkCheckBox(
            self,
            text=None,
            height=40,
            width=40,
            variable=self.isChecked,
            onvalue=True,
            offvalue=False,
            border_color="#F0F0F0",
        )
        self.checkbox.grid(row=0, column=2, padx=10, pady=10)
