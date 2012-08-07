mi_Python_Modules
=================

You need these modules to run any of the mi_ Python code.

They provide general purpose features such as error handling
and file processing used in most mi_ python code.

These files should be in a single directory at the same level as
the directory containing your mi_ code.

For example:  

    Some parent dir/
        Modules/
        mi_Command_Line_Editor/
            miuml.py
            Session.py
            ...
        mi_Postgresql_Function_Code_Generator/
            ...
        

If you look at the headers in the .py files of code that uses
these modules, you will see that they refer to ../Modules
