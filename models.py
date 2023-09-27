class RootFolder:
    def __init__(self, folder_name, parent_folder):
        self.folder_name = folder_name
        self.parent_folder = parent_folder  # parent_folder will be an instance of Folder class
        self.contents = []
        self.contents_file = []  # contents_file list contains instances of File class
        self.contents_folder = []  # contents_folder list contains instances of Folder class


class Folder:
    def __init__(self, folder_name, parent_folder, owner):
        self.folder_name = folder_name
        self.parent_folder = parent_folder  # parent_folder will be an instance of Folder class
        self.contents = []
        self.contents_file = []  # contents_file list contains instances of File class
        self.contents_folder = []  # contents_folder list contains instances of Folder class
        self.str_perm = "drwxr-x"
        self.owner = owner


class File:
    def __init__(self, file_name, parent_folder, owner):
        self.file_name = file_name
        self.parent_folder = parent_folder
        self.str_perm = "-rw-r--"
        self.owner = owner


class User:
    def __init__(self, usr_name, current_folder):
        self.usr_name = usr_name
        self.current_wk_path = ["/"]
        self.current_folder = current_folder  # current_folder will be an instance of Folder class
        self.target_folder = None
        self.folder_pointer = current_folder  # folder_pointer will be used to iterate through name space

    def touch(self, str_target_folder, current_running_usr):
        """
        To create new files.

        :param str_target_folder: path of file to be created.
        :return: None
        """
        ls_elems_of_target_folder = str_target_folder.strip().split("/")
        str_target_folder_name_only = ls_elems_of_target_folder[-1]
        # check if the input is an empty string
        if (ls_elems_of_target_folder[0] == "") and len(ls_elems_of_target_folder) == 1:
            return
        # if <file> is a file name rather than a path, mount <file> under current_folder
        if len(ls_elems_of_target_folder) == 1:
            for i in self.current_folder.contents_folder:
                if i.folder_name == str_target_folder_name_only:
                    return
            for i in self.current_folder.contents_file:
                if i.file_name == str_target_folder_name_only:
                    return
            touched_file = File(file_name=str_target_folder_name_only,
                                parent_folder=self.current_folder,
                                owner=current_running_usr)
            self.current_folder.contents_file.append(touched_file)
        # If <file> is a path, create the file at the corresponding location.
        # If a certain ancestor directory does not exist,
        # the file and any of its ancestor directories will not be created,
        # and error message will be displayed: "touch: Ancestor directory does not exist"
        if len(ls_elems_of_target_folder) > 1:
            # If an absolute path is given (e.g. “/folder1/folder2/folder3”),
            # the first element will be "" (an empty string)
            if ls_elems_of_target_folder[0] == "":
                # move folder_pointer all the way to /
                while True:
                    if self.folder_pointer.parent_folder is None:
                        break
                    self.folder_pointer = self.folder_pointer.parent_folder

            if ls_elems_of_target_folder[0] == "..":
                if self.folder_pointer.parent_folder is not None:
                    self.folder_pointer = self.folder_pointer.parent_folder

            if ls_elems_of_target_folder[0] == ".":
                pass

            tuple_ancestor_check = self.recursive_ancestors_checker(folder_pointer=self.folder_pointer,
                                             ls_elems_of_target_folder=ls_elems_of_target_folder,
                                             recur_depth=1)
            is_ended_ls_elems_of_target_folder = tuple_ancestor_check[0]
            obj_bottom_level_of_existing_dir = tuple_ancestor_check[1]
            idx_of_top_level_of_non_exist_dir = tuple_ancestor_check[3]
            if is_ended_ls_elems_of_target_folder:
                touched_file = File(file_name=ls_elems_of_target_folder[idx_of_top_level_of_non_exist_dir],
                                    parent_folder=obj_bottom_level_of_existing_dir,
                                    owner=current_running_usr)
                obj_bottom_level_of_existing_dir.contents_file.append(touched_file)

            if not is_ended_ls_elems_of_target_folder:
                if (idx_of_top_level_of_non_exist_dir + 1) != ls_elems_of_target_folder[-1]:
                    print("touch: Ancestor directory does not exist")
                    return

    def ls(self, obj_target_folder, is_l):
        if len(obj_target_folder.contents_folder) == 0 and len(obj_target_folder.contents_file) == 0:
            return
        if not is_l:  # -l option is not specified
            if len(obj_target_folder.contents_folder) != 0:
                for j in obj_target_folder.contents_folder:
                    print(j.folder_name + " ", end="")
            if len(obj_target_folder.contents_file) != 0:
                for i in obj_target_folder.contents_file:
                    print(i.file_name + " ", end="")
            print()

        if is_l:  # -l option is specified
            if len(obj_target_folder.contents_folder) != 0:
                for j in obj_target_folder.contents_folder:
                    print(j.str_perm + " " + j.owner.usr_name + " " + j.folder_name)
            if len(obj_target_folder.contents_file) != 0:
                for i in obj_target_folder.contents_file:
                    print(i.str_perm + " " + i.owner.usr_name + " " + i.file_name)

    def pwd(self):
        """
        Print name of current working virtual directory.
        :return: str_pwd: a string of current working directory
        """
        if self.current_folder.parent_folder is None:
            return "/"
        str_pwd = ""
        i = 0
        while i < len(self.current_wk_path):
            if self.current_wk_path[i] == "/":
                str_pwd += self.current_wk_path[i]
            else:
                if i == len(self.current_wk_path) - 1:
                    str_pwd += self.current_wk_path[i]  # do not print a tailing "/" when it is not the end of pwd
                else:
                    str_pwd += self.current_wk_path[i] + "/"
            i += 1
        return str_pwd

    def mkdir(self, str_target_folder, is_recursive, current_running_usr):
        """
        Create the directory <dir>.
        :param str_target_folder: Path of directory to be created
        :param is_recursive: If -p option is specified. If -p is specified, is_recursive will be True.
        :param current_running_usr: The current effective user of the virtual name space.
        :return: None
        """
        ls_elems_of_target_folder = str_target_folder.strip().split("/")
        str_only_target_folder_name = ls_elems_of_target_folder[-1]

        # check if an empty string is given
        if (ls_elems_of_target_folder[0] == "") and len(ls_elems_of_target_folder) == 1:
            return

        # Scenario 1: <dir> is the name of directory to be created straight away.
        if len(ls_elems_of_target_folder) == 1:
        # If -p is not specified and <dir> does exist, print: mkdir: File exists
            if not is_recursive:
                for i in self.current_folder.contents_folder:
                    if i.folder_name == str_only_target_folder_name:
                        print("mkdir: File exists")
                        return
                for i in self.current_folder.contents_file:
                    if i.file_name == str_only_target_folder_name:
                        print("mkdir: File exists")
                        return
            else:
                return
            new_made_dir = Folder(folder_name=str_only_target_folder_name,
                                  parent_folder=self.current_folder,
                                  owner=current_running_usr)
            self.current_folder.contents_folder.append(new_made_dir)

        # Scenario 2: <dir> is the path of directory to be created.
        if len(ls_elems_of_target_folder) > 1:

            # When -p option is not specified, check if any ancestor directory does not exist:
            # If -p is not specified and <dir> does exist, print: mkdir: File exists

            # If an absolute path is given (e.g. “/folder1/folder2/folder3”),
            # the first element will be "" (an empty string)
            if ls_elems_of_target_folder[0] == "":
                # move folder_pointer all the way to /
                while True:
                    if self.folder_pointer.parent_folder is None:
                        break
                    self.folder_pointer = self.folder_pointer.parent_folder

            if ls_elems_of_target_folder[0] == "..":
                if self.folder_pointer.parent_folder is not None:
                    self.folder_pointer = self.folder_pointer.parent_folder

            if ls_elems_of_target_folder[0] == ".":
                pass

            # After the file_pointer is in the right place,
            # recursively iterate through the name space from top to bottom
            # to check if ancestor directories exist.
            #
            # If -p is not specified and any ancestor directory in <dir> does not exist,
            # print: mkdir: Ancestor directory does not exist
            tuple_ancestor_check = self.recursive_ancestors_checker(folder_pointer=self.folder_pointer,
                                                                    ls_elems_of_target_folder=ls_elems_of_target_folder,
                                                                    recur_depth=1)
            is_ended_ls_elems_of_target_folder = tuple_ancestor_check[0]
            obj_bottom_level_of_existing_dir = tuple_ancestor_check[1]
            str_top_level_of_non_exist_dir = tuple_ancestor_check[2]
            idx_of_top_level_of_non_exist_dir = tuple_ancestor_check[3]

            if is_recursive and (not is_ended_ls_elems_of_target_folder):
                if (idx_of_top_level_of_non_exist_dir + 1) != ls_elems_of_target_folder[-1]:
                    self.recursive_folder_creator(obj_head_dir=obj_bottom_level_of_existing_dir,
                                                  ls=ls_elems_of_target_folder,
                                                  idx=idx_of_top_level_of_non_exist_dir,
                                                  current_running_usr=current_running_usr)
                    self.folder_pointer = self.current_folder  # restore the location of folder pointer
                    return

            # -p is not specified, but a directory path is given.
            # According to public test cases, the program is still expected to create the specified directory.
            # if (not is_recursive) and is_ended_ls_elems_of_target_folder:
            if is_ended_ls_elems_of_target_folder:
                self.recursive_folder_creator(obj_head_dir=obj_bottom_level_of_existing_dir,
                                              ls=ls_elems_of_target_folder,
                                              idx=idx_of_top_level_of_non_exist_dir,
                                              current_running_usr=current_running_usr)
                self.folder_pointer = self.current_folder  # restore the location of folder pointer

            if (not is_recursive) and (not is_ended_ls_elems_of_target_folder):
                if (idx_of_top_level_of_non_exist_dir + 1) != ls_elems_of_target_folder[-1]:
                    print("mkdir: Ancestor directory does not exist")
                    self.folder_pointer = self.current_folder  # restore the location of folder pointer
                    return
                else:
                    self.recursive_folder_creator(obj_head_dir=obj_bottom_level_of_existing_dir,
                                                  ls=ls_elems_of_target_folder,
                                                  idx=idx_of_top_level_of_non_exist_dir,
                                                  current_running_usr=current_running_usr)
                    self.folder_pointer = self.current_folder  # restore the location of folder pointer

    def recursive_folder_creator(self, obj_head_dir, ls, idx, current_running_usr):
        """
        Recursively create layers of directories.
        :param obj_head_dir: the top level of layers of directories to be created.
        :param ls: a string of directory layers. e.g. folder1/folder2/folder3
        :param idx: used as a pointer which indicates the next directory to be created.
        :param current_running_usr: the current effective user of the virtual name space.
        :return: None
        """
        tail_folder = Folder(folder_name=ls[idx], parent_folder=obj_head_dir, owner=current_running_usr)
        obj_head_dir.contents_folder.append(tail_folder)
        if idx + 1 >= len(ls):
            return
        self.recursive_folder_creator(tail_folder, ls, idx + 1, current_running_usr=current_running_usr)

    def recursive_ancestors_checker(self, folder_pointer, ls_elems_of_target_folder, recur_depth=1, is_first_time=True):
        """
        Recursively check if all the ancestor directories in a path exists
        :param folder_pointer: points to next directory to be checked.
        :param ls_elems_of_target_folder: a list containing the path of file/folder to be created.
        Each of its element is an ancestor. The last element is the name of file/folder to be created.
        :param recur_depth: The recursive depth of this function,
        and also the index of ancestor being checked in ls_elems_of_target_folder
        :return:
        True/False: "True" means this recursive function has reached the end of ls_elems_of_target_folder,
        indicating that there is already an existing file at the location of this path;
        "False" means this recursive function has reached the end of ls_elems_of_target_folder,
        indicating that there may still be one or more levels of directories to be created.
        folder_pointer will be pointing to the bottom layer of existing directory.
        str_folder_name_to_check will be the first layer of currently non-existing directory.
        index of ls_elems_of_target_folder is the index of the first layer of currently non-existing directory.
        """
        # After the file_pointer is in the right place,
        # recursively iterate through the name space from top to bottom
        # to check if ancestor directories exist.

        # Place those of Folder class in a new list while iterating through all objects within folder_pointer,
        # then use "not in" to see if ancestor directories' name exist in this list.
        # The return value of false indicates the specified str_folder_name_to_check is not found under folder_pointer

        if is_first_time and ls_elems_of_target_folder[0] != "":
            recur_depth -= 1

        str_folder_name_to_check = ls_elems_of_target_folder[recur_depth]  # str... 应该是路径中的第一个非./..的文件夹名
        recur_depth += 1
        # check if the folder name to be checked in this round has reached the end of path
        if recur_depth >= len(ls_elems_of_target_folder):
            return True, folder_pointer, str_folder_name_to_check, recur_depth - 1

        # initialize the starting position of folder_pointer according to the path
        # 根据文件路径来初始化folder_pointer的起始位置：
        if str_folder_name_to_check == ".":
            str_folder_name_to_check = folder_pointer.folder_name
        if str_folder_name_to_check == "..":
            if folder_pointer.parent_folder is None:
                str_folder_name_to_check = folder_pointer.folder_name
            else:
                str_folder_name_to_check = folder_pointer.parent_folder.folder_name

        ls_names_of_folder_pointer_contents = []

        for i in folder_pointer.contents_folder:
            ls_names_of_folder_pointer_contents.append(i.folder_name)
        if str_folder_name_to_check not in ls_names_of_folder_pointer_contents:
            return False, folder_pointer, str_folder_name_to_check, recur_depth - 1
        else:
            # If the ancestor directory at present level exists,
            # call this function again to recursively search contents within this ancestor
            for i in folder_pointer.contents_folder:
                if i.folder_name == str_folder_name_to_check:
                    return self.recursive_ancestors_checker(i, ls_elems_of_target_folder, recur_depth, is_first_time=False)


    def recursive_folder_checker(self, obj_folder, str_name_to_check):
        """
        Recursively check if there is a file/folder with a certain name
        :param obj_folder: the folder to be searched for any same name
        :param str_name_to_check: the name to check
        :return: True/False; true means there is an existing folder/file of str_name_to_check.
        """
        for content in obj_folder.contents_file:
            if content.file_name == str_name_to_check:
                return True
        for content in obj_folder.contents_folder:
            if content.folder_name == str_name_to_check:
                return True
            else:
                if self.recursive_folder_checker(content, str_name_to_check):
                    return True
                return False

    def cd(self, target_path):
        ls_elems_of_target_folder = target_path.strip().split("/")

        # Scenario 1: the length of target_path is 1:
        # target_path is either "."/".." or pointing to file/folder under the present folder
        if len(ls_elems_of_target_folder) == 1:
            # check if the input is empty
            if ls_elems_of_target_folder[0] == "":
                print("cd: Invalid syntax")
                return
            if ls_elems_of_target_folder[0] == ".":
                return
            if ls_elems_of_target_folder[0] == "..":
                if self.current_folder.parent_folder is not None:
                    self.current_folder = self.current_folder.parent_folder
                    self.current_wk_path.pop(-1)
                    self.folder_pointer = self.current_folder
                    return
                else:
                    return

            for i in self.current_folder.contents_file:
                if i.file_name == ls_elems_of_target_folder[0]:
                    print("cd: Destination is a file")
                    return
            is_folder_exist = False
            for i in self.current_folder.contents_folder:
                if i.folder_name == ls_elems_of_target_folder[0]:
                    self.current_folder = i
                    self.current_wk_path.append(i.folder_name)
                    is_folder_exist = True
            if not is_folder_exist:
                print("cd: No such file or directory")
                return

        # Scenario 2: the length of target_path is longer than 1
        if len(ls_elems_of_target_folder) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_target_folder):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_target_folder[i] == "" and i == 0:
                    while True:
                        if self.current_folder.parent_folder is None:
                            self.current_wk_path.clear()
                            self.current_wk_path.append("/")
                            break
                        self.current_folder = self.current_folder.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Point the current_folder to / under this situation.
                    if ls_elems_of_target_folder[1] == "":
                        return
                elif ls_elems_of_target_folder[i] == ".":
                    pass
                elif ls_elems_of_target_folder[i] == "..":
                    if self.current_folder.parent_folder is not None:
                        self.current_folder = self.current_folder.parent_folder
                        self.current_wk_path.pop(-1)
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is not . or ..
                    for j in self.current_folder.contents_file:
                        if j.file_name == ls_elems_of_target_folder[i]:
                            print("cd: Destination is a file")
                            self.current_folder = self.folder_pointer
                            for k in range(0, i):
                                self.current_wk_path.clear()
                                self.current_wk_path.append("/")
                            return
                    is_folder_exist = False
                    for j in self.current_folder.contents_folder:
                        if j.folder_name == ls_elems_of_target_folder[i]:
                            self.current_folder = j
                            self.current_wk_path.append(j.folder_name)
                            is_folder_exist = True
                    if not is_folder_exist:
                        print("cd: No such file or directory")
                        # if any point on the path does not exit, roll back to the original working directory;
                        # folder_pointer was a duplicate of current_folder at initial stage,
                        # so it could be used as a quick path of rolling back.
                        self.current_folder = self.folder_pointer
                        for k in range(0, i):
                            self.current_wk_path.clear()
                            self.current_wk_path.append("/")
                        return
                i += 1

    def cp(self, src_path, dst_path, current_running_usr):
        ls_elems_of_dst = dst_path.strip().split("/")
        ls_elems_of_src = src_path.strip().split("/")

        # pre-check <dst>
        if len(ls_elems_of_dst) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_dst) == 1:
                if ls_elems_of_dst[0] == ".":
                    return
                if ls_elems_of_dst[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_dst[0]:
                        print("cp: Destination is a directory")
                        return

                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_dst[0]:
                        is_file_exist = True
                        print("cp: File exists")
                        return

        if len(ls_elems_of_dst) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_dst):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_dst[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: cp: Source is a directory
                    if ls_elems_of_dst[1] == "":
                        print("cp: Destination is a directory")
                        self.folder_pointer = self.current_folder  # restore the folder_pointer
                        return
                elif ls_elems_of_dst[i] == ".":
                    pass
                elif ls_elems_of_dst[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    # check all elements that are not the last one in ls_elems_of_target_folder
                    # to see if the element's parent exists
                    if i != len(ls_elems_of_dst) - 1:
                        is_parent_exist = False
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                self.folder_pointer = j
                                is_parent_exist = True
                        if not is_parent_exist:
                            print("cp: No such file or directory")
                            self.folder_pointer = self.current_folder
                            return
                    else:
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                print("cp: Destination is a directory")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                        for j in self.folder_pointer.contents_file:
                            if j.file_name == ls_elems_of_dst[i]:
                                print("cp: File exists")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                i += 1

        self.folder_pointer = self.current_folder

        # check <src>

        if len(ls_elems_of_src) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_src) == 1:
                if ls_elems_of_src[0] == ".":
                    return
                if ls_elems_of_src[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_src[0]:
                        print("cp: Source is a directory")
                        return
                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_src[0]:
                        is_file_exist = True
                if not is_file_exist:
                    print("cp: No such file")
                    return

        if len(ls_elems_of_src) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_src):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_src[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: cp: Source is a directory
                    if ls_elems_of_src[1] == "":
                        print("cp: Source is a directory")
                        return
                elif ls_elems_of_src[i] == ".":
                    pass
                elif ls_elems_of_src[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    for j in self.folder_pointer.contents_folder:
                        if j.folder_name == ls_elems_of_src[i]:
                            if i != len(ls_elems_of_src) - 1:
                                self.folder_pointer = j
                                is_file_exist = False
                                for k in self.folder_pointer.contents_file:
                                    if k.file_name == ls_elems_of_src[i]:
                                        is_file_exist = True
                                if (not is_file_exist) and (i == len(ls_elems_of_src) - 1):
                                    print("cp: No such file")
                                    # if any point on the path does not exit,
                                    # roll back to the original working directory;
                                    # folder_pointer was a duplicate of current_folder at initial stage,
                                    # so current_folder could be used as a quick path of rolling back.
                                    self.folder_pointer = self.current_folder
                            else:
                                print("cp: Source is a directory")
                                return
                i += 1

        self.folder_pointer = self.current_folder

        # check <dst>
        if len(ls_elems_of_dst) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_dst) == 1:
                if ls_elems_of_dst[0] == ".":
                    return
                if ls_elems_of_dst[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_dst[0]:
                        print("cp: Destination is a directory")
                        return

                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_dst[0]:
                        is_file_exist = True
                        print("cp: File exists")
                        return

        if len(ls_elems_of_dst) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_dst):
                # 若路径形如 /a/b/c/d/e ， 则将 folder_pointer 重置到根目录下
                if ls_elems_of_dst[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: cp: Source is a directory
                    if ls_elems_of_dst[1] == "":
                        print("cp: Destination is a directory")
                        return
                elif ls_elems_of_dst[i] == ".":
                    pass
                elif ls_elems_of_dst[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    if i != len(ls_elems_of_dst) - 1:
                        is_parent_exist = False
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                self.folder_pointer = j
                                is_parent_exist = True
                        if not is_parent_exist:
                            print("cp: No such file or directory")
                            self.folder_pointer = self.current_folder
                            return
                    else:
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                print("cp: Destination is a directory")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                        for j in self.folder_pointer.contents_file:
                            if j.file_name == ls_elems_of_dst[i]:
                                print("cp: File exists")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return

                        new_made_file = File(file_name=ls_elems_of_dst[-1],
                                             parent_folder=self.folder_pointer,
                                             owner=current_running_usr)
                        self.folder_pointer.contents_file.append(new_made_file)
                        self.folder_pointer = self.current_folder  # restore the folder_pointer
                i += 1


    def mv(self, src_path, dst_path, current_running_usr):
        """
        Move a file src_path to a file dst_path.
        :param src_path: source file's path
        :param dst_path: destination file's path
        :param current_running_usr: current effective user
        :return: None
        """
        ls_elems_of_dst = dst_path.strip().split("/")
        ls_elems_of_src = src_path.strip().split("/")

        # pre-check <dst>
        if len(ls_elems_of_dst) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_dst) == 1:
                if ls_elems_of_dst[0] == ".":
                    return
                if ls_elems_of_dst[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_dst[0]:
                        print("mv: Destination is a directory")
                        return

                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_dst[0]:
                        is_file_exist = True
                        print("mv: File exists")
                        return

        if len(ls_elems_of_dst) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_dst):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_dst[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: mv: Destination is a directory
                    if ls_elems_of_dst[1] == "":
                        print("mv: Destination is a directory")
                        return
                elif ls_elems_of_dst[i] == ".":
                    pass
                elif ls_elems_of_dst[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    # check all elements that are not the last one in ls_elems_of_target_folder
                    # to see if the element's parent exists
                    if i != len(ls_elems_of_dst) - 1:
                        is_parent_exist = False
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                self.folder_pointer = j
                                is_parent_exist = True
                        if not is_parent_exist:
                            print("mv: No such file or directory")
                            self.folder_pointer = self.current_folder
                            return
                    else:
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                print("mv: Destination is a directory")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                        for j in self.folder_pointer.contents_file:
                            if j.file_name == ls_elems_of_dst[i]:
                                print("mv: File exists")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                i += 1

        self.folder_pointer = self.current_folder

        # check <src>

        if len(ls_elems_of_src) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_src) == 1:
                if ls_elems_of_src[0] == ".":
                    return
                if ls_elems_of_src[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_src[0]:
                        print("mv: Source is a directory")
                        return
                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_src[0]:
                        is_file_exist = True
                        self.folder_pointer.contents_file.remove(i)
                if not is_file_exist:
                    print("mv: No such file")
                    return

        if len(ls_elems_of_src) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_src):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_src[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: mv: Source is a directory
                    if ls_elems_of_src[1] == "":
                        print("mv: Source is a directory")
                        return
                elif ls_elems_of_src[i] == ".":
                    pass
                elif ls_elems_of_src[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    is_file_exist = False
                    if i == len(ls_elems_of_src) - 1:
                        for k in self.folder_pointer.contents_file:
                            if k.file_name == ls_elems_of_src[i]:
                                is_file_exist = True
                                self.folder_pointer.contents_file.remove(k)
                    is_folder_exist = False
                    for j in self.folder_pointer.contents_folder:
                        if j.folder_name == ls_elems_of_src[i]:
                            if i != len(ls_elems_of_src) - 1:
                                self.folder_pointer = j
                                is_folder_exist = True
                            else:
                                print("mv: Source is a directory")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                    if not is_folder_exist and not is_file_exist:
                        print("mv: No such file")
                        self.folder_pointer = self.current_folder  # restore the folder_pointer
                        return
                i += 1

        self.folder_pointer = self.current_folder

        # check <dst>
        if len(ls_elems_of_dst) == 1:
            # Scenario 1: the length of target_path is 1:
            # target_path is either "."/".." or pointing to file/folder under the present folder
            if len(ls_elems_of_dst) == 1:
                if ls_elems_of_dst[0] == ".":
                    return
                if ls_elems_of_dst[0] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                        return
                    else:
                        return

                for i in self.folder_pointer.contents_folder:
                    if i.folder_name == ls_elems_of_dst[0]:
                        print("mv: Destination is a directory")
                        return

                is_file_exist = False
                for i in self.folder_pointer.contents_file:
                    if i.file_name == ls_elems_of_dst[0]:
                        is_file_exist = True
                        print("mv: File exists")
                        return

        if len(ls_elems_of_dst) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_dst):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_dst[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Print error message: mv: Source is a directory
                    if ls_elems_of_dst[1] == "":
                        print("mv: Destination is a directory")
                        return
                elif ls_elems_of_dst[i] == ".":
                    pass
                elif ls_elems_of_dst[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    # check all elements that are not the last one in ls_elems_of_target_folder
                    # to see if the element's parent exists
                    if i != len(ls_elems_of_dst) - 1:
                        is_parent_exist = False
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                self.folder_pointer = j
                                is_parent_exist = True
                        if not is_parent_exist:
                            print("mv: No such file or directory")
                            self.folder_pointer = self.current_folder
                            return
                    else:
                        for j in self.folder_pointer.contents_folder:
                            if j.folder_name == ls_elems_of_dst[i]:
                                print("mv: Destination is a directory")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return
                        for j in self.folder_pointer.contents_file:
                            if j.file_name == ls_elems_of_dst[i]:
                                print("mv: File exists")
                                self.folder_pointer = self.current_folder  # restore the folder_pointer
                                return

                        new_made_file = File(file_name=ls_elems_of_dst[-1],
                                             parent_folder=self.folder_pointer,
                                             owner=current_running_usr)
                        self.folder_pointer.contents_file.append(new_made_file)
                        self.folder_pointer = self.current_folder  # restore the folder_pointer for next use
                i += 1

    def rm(self, target_folder: str):
        """
        Remove the file at the path of target_folder.
        :param target_folder: path of file to be removed.
        :return: None
        """
        ls_elems_of_target_folder = target_folder.strip().split("/")

        if len(ls_elems_of_target_folder) == 1:
            is_file_exist = False
            for i in self.current_folder.contents_file:
                if i.file_name == ls_elems_of_target_folder[0]:
                    is_file_exist = True
                    self.current_folder.contents_file.remove(i)
            for i in self.current_folder.contents_folder:
                if i.folder_name == ls_elems_of_target_folder[0]:
                    print("rm: Is a directory")
                    return
            if not is_file_exist:
                print("rm: No such file")
                return

        if len(ls_elems_of_target_folder) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_target_folder):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_target_folder[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Point the current_folder to / under this situation.
                    if ls_elems_of_target_folder[1] == "":
                        return
                elif ls_elems_of_target_folder[i] == ".":
                    pass
                elif ls_elems_of_target_folder[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    is_not_end_of_target_path = False
                    for j in self.folder_pointer.contents_folder:
                        if j.folder_name == ls_elems_of_target_folder[i]:
                            if i != len(ls_elems_of_target_folder) - 1:
                                self.folder_pointer = j
                                is_not_end_of_target_path = True
                                break
                            else:
                                print("rm: Is a directory")
                                self.folder_pointer = self.current_folder  # restore and get prepared for next function
                                return
                    if is_not_end_of_target_path:
                        i += 1
                        continue
                    is_file_exist = False
                    for j in self.folder_pointer.contents_file:
                        if j.file_name == ls_elems_of_target_folder[i]:
                            is_file_exist = True
                            self.folder_pointer.contents_file.remove(j)
                            self.folder_pointer = self.current_folder  # restore and get prepared for next function
                            return
                    if not is_file_exist:
                        print("rm: No such file")
                        self.folder_pointer = self.current_folder  # restore and get prepared for next function
                        return
                i += 1

    def rmdir(self, target_folder: str):
        """
        Remove empty directory.
        :param target_folder: the path of directory to be removed
        :return: None
        """
        ls_elems_of_target_folder = target_folder.strip().split("/")

        if len(ls_elems_of_target_folder) == 1:
            is_file_or_dir_exist = False

            self.folder_pointer = self.current_folder

            if ls_elems_of_target_folder[0] == "":
                while True:
                    if self.folder_pointer.parent_folder is None:
                        break
                    self.folder_pointer = self.folder_pointer.parent_folder

            if ls_elems_of_target_folder[0] == "..":
                if self.current_folder.parent_folder is not None:
                    # point the folder_pointer to the target
                    self.folder_pointer = self.current_folder.parent_folder
                else:
                    print("rmdir: Cannot remove pwd")
                    return

            if ls_elems_of_target_folder[0] == self.folder_pointer.folder_name \
                    or ls_elems_of_target_folder[0] == ".":
                print("rmdir: Cannot remove pwd")
                return

            if ls_elems_of_target_folder[0] == "." or ls_elems_of_target_folder[0] == "..":
                if len(self.folder_pointer.contents_folder) > 0 or len(self.folder_pointer.contents_file) > 0:
                    print("rmdir: Directory not empty")
                    return

            # a folder name has been given:
            for i in self.folder_pointer.contents_file:
                if i.file_name == ls_elems_of_target_folder[0]:
                    is_file_or_dir_exist = True
                    print("rmdir: Not a directory")
                    return

            for i in self.folder_pointer.contents_folder:
                if len(i.contents_file) > 0 or len(i.contents_folder) > 0:
                    print("rmdir: Directory not empty")
                    return
                if i.folder_name == ls_elems_of_target_folder[0]:
                    is_file_or_dir_exist = True
                    # delete the specified folder
                    self.folder_pointer.contents_folder.remove(i)
                    self.folder_pointer = self.current_folder  # restore and get prepared for next function
                    return
            if not is_file_or_dir_exist:
                print("rmdir: No such file or directory")
                return

            if self.folder_pointer == self.current_folder:
                print("rmdir: Cannot remove pwd")
                return

        if len(ls_elems_of_target_folder) > 1:
            # tackle multiple ./..
            i = 0
            while i < len(ls_elems_of_target_folder):
                # If the path is in the format of "/a/b/c/d/e", then point the current_folder to /
                if ls_elems_of_target_folder[i] == "" and i == 0:
                    while True:
                        if self.folder_pointer.parent_folder is None:
                            break
                        self.folder_pointer = self.folder_pointer.parent_folder

                    # If target_path is "/", then ls_elems_of_target_folder should be ["", ""].
                    # Point the current_folder to / under this situation.
                    if ls_elems_of_target_folder[1] == "":
                        if self.folder_pointer.folder_name == self.current_folder.folder_name:
                            print("rmdir: Cannot remove pwd")
                            return
                        else:
                            print("rmdir: Directory not empty")
                            return

                elif ls_elems_of_target_folder[i] == ".":
                    pass
                elif ls_elems_of_target_folder[i] == "..":
                    if self.folder_pointer.parent_folder is not None:
                        self.folder_pointer = self.folder_pointer.parent_folder
                    else:  # already reached /
                        pass
                else:  # when element from ls_elems_of_target_folder is neither . nor ..
                    is_not_end_of_target_path = False
                    for j in self.folder_pointer.contents_folder:
                        if j.folder_name == ls_elems_of_target_folder[i]:
                            self.folder_pointer = j
                            if i != len(ls_elems_of_target_folder) - 1:
                                # if this is not the last folder, the skip the check and start next loop
                                is_not_end_of_target_path = True
                                break
                            else:  # if this is the last folder
                                # check if this is pwd
                                if j.folder_name == self.current_folder.folder_name:
                                    print("rmdir: Cannot remove pwd")
                                    return
                                # check if the folder is empty
                                if len(j.contents_folder) > 0 or len(j.contents_file) > 0:
                                    print("rmdir: Directory not empty")
                                    self.folder_pointer = self.current_folder  # restore and get prepared for next function
                                    return
                                # delete the specified folder
                                self.folder_pointer = j.parent_folder  # move the pointer to a higher level
                                self.folder_pointer.contents_folder.remove(j)
                                self.folder_pointer = self.current_folder  # restore and get prepared for next function
                                return
                    if is_not_end_of_target_path:
                        i += 1
                        continue
                    is_file_exist = False
                    for j in self.folder_pointer.contents_file:
                        if j.file_name == ls_elems_of_target_folder[i]:
                            is_file_exist = True
                            print("rmdir: Not a directory")
                            self.folder_pointer = self.current_folder  # restore and get prepared for next function
                            return
                    if not is_file_exist:
                        # whenever this step is reached,
                        # it means that specified folder is not found under current_folder
                        print("rmdir: No such file or directory")
                        self.folder_pointer = self.current_folder  # restore and get prepared for next function
                        return
                i += 1

    def chown(self, obj_new_owner, target: str):
        """
        Change file owner. Only root user can perform this command.
        :param obj_new_owner: the new owner (of User class) of this file
        :param target: the file path
        :return: None
        """
        ls_elems_of_target = target.strip().split("/")

        is_target_exist = False
        for i in self.folder_pointer.contents_folder:
            if i.folder_name == ls_elems_of_target[0]:
                obj_target = i
                is_target_exist = True
        for i in self.folder_pointer.contents_file:
            if i.file_name == ls_elems_of_target[0]:
                obj_target = i
                is_target_exist = True
        if target == "/":
            return
        if not is_target_exist:
            print("chown: No such file or directory")
            return

        if len(ls_elems_of_target) == 1:
            for i in self.folder_pointer.contents_folder:
                if i.folder_name == ls_elems_of_target[0]:
                    i.owner = obj_new_owner
            for i in self.folder_pointer.contents_file:
                if i.file_name == ls_elems_of_target[0]:
                    i.owner = obj_new_owner

    def chmod(self, str_usr_perms, str_target_path):
        """
        Change file mode bits.
        :param str_usr_perms: is the format string (mode string) in format of [uoa...][-+=][perms...],
        where perms is either zero or more letters from the set rwx.
        :param str_target_path: the file path
        :return: None
        """
        obj_target = None
        is_target_exist = False
        for i in self.folder_pointer.contents_folder:
            if i.folder_name == str_target_path:
                obj_target = i
                is_target_exist = True
        for i in self.folder_pointer.contents_file:
            if i.file_name == str_target_path:
                obj_target = i
                is_target_exist = True
        if str_target_path == "/":
            return
        if not is_target_exist:
            print("chmod: No such file or directory")
            return

        ls_usr_perms = list(str_usr_perms)

        target_usr_char = ls_usr_perms[0]
        operator_char = ls_usr_perms[1]
        ls_perms = list(obj_target.str_perm)

        if len(str_usr_perms) == 3:  # when the [perms] is explicitly specified
            perm_char = ls_usr_perms[2]

            if target_usr_char == "u":
                if operator_char == "+":
                    if perm_char == "r":
                        ls_perms[1] = "r"
                    elif perm_char == "w":
                        ls_perms[2] = "w"
                    elif perm_char == "x":
                        ls_perms[3] = "x"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "-":
                    if perm_char == "r":
                        ls_perms[1] = "-"
                    elif perm_char == "w":
                        ls_perms[2] = "-"
                    elif perm_char == "x":
                        ls_perms[3] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "=":
                    if perm_char == "r":
                        ls_perms[1] = "r"
                        ls_perms[2] = ls_perms[3] = "-"
                    elif perm_char == "w":
                        ls_perms[2] = "w"
                        ls_perms[1] = ls_perms[3] = "-"
                    elif perm_char == "x":
                        ls_perms[3] = "x"
                        ls_perms[1] = ls_perms[2] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                else:
                    print("chmod: Invalid mode")
                    return
            elif target_usr_char == "o":
                if operator_char == "+":
                    if perm_char == "r":
                        ls_perms[4] = "r"
                    elif perm_char == "w":
                        ls_perms[5] = "w"
                    elif perm_char == "x":
                        ls_perms[6] = "x"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "-":
                    if perm_char == "r":
                        ls_perms[4] = "-"
                    elif perm_char == "w":
                        ls_perms[5] = "-"
                    elif perm_char == "x":
                        ls_perms[6] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "=":
                    if perm_char == "r":
                        ls_perms[4] = "r"
                        ls_perms[5] = ls_perms[6] = "-"
                    elif perm_char == "w":
                        ls_perms[5] = "w"
                        ls_perms[4] = ls_perms[6] = "-"
                    elif perm_char == "x":
                        ls_perms[6] = "x"
                        ls_perms[4] = ls_perms[5] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                else:
                    print("chmod: Invalid mode")
                    return
            elif target_usr_char == "a":
                if operator_char == "+":
                    if perm_char == "r":
                        ls_perms[1] = ls_perms[4] = "r"
                    elif perm_char == "w":
                        ls_perms[2] = ls_perms[5] = "w"
                    elif perm_char == "x":
                        ls_perms[3] = ls_perms[6] = "x"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "-":
                    if perm_char == "r":
                        ls_perms[1] = ls_perms[4] = "-"
                    elif perm_char == "w":
                        ls_perms[2] = ls_perms[5] = "-"
                    elif perm_char == "x":
                        ls_perms[3] = ls_perms[6] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                elif operator_char == "=":
                    if perm_char == "r":
                        ls_perms[1] = ls_perms[4] = "r"
                        ls_perms[2] = ls_perms[3] = ls_perms[5] = ls_perms[6] = "-"
                    elif perm_char == "w":
                        ls_perms[2] = ls_perms[5] = "w"
                        ls_perms[1] = ls_perms[3] = ls_perms[4] = ls_perms[6] = "-"
                    elif perm_char == "x":
                        ls_perms[3] = ls_perms[6] = "x"
                        ls_perms[1] = ls_perms[2] = ls_perms[4] = ls_perms[5] = "-"
                    else:
                        print("chmod: Invalid mode")
                        return
                else:
                    print("chmod: Invalid mode")
                    return
            else:
                print("chmod: Invalid mode")
                return

        if len(str_usr_perms) == 2:  # the [perms] is omitted
            if target_usr_char == "u":
                ls_perms[1] = ls_perms[2] = ls_perms[3] = "-"
            elif target_usr_char == "o":
                ls_perms[4] = ls_perms[5] = ls_perms[6] = "-"
            elif target_usr_char == "a":
                ls_perms[1] = ls_perms[2] = ls_perms[3] = ls_perms[4] = ls_perms[5] = ls_perms[6] = "-"
            else:
                print("chmod: Invalid mode")
                return

        str_modified_perms = "".join(ls_perms)
        obj_target.str_perm = str_modified_perms

