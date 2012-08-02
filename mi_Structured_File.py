#! /usr/bin/env python

"""
Unpacks sections from a structured (.mi) file removing any single line commments,
blank lines and section boundaries.  Indents are preserved, but all new line chars
are stripped.

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

# System
import re

# Local
from mi_Error import *

# Diagnostic
import pdb # debug

_last_line_no = 0 # For error reporting

class Structured_File:
    """
    Structured File - Extracts Sections from a Structured File

    """
    def __init__( self, filename ):
        self.filename = filename # Keep for error reporting
        self.file = None # File handle for filename, structured file to read
        self.line_no = None # For error reporting
        self.sections = {} # One or more sections each with a list of lines
        self.sname = None # Name of the currently open (reading) section
        try:
            self.unpack( self.filename )
        except mi_File_Error:
            exit()
        except mi_Unpack_Error:
            exit()

    def unpack( self, filename ):
        """
        Extract all sections for processing

        """
        try:
            self.file = open( filename )
        except:
            raise mi_File_Error( "Cannot open", filename )

        for n, line in enumerate(self.file, 1):
            line = line.rstrip()
            if line:
                self.line_no = n
                self.process( line.rstrip() )
            _last_line_no = n
        if not self.sections:
            raise mi_File_Error( "No sections found", self.filename )
        if self.sname:
            raise mi_Unpack_Error( "Missing final section end",
                    self.filename, _last_line_no, None )
        self.file.close()

    def process( self, line ):
        """
        Scan regex'es to find a match for this line and call the
        related function.

        """
        for f, p in Structured_File.commands:
            r = p.match( line )
            if r: # Line matches a regex
                if not f:
                    return # No function specified for this match, so skip this line
                f( self, r, line ) # Apply the regex's function to the line
                return
        # Fall through case when no regex matches (incomplete set of regexs defined)
        raise mi_Unpack_Error( "Unrecognized line", self.filename, self.line_no, line )


    # Line processing functions, each triggered by a different regex

    def begin_section( self, r, line ):
        """
        Process beginning of section line

        """
        if self.sname:
            raise mi_Unpack_Error( "Duplicate begin section", self.filename, self.line_no, line )
        self.sname = line[r.end():].strip() # Removes BOS marker and surrounding whitespace
        if not self.sname:
            raise mi_Unpack_Error( "Missing section name", self.filename, self.line_no, line )
        self.sections[self.sname] = []

    def end_section( self, r, line ):
        """
        Process end of section line

        """
        if not self.sname:
            raise mi_Unpack_Error( "Duplicate end section", self.filename, self.line_no, line )
        self.sname = None

    def add_content( self, r, line ):
        """
        Adds content to the current section

        """
        if self.sname:
            self.sections[self.sname].append( line )
        else:
            raise mi_Unpack_Error( "Content outside section", self.filename, self.line_no, line )

# Population
# Assign each line processing function to an appropriate regex
# The regex'es are applied in sequence, so order by most to least restrictive
Structured_File.commands = (
    ( Structured_File.begin_section, re.compile( r'^--' ) ), # Beginning of section
    ( Structured_File.end_section, re.compile( r'^==' ) ), # End of section
    ( None, re.compile( r'^\s*#' ) ), # A single line comment, not processed
    ( Structured_File.add_content, re.compile( r'^.*' ) ) # Anything else
)

if __name__ == '__main__':
    from os import getenv
    from pprint import pprint
    the_SFile = Structured_File( "Resources/api_def.mi" )
    pprint( the_SFile.sections )
