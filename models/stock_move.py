from odoo import _, api, Command, fields, models

from odoo.tools.float_utils import float_compare
from collections import defaultdict


class StockMove(models.Model):
    _inherit = "stock.move"


    def _assign_picking(self):
        Picking = self.env['stock.picking']
        grouped_moves = defaultdict(lambda: self.env['stock.move'])

        for move in self:
            if float_compare(move.product_uom_qty, 0.0, precision_rounding=move.product_uom.rounding) <= 0:
                continue
            grouped_moves[move.product_id.categ_id] |= move

        for category, moves in grouped_moves.items():
            new_picking = Picking.create(moves._get_new_picking_values())
            moves.write({'picking_id': new_picking.id})
            moves._assign_picking_post_process(new=True)

        return True


