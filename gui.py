import re

from flet import (
    Text,
    Column,
    FloatingActionButton,
    IconButton,
    Row,
    TextField,
    UserControl,
    colors,
    icons,
    ProgressBar,
    AlertDialog,
)

from utils import get_file


links = []


class Task(UserControl):
    """Create a new task(link) object"""

    def __init__(self, task_name, task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        """Pattern for a new task object"""
        self.display_task = Text(value=self.task_name)
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit Link",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete Link",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update Link",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        """Edit handler"""

        self.edit_name.value = self.display_task.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        """Save handler"""

        for i in range(len(links)):
            if links[i] == self.edit_name.value:
                pass

            if links[i] == self.display_task.value:
                links[i] = self.edit_name.value

        self.display_task.value = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        """Delete handler"""
        for i in range(len(links)):
            if links[i] == self.task_name:
                links.remove(links[i])
        self.task_delete(self)


class DownloaderApp(UserControl):
    """Main gui"""

    def build(self):
        """Main page pattern"""
        self.new_task = TextField(hint_text="Please provide me a link", expand=True)
        self.tasks = Column()
        self.progress_text = Text(
            "Downloading files",
            style="headlineSmall",
            text_align="center",
            width=800,
        )
        self.progression = Column(
            visible=False,
            controls=[
                self.progress_text,
                ProgressBar(width=800, color="amber", bgcolor="#eeeeee"),
            ],
        )
        self.dlg = AlertDialog(title=Text("Finished", text_align="center"))
        self.dlg_dl_error = AlertDialog(
            title=Text(
                "There was an error during downloading files", text_align="center"
            )
        )
        self.dlg_already_in_list = AlertDialog(
            title=Text("This link already exists in your list", text_align="center")
        )
        return Column(
            width=800,
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Row(
                    controls=[
                        FloatingActionButton(
                            text="Download", width=800, on_click=self.download
                        )
                    ]
                ),
                self.progression,
                self.tasks,
            ],
        )

    def add_clicked(self, e):
        """Create a new task(link) obj"""
        if len(self.new_task.value) > 0:
            if len(links) == 0:
                if re.search("(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.new_task.value):
                    links.append(self.new_task.value)
                    task = Task(self.new_task.value, self.task_delete)
                    self.tasks.controls.append(task)
            else:
                for i in range(len(links)):
                    if links[i] != self.new_task.value:
                        if re.search(
                            "(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.new_task.value
                        ):
                            task = Task(self.new_task.value, self.task_delete)
                            self.tasks.controls.append(task)
                            links.append(self.new_task.value)
                    else:
                        self.open_dl(self.dlg_already_in_list)

            self.new_task.value = ""
            self.update()

    def open_dl(self, dlg):
        """Open specified dialog"""
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def task_delete(self, task):
        """Delete a task(link) obj"""
        self.tasks.controls.remove(task)
        self.update()

    def download(self, e):
        """Download music from links that are provided"""
        self.progression.visible = True
        self.update()
        download = get_file(links)
        if download != "":
            self.open_dl(self.dlg_dl_error)
        else:
            self.open_dl(self.dlg)
        self.progression.visible = False
        self.update()

    def main_gui(page):
        page.title = "Yt Downloader"
        page.horizontal_alignment = "center"
        page.update()
        app = DownloaderApp(page)
        page.add(app)
        page.add()
