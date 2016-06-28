#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from decimal import Decimal
from collections import namedtuple
from itertools import groupby

from sql.aggregate import Sum

from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pyson import Eval, If, Bool
from trytond.transaction import Transaction
from trytond import backend
from trytond.pool import Pool, PoolMeta
from trytond.modules.company import CompanyReport
from trytond.tools import reduce_ids

__all__ = ['Statement']

class Statement():
    __metaclass__ = PoolMeta
    __name__ = 'account.statement'

    @classmethod
    def __setup__(cls):
        super(Statement, cls).__setup__()

    @fields.depends('journal', 'state', 'lines')
    def on_change_journal(self):
        res = {}
        if not self.journal:
            return res

        statements = self.search([
                ('journal', '=', self.journal.id),
                ], order=[
                ('date', 'DESC'),
                ], limit=1)
        if not statements:
            return res

        statement, = statements
        res['start_balance'] = Decimal(0.0)
        return res
