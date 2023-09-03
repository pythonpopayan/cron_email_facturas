import os
import re
import shutil
import argparse
from typing import List


class InboxManager:
    """InboxManager, which is responsible for organizing and cleaning email inbox files.

    The class has the following attributes:
    - current_dir: stores the absolute path of the current directory
    - title_regx: a regular expression pattern used to extract information from email file names
    - attatchment_regx: a regular expression pattern used to extract information from attachment file names
    - target_folder: the target folder where the email files and attachments will be organized
    - html_files: a list to store the paths of all HTML email files
    - attatchment_files: a list to store the paths of all attachment files
    - years: a list to store the years of the emails
    - actions: a dictionary that maps supported actions to their corresponding methods
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    title_regx = re.compile(
        r"(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-.+-\d+.html"
    )
    attatchment_regx = re.compile(r"href=.(?P<attatchment>Attachments-\d+)\/.+")
    target_folder = ""
    html_files = []
    attatchment_files = []
    years = []
    actions = {}

    def __init__(self) -> None:
        """initializes the actions dictionary
        with supported actions and their corresponding methods"""
        self.actions = {
            "organize": self.organize_emails,
            "clean": self.clean_attatchments,
        }

    @property
    def supported_actions(self):
        """a property that returns a list of supported actions"""
        return self.actions.keys()

    @property
    def supported_actions_docs(self):
        """a property that returns a string containing the
        documentation of supported actions"""
        points = "\n- ".join(
            (f"{k}: {v.__doc__.strip()}" for k, v in self.actions.items())
        )
        return "\n- " + points

    def execute(self, action, folder):
        """executes the specified action on the given folder"""
        fn = self.actions.get(action)
        fn(folder)

    def clean_attatchments(self, *args):
        """Delete attatchment from deleted emails that were not relevant"""
        folder = args[0]
        folder = os.path.abspath(folder)
        self.sort_files_by_type(folder)
        survivor_attatchment = set()
        for ht in self.html_files:
            att = self.get_contents_associated(ht)
            for fl in att:
                if fl:
                    survivor_attatchment.add(os.path.join(self.target_folder, fl))
        all_attatchments = set(self.attatchment_files)
        to_delete = all_attatchments.difference(survivor_attatchment)
        for itm in to_delete:
            shutil.rmtree(itm)

    def organize_emails(self, *args):
        """Organize emails by year and pack them for accountant"""
        target_folder = args[0]
        self.sort_files_by_type(target_folder)
        self.sort_files_by_year()
        self.pack_attatchments()

    def sort_files_by_type(self, target_folder: List):
        """sorts files in the target folder into HTML email
        files and attachment files"""
        self.target_folder = os.path.abspath(target_folder)
        for a in os.listdir(self.target_folder):
            f_path = os.path.join(self.target_folder, a)
            if a.endswith(".html") and os.path.isfile(f_path):
                self.html_files.append(f_path)
            elif os.path.isdir(f_path):
                self.attatchment_files.append(f_path)

    def assert_folder(self, target) -> str:
        """creates a folder if it does not exist and
        returns its absolute path"""
        folder = os.path.join(self.current_dir, target)
        if not os.path.exists(folder):
            os.mkdir(folder)
        return folder

    def get_contents_associated(self, content: str) -> List:
        """reads the contents of an HTML email file and
        extracts the attachment file name"""
        try:
            with open(content, "r") as fl:
                txt = fl.read()
        except Exception as err:
            print(content)
            print(err)
            with open(content, "r", encoding="latin") as fl:
                txt = fl.read()

        raw = self.attatchment_regx.search(txt)
        try:
            resp = raw["attatchment"]
        except Exception as err:
            resp = None
        return [resp]

    def move_content_to_folder(self, content, target):
        """moves a file and its associated attachments
        to a target folder"""
        dest_folder = os.path.join(self.current_dir, target)
        shutil.copy2(content, dest_folder)
        contents_associated = self.get_contents_associated(content)
        for cnt in contents_associated:
            if cnt:
                shutil.copytree(
                    os.path.join(self.target_folder, cnt),
                    os.path.join(dest_folder, cnt),
                )

    def sort_files_by_year(self):
        """sorts email files by year and moves them to
        the corresponding year folder"""
        for ht in self.html_files:
            raw = self.title_regx.search(ht.split("/")[-1])
            doc_year = raw.group("year")
            if doc_year not in self.years:
                self.years.append(doc_year)
                self.assert_folder(doc_year)
                self.move_content_to_folder(ht, doc_year)
            else:
                self.move_content_to_folder(ht, doc_year)

    def pack_attatchments(self):
        """a placeholder method for packing
        attachments (not implemented)"""
        pass


if __name__ == "__main__":
    manager = InboxManager()
    parser = argparse.ArgumentParser(
        description="List files in a folder and apply a user-defined sort function."
    )
    parser.add_argument(
        "action",
        type=str,
        help=f"action to do {manager.supported_actions_docs}",
        choices=manager.supported_actions,
    )
    parser.add_argument("folder_path", type=str, help="Path to the folder")

    args = parser.parse_args()
    folder_path = args.folder_path
    action = args.action

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
    else:
        manager.execute(action, folder_path)
