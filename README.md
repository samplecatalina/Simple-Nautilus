# Simple-Nautilus

# Digest
- Created a Python-based application that mimics the functionalities of a Unix shell with an interactive user interface.

- Implemented built-in commands for: file/directory manipulation, user management, and system permission handling.

- Designed the data structure that maintains a virtual namespace and handles files and folders during program run time.

## [Overview](https://github.com/samplecatalina/Simple-Nautilus#overview)

Simple Nautilus is a Python-based application that mimics the functionalities of a Unix/Linux shell. It provides a wide range of built-in commands for file and directory manipulation, user management, and system information queries. The simulator is designed to be comprehensive and includes permission handling features.

## [Features](https://github.com/samplecatalina/Simple-Nautilus#features)

- **File and Directory Operations**: Create (`mkdir`, `touch`), copy (`cp`), move (`mv`), and delete (`rm`, `rmdir`) files and directories.
    
- **User Management**: Add (`adduser`), delete (`deluser`), and switch (`su`) users.
    
- **System Information**: Display the current working directory (`pwd`) and list directory contents (`ls`).
    
- **Permission Handling**: Change file permissions (`chmod`) and ownership (`chown`).
    

## [Requirements](https://github.com/samplecatalina/Simple-Nautilus#requirements)

- Python 3.x
    

## [Usage](https://github.com/samplecatalina/Simple-Nautilus#overview)

Here are some example usages of the built-in commands:

- To change the current directory:
    
    ```
    cd /path/to/directory
    ```
    
- To create a new directory:
    
    ```
    mkdir new_directory
    ```
    
- To create a new file:
    
    ```
    touch new_file.txt
    ```
    
- To copy a file:
    
    ```
    cp source_file.txt destination_file.txt
    ```
    
- To move a file:
    
    ```
    mv old_location.txt new_location.txt
    ```
    
- To remove a file:
    
    ```
    rm file_to_remove.txt
    ```
    
- To list the contents of a directory:
    
    ```
    ls
    ```
    
- To add a new user:
    
    ```
    adduser username
    ```
    
- To switch to another user:
    
    ```
    su username
    ```