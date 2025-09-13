import customtkinter


class AddBtn(customtkinter.CTkButton):

    def __init__(self, master, command, *args, **kwargs):
        super().__init__(
            master,
            *args,
            **kwargs,
            text="+",
            command=command,
            fg_color="#555555",
            hover_color="#424242",
            corner_radius=10,
            height=40,
            width=100,
            font=("sans-serif", 24)
        )


class DeleteBtn(customtkinter.CTkButton):

    def __init__(self, master, command, *args, **kwargs):
        super().__init__(
            master,
            *args,
            **kwargs,
            text="Delete Selected",
            command=command,
            fg_color="#D90404",
            hover_color="#7A0000",
            corner_radius=10,
            height=40,
            width=100,
            font=("sans-serif", 20)
        )
