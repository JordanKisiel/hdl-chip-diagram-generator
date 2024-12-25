from src.diagram.bounds import Bounds

class Chip_Layout:
    PART_ASPECT = 4 / 3

    def distribute_io(group_bounds, io_list):
        for index, io in enumerate(io_list):
            bottom = (((index + 1) * group_bounds.height) / 
                     (len(io_list) + 1) + group_bounds.top)
            # top value isn't used so we just set it
            # arbitrarily to 100 pixels above the bottom
            bounds = Bounds(bottom - 100, 
                            group_bounds.left, 
                            bottom, 
                            group_bounds.right) 
            io.layout(bounds)

    def distribute_parts(group_bounds, 
                         parts_list, 
                         row_height, 
                         column_width):
        parts_margin = row_height / len(parts_list)
        part_height = (group_bounds.height / 
                       len(parts_list) - 
                       (2 * parts_margin))
        part_width = part_height * Chip_Layout.PART_ASPECT

        for index, part in enumerate(parts_list):
            if index == 0:
                top_margin = 0
                bottom_margin = parts_margin * 2
            elif index < len(parts_list) - 1:
                top_margin = parts_margin
                bottom_margin = parts_margin
            else:
                top_margin = parts_margin * 2
                bottom_margin = 0

            if len(parts_list) == 1:
                bottom_margin = 0

            part_top = ((group_bounds.top + 
                        (index * group_bounds.height) / 
                        len(parts_list)) +
                        top_margin)
            part_bottom = ((group_bounds.top + 
                           (((index + 1) * 
                           group_bounds.height)) /
                           len(parts_list)) -
                           bottom_margin)
            pre_snap_left = (group_bounds.left +
                             (group_bounds.width / 2) - 
                             (part_width / 2))
            part_left = Chip_Layout._snap(pre_snap_left, 
                                          column_width, 
                                          snap_lower=True)
            pre_snap_right = (group_bounds.left + 
                              (group_bounds.width / 2) + 
                              part_width / 2)
            part_right = Chip_Layout._snap(pre_snap_right,
                                           column_width,
                                           snap_lower=False)


            part.layout(Bounds(part_top, part_left, part_bottom, part_right))

    def _snap(value, div_value, snap_lower=True):
        threshold = 0.001
        divisions = value / div_value
        fractional = divisions % 1
        if fractional < threshold:
            return value
        if 1 - fractional < threshold:
            return value
        
        if snap_lower:
            rounding = value % div_value
            return value - rounding
        else:
            rounding = 1 - (value % div_value)
            return value + rounding
