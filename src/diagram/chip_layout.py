import math
from src.diagram.bounds import Bounds


class Chip_Layout:
    PART_ASPECT = 4 / 3
    MIN_PART_COLS = 3
    MAX_PARTS_PER_COL = 3
    # describes the desired distributions
    # in the cases of 9 parts or less
    # so that there's more control aesthetically
    INITIAl_PART_DIST = [
        (0, 1, 0),
        (0, 2, 0),
        (1, 2, 0),
        (1, 2, 1),
        (1, 3, 1),
        (2, 2, 2),
        (2, 3, 2),
        (3, 3, 2),
        (3, 3, 3)
    ]

    def distribute_io(group_bounds, io_list):
        for index, io in enumerate(io_list):
            bottom = (((index + 1) * group_bounds.height) / 
                     (len(io_list) + 1) + group_bounds.top)
            # top value isn't used so we just set it
            # to the same value as bottom
            bounds = Bounds(bottom, 
                            group_bounds.left, 
                            bottom, 
                            group_bounds.right) 
            io.layout(bounds)

    def distribute_parts(group_bounds, 
                         parts_list,
                         connections_data,
                         internal_wires, 
                         row_height, 
                         column_width):
        add_col_boundary = (Chip_Layout.MIN_PART_COLS * Chip_Layout.MAX_PARTS_PER_COL) + 1

        num_cols = (Chip_Layout.MIN_PART_COLS 
                    if len(parts_list) < add_col_boundary
                    else math.ceil(len(parts_list) / Chip_Layout.MAX_PARTS_PER_COL))

        ordered_parts = Chip_Layout._order_parts(parts_list, 
                                                 connections_data, 
                                                 internal_wires)
        
        columns = Chip_Layout._distribute_to_cols(ordered_parts, num_cols)

        Chip_Layout._layout_cols(group_bounds, columns, row_height, column_width)    
        
    

    # this will be replaced by a pathfinding
    # algo similar to A* but optimizing for
    # fewer bends, distance travelled, distance to target
    def distribute_connections(connections):
        for index, connection in enumerate(connections):
            zag_fraction= (1 + index) / (1 + len(connections))
            connection.layout(zag_fraction)


    # helper methods
    # -------------------------------------------------------------

    def _snap(value, div_value, snap_lower=True):
        threshold = 0.001
        fractional = (value / div_value) % 1
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

    def _get_connections_by_part_id(part_id, connections):
        part_connections = filter(lambda x: part_id == x["part_id"], 
                                  connections)
        return list(part_connections)

    def _calculate_order_metric(part, connections_data, internal_wires):
        ordering_metric = 0
        part_connections = Chip_Layout._get_connections_by_part_id(part.id, 
                                                                    connections_data)

        # move part to the right for each input it has
        # and more to the right for each input that comes
        # from a part output
        for connection in part_connections:
            is_part_input = connection["part_pin"] in part.input_names
            is_from_part_output = connection["other_pin"] in internal_wires
            if is_part_input:
                ordering_metric += 1
            if is_part_input and is_from_part_output:
                ordering_metric += 1

        # move part to the left for each output it has
        # and more to the left each output that goes
        # to a part input
        for connection in part_connections:
            is_part_output = connection["part_pin"] in part.output_names
            is_going_to_part_input = connection["other_pin"] in internal_wires
            if is_part_output:
                ordering_metric -= 1
            if is_part_output and is_going_to_part_input:
                ordering_metric -= 1

        return ordering_metric
    
    def _order_parts(parts_list, connections_data, internal_wires):
        ordering_lst = []
        
        for part in parts_list:
            ordering_metric = Chip_Layout._calculate_order_metric(part,
                                                                  connections_data, 
                                                                  internal_wires)            

            ordering_lst.append({"part": part, "ordering_metric": ordering_metric})

        ordered_lst = sorted(ordering_lst, key=lambda x: x["ordering_metric"])

        return ordered_lst
    
    def _distribute_to_cols(ordered_parts, num_cols):
        columns = [[] for n in range(num_cols)]
        part_dist = Chip_Layout.INITIAl_PART_DIST[len(ordered_parts) - 1]
        
        for col_index, column in enumerate(columns):
            while not Chip_Layout._is_col_full(len(column), 
                                              part_dist[col_index], 
                                              len(ordered_parts), 
                                              len(Chip_Layout.INITIAl_PART_DIST)):
                column.append(ordered_parts[0]["part"])
                ordered_parts = ordered_parts[1:]

        return columns

    def _is_col_full(num_col_items, col_max, total_items, initial_dist_boundary):
        is_col_full = num_col_items >= col_max
        if total_items > initial_dist_boundary:
            is_col_full = num_col_items >= Chip_Layout.MAX_PARTS_PER_COL
        
        return is_col_full

    def _layout_parts_in_col(group_bounds, 
                         parts_list, 
                         row_height, 
                         column_width):
        
        num_parts = len(parts_list)
        parts_margin = num_parts / (num_parts + 1) * row_height * 2
        part_width = group_bounds.width 
        part_height = part_width * 1 / Chip_Layout.PART_ASPECT
        parts_group_height = (part_height * num_parts +
                              parts_margin * (num_parts - 1))
        centered_group_top = (group_bounds.top + 
                              group_bounds.height / 2 - 
                              parts_group_height / 2)

        for index, part in enumerate(parts_list):
            part_top = (centered_group_top + 
                       index * part_height +
                       index * parts_margin)

            part_bottom = part_top + part_height
            pre_snap_left = (group_bounds.left +
                             group_bounds.width / 2 - 
                             part_width / 2)
            part_left = Chip_Layout._snap(pre_snap_left, 
                                          column_width, 
                                          snap_lower=True)
            pre_snap_right = (group_bounds.left + 
                              group_bounds.width / 2 + 
                              part_width / 2)
            part_right = Chip_Layout._snap(pre_snap_right,
                                           column_width,
                                           snap_lower=False)


            part.layout(Bounds(part_top, 
                               part_left, 
                               part_bottom, 
                               part_right))

    def _layout_cols(group_bounds, columns, row_height, column_width):
        num_cols = len(columns)
        num_margins = num_cols - 1
        col_margin = column_width * 3
        total_margin = col_margin * num_margins
        col_width = (group_bounds.width - total_margin) / num_cols

        for index, column in enumerate(columns):
            col_offset = row_height * 1
            if index % 2 == 0:
               col_offset = -col_offset

            col_bounds = Bounds(group_bounds.top + col_offset,
                                (group_bounds.left + index * 
                                 (col_width + col_margin)),
                                group_bounds.bottom,
                                (group_bounds.left + 
                                 (col_width * (index + 1)) + 
                                 (col_margin * index)))
            
            Chip_Layout._layout_parts_in_col(col_bounds,
                                             column,
                                             row_height,
                                             column_width)