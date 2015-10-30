#*********************************************************************
# File : checkbookReport.py
# Date: 9/8/2015
# Author: Allen Kirby
# Purpose: Generate reports for a checkbook
#*********************************************************************


from Constants import config
import locale

REPORT_TYPES = ["Monthly", "Total"]
headerFormat = "{:*^40}"

class CheckbookReport:

    def __init__(self, cb):
        """Initializes the report with the specified checkbook
        Parameter:
            cb (Checkbook) : the checkbook to operate on
        """
        self.checkbook = cb

    def genReport(self):
        """Generates an Expense report for all Debit transactions"""
        transTotal = abs(self.checkbook.getTotalForTrans("Debit"))
        payTotal = self.checkbook.getTotalForCat("Paycheck")
        formatString = "{:<12}"
        print("\n" + headerFormat.format(" REPORT ") + "\n")
        print(formatString.format("Pay Total"), ":",
              locale.currency(payTotal, grouping=config.THOUSAND_SEP))
        print(formatString.format("Debit Total"), ":",
              locale.currency(transTotal, grouping=config.THOUSAND_SEP))
        print(formatString.format("Savings"), ":",
              locale.currency(payTotal - transTotal, grouping=config.THOUSAND_SEP))
        print() # add extra space before printing categories
        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            print(cat)
            for cbt in currentCatList:
                total += abs(cbt.getAmount())

            print("  " + "{:.2%}".format(total / transTotal),
                  "(" + locale.currency(total, grouping=config.THOUSAND_SEP) + ")")
        print("\n" + headerFormat.format(" END REPORT ") + "\n")

    def genMonthlyReport(self, month):
        """Generates an Expense report for all Debit transactions for the specified month
        Parameters:
            month : an integer representing the month used to generate the report
        """
        transTotal = abs(self.checkbook.getTotalForTransMonth("Debit", month))
        payTotal = self.checkbook.getTotalForCatMonth("Paycheck", month)
        formatString = "{:<12}"
        print("\n" + headerFormat.format(" MONTHLY REPORT ") + "\n")
        print(formatString.format("Pay Total"), ":",
              locale.currency(payTotal, grouping=config.THOUSAND_SEP))
        print(formatString.format("Debit Total"), ":",
              locale.currency(transTotal, grouping=config.THOUSAND_SEP))
        print(formatString.format("Savings"), ":",
              locale.currency(payTotal - transTotal, grouping=config.THOUSAND_SEP))
        print() # add extra space before printing categories

        for cat in config.DEBIT_CATEGORIES:
            currentCatList = self.checkbook.getCategory(cat)
            total = 0
            print (cat)
            for cbt in currentCatList:
                date = cbt.getDate().month
                if date == month:
                    total += abs(cbt.getAmount())

            print("  " + "{:.2%}".format(total / transTotal),
                  "(" + locale.currency(total, grouping=config.THOUSAND_SEP) + ")")
                    
        print("\n" + headerFormat.format(" END REPORT ") + "\n")

    # A dictionary used to more generically call the methods for this class
    dispatcher = {
        REPORT_TYPES[0] : genMonthlyReport,
        REPORT_TYPES[1] : genReport
    }
