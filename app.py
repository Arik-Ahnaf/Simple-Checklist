import customtkinter, json, logging, sys
from components.task import Task
from components.buttons import AddBtn, DeleteBtn
from PIL import Image, ImageTk
from pathlib import Path


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent
    return base_path / relative_path

LOG_PATH = get_app_dir() / "app.log"
INFO_PATH = get_app_dir() / "info.json"
ICON_PATH = resource_path("logo.png")


logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def ensure_info_json():
    if not INFO_PATH.exists():
        default_data = {"tasks": [], "default_color_theme": "blue", "appearance_mode": "dark"}
        with open(INFO_PATH, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        logging.warning("info.json not found. Created a new one.")
        return default_data
    return None

# Load or initialize data
data = ensure_info_json() or json.load(open(INFO_PATH, "r", encoding="utf-8"))

customtkinter.set_default_color_theme(data.get("default_color_theme", "blue"))
customtkinter.set_appearance_mode(data.get("appearance_mode", "dark"))


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x440")
        self.title("Checklist")

        try:
            self.icon_image = Image.open(ICON_PATH)
            self.icon_photo = ImageTk.PhotoImage(self.icon_image)
            self.iconphoto(False, self.icon_photo)
        except Exception as e:
            logging.warning(f"Could not load icon: {e}")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.pack(padx=10, pady=(10, 0), fill="both", expand=True)

        # load tasks from info.json
        for task_name in data.get("tasks", []):
            task = Task(self.scrollable_frame, task_name)
            task.pack(pady=5, fill="x", expand=True)

        self.add_btn = AddBtn(self.scrollable_frame, self.create_input_window)
        self.add_btn.pack(pady=10)

        self.delete_btn = DeleteBtn(self, self.delete_task)
        self.delete_btn.pack(pady=10)

        self.mainloop()

    def create_input_window(self):
        self.top = customtkinter.CTkToplevel(self)
        self.top.geometry("400x150")
        self.top.title("Add Task")
        try:
            self.icon_image = Image.open(ICON_PATH)
            self.icon_photo = ImageTk.PhotoImage(self.icon_image)
            self.top.iconphoto(False, self.icon_photo)
        except Exception as e:
            logging.warning(f"Could not load icon: {e}")

        self.textbox = customtkinter.CTkEntry(
            self.top,
            placeholder_text="Enter task here",
            width=300,
            font=("sans-serif", 20),
        )
        self.textbox.pack(pady=20)
        self.textbox.focus()

        self.submit_btn = customtkinter.CTkButton(
            self.top,
            text="Submit",
            command=lambda: self.add_task(self.textbox.get().strip()),
            fg_color="#29AE01",
            hover_color="#035800",
            corner_radius=10,
            height=40,
            width=100,
            font=("sans-serif", 20),
        )
        self.submit_btn.pack()

    def add_task(self, text: str = None):
        if not text:
            return
        if len(text) > 120:
            text = text[:120] + "..."
        if text in data["tasks"]:
            logging.info(f"Attempted to add duplicate task: {text}")
            return

        self.add_btn.destroy()
        self.top.destroy()

        task = Task(self.scrollable_frame, text)
        task.pack(pady=5, fill="x", expand=True)

        self.add_btn = AddBtn(self.scrollable_frame, self.create_input_window)
        self.add_btn.pack(pady=5)

        # save the new task to info.json
        data["tasks"].append(text)
        with open(INFO_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Added task: {text}")

    def delete_task(self):
        for task in self.scrollable_frame.winfo_children():
            if isinstance(task, Task) and task.isChecked.get():
                task.destroy()

                if task.label.cget("text") in data["tasks"]:
                    data["tasks"].remove(task.label.cget("text"))
                    with open(INFO_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    logging.info(f"Deleted task: {task.label.cget('text')}")


if __name__ == "__main__":
    App()