# !/usr/bin/env python
"""
MI Errors - All app specific exceptions are defined here.

"""
# --
# Copyright 2012, Model Integration, LLC
# Developer: Leon Starr / leon_starr@modelint.com

# This file is part of the miUML metamodel library.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  The license text should be viewable at
# http://www.gnu.org/licenses/
# --
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# >>> miUML Error Categories

# System
from os import getcwd

# Diagnostic
import pdb

class mi_Error( BaseException ):
    """
    Prints standard error prefix.  Use this when you intend
    to quit but want to print a non-system error message.

    """
    def __init__( self, message ):
        if message:
            print()
            print( "MI Fatal: {}".format( message ) )
            print()

class mi_Quiet_Error( BaseException ):
    """
    Handle error quietly.  (Probably because it was already handled, but we still
    want to notify an outside context that something went wrong without necessarily
    quitting or printing any further messages).

    """
    def __init__( self ):
        pass

class mi_File_Error( BaseException ):
    """
    Cannot access a file or directory.

    """
    def __init__( self, problem, filename ):
        print()
        print( "MI file access: {}\n  File: [{}]\n  In: [{}]".format(
            problem, filename, getcwd() )
        )
        print()

class mi_Parse_Error( BaseException ):
    """
    Problem parsing a record.  Record# is NOT a file line #.

    """
    def __init__( self, problem, filename, record_no, record ):
        print()
        print( "MI parse error: {}\n  File: [{}], Record#[{}]\n  [{}]".format(
                problem, filename, record_no, record )
            )
        print()

class mi_Unpack_Error( BaseException ):
    """
    Line read from file is not recognized

    """
    def __init__( self, problem, filename, line_no, line ):
        print()
        print( "MI unpack error: {}\n  File: [{}], Line[{}]:\n  [{}]".format(
                problem, filename, line_no, line )
            )
        print()

class mi_Command_Error( BaseException ):
    """
    Prints a message about an inappropriate subject provided
    by the user.  It is expected that the user will be prompted
    for further input.

    """
    def __init__( self, message, subject ):
        print( "{}: {}".format( message, subject ) )

class mi_DB_Error( BaseException ):
    """
    """
    def __init__( self, code, message ):
        # We just want the first line 'ERROR: [UI:|SYS:] User message'
        # and ignore the 'ERROR: ' part
        user_parts = message.split('\n')[0].split(':', 2)[1:]
        try:
            if user_parts[0].strip() == 'UI': # most likely case, hopefully
                print( "> " + user_parts[-1].strip() )
                return # Everything is okay on our end, continue as normal
            if len(user_parts) > 1: # If one of our other standard prefixes was supplied
                # SYS is anticipated, but deemed unlikely or impossible
                # A failed ASSERT for all practical purposes
                print( "Editor failed wth [{}] error.".format(user_parts[0].strip()) )
        except:
            print( "--" )
            print( "Unusual error message format received from Postgres DB." )
            print( "Couldn't parse it, so maybe the reporting format changed." )
            print( "Diagnose in the mi_Error / mi_DB_Error class" )
            print( "--" )

        # For all non-UI errors
        print( "MI DB Code: [{}]".format( code ) )
        print("***")
        print( message )
        print("***")
        # RELEASE: Uncomment below
        # exit(1)

# <<< miUML Error Categories

# >>> Command errors
class mi_Syntax_Error( mi_Command_Error ):
    def __init__( self, syntax ):
        super().__init__( "Usage", syntax )

class mi_Arg_Type_Error( mi_Command_Error ):
    def __init__( self, arg_name ):
        super().__init__( "Bad value entered for", arg_name )

class mi_Bad_Set_Value( mi_Command_Error ):
    def __init__( self, subject, set_values ):
        super().__init__( "{} value must be one of".format(subject), set_values )

class mi_Bad_Subject( mi_Command_Error ):
    def __init__( self, subject ):
        super().__init__( "Unknown subject", subject )

class mi_Bad_Op( mi_Syntax_Error ):
    def __init__( self, okops, subject ):
        super().__init__( "< {} > {} args".format( okops, subject ) )

class mi_Bad_Arg( mi_Syntax_Error ):
    def __init__( self, op, subject, arg_syntax ):
        super().__init__( "< {} > {} {}".format( op, subject, arg_syntax ) )

class mi_Compound_Subject( mi_Command_Error ):
    def __init__( self, subject ):
        super().__init__( "Cannot set focus on compound subject", subject )
# <<< Command errors

if __name__ == '__main__':
    print("MI Error Classes defined.")
