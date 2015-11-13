#*********************************************************************
# File    : commands.py
# Date    : 9/3/2015
# Author  : Allen Kirby
# Purpose : commands that are used at the CLI
#*********************************************************************

HELP_COMMAND  = "help"          # prints the help
ADD_COMMAND   = "add"           # adds a transaction
PRINT_COMMAND = "print"         # prints the checkbook
SAVE_COMMAND  = "save"          # saves the checkbook
EDIT_COMMAND = "edit"           # edit a transaction
REPORT_COMMAND = "report"       # generate a report
LOAD_COMMAND = "load"           # load an XML file

EXIT_LIST = ["Quit", "quit", "Exit", "exit", "q"] # the commands that exit the program
GUI_COMMAND_LIST = [ADD_COMMAND, EDIT_COMMAND, REPORT_COMMAND, LOAD_COMMAND, SAVE_COMMAND, EXIT_LIST[0]]
helpHeadersFormat = "{:*^35}"
topHelpHeader = helpHeadersFormat.format(" HELP ")
botHelpHeader = helpHeadersFormat.format(" END HELP ")
# displays when the help command is executed
EXIT_HELP = """
How to exit:
    Quit/quit
    Exit/exit
    q
"""
COMMAND_HELP = """
Commands:
    help   : Prints this help
    add    : Add a transaction to the checkbook
    print  : Print the checkbook 
    save   : Save the checkbook
    edit   : Edit a transaction
    report : Generate a report about the transactions
"""
HELP_TEXT = ("""
{}
""" + EXIT_HELP + COMMAND_HELP + """
{}
""").format(topHelpHeader, botHelpHeader)
