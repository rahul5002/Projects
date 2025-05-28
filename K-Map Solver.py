import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
from itertools import product

class KMapSolver:
    """Enhanced K-Map Solver with support for more variables and matplotlib visualization"""
    
    def __init__(self):
        self.max_vars = 6 
        self.colors = list(mcolors.TABLEAU_COLORS)
        
    def gray_code(self, bits):
        """Generate Gray code sequence for given number of bits"""
        return [i ^ (i >> 1) for i in range(2 ** bits)]
    
    def create_kmap(self, num_vars, minterms=None, dont_cares=None):
        """Create a K-map with specified variables, minterms, and don't cares"""
        if num_vars < 2 or num_vars > self.max_vars:
            print(f"Error: Only 2 to {self.max_vars} variables are supported")
            return None, None, None, None
        
        minterms = minterms or []
        dont_cares = dont_cares or []
        
        default_var_names = ['A', 'B', 'C', 'D', 'E', 'F'][:num_vars]
        
        # Setup K-map dimensions - split variables as evenly as possible
        row_vars = num_vars // 2
        col_vars = num_vars - row_vars
        
        rows = 2 ** row_vars
        cols = 2 ** col_vars
        
        # Create K-map grid (0=False, 1=True, 2=Don't Care)
        kmap = np.zeros((rows, cols), dtype=int)
        
        # Generate Gray code ordering
        row_gray = self.gray_code(row_vars)
        col_gray = self.gray_code(col_vars)
        
        # Fill K-map with values
        for r in range(rows):
            for c in range(cols):
                row_bits = format(row_gray[r], f'0{row_vars}b')
                col_bits = format(col_gray[c], f'0{col_vars}b')
                binary = row_bits + col_bits
                cell_value = int(binary, 2)
                
                # Set cell value based on minterms and don't cares
                if cell_value in minterms:
                    kmap[r, c] = 1
                elif cell_value in dont_cares:
                    kmap[r, c] = 2
        
        return kmap, default_var_names, row_gray, col_gray
    
    def plot_kmap(self, kmap, var_names, row_gray, col_gray, implicant_groups=None):
        """Display the K-map using matplotlib with optional implicant grouping"""
        rows, cols = kmap.shape
        num_vars = len(var_names)
        row_vars = num_vars // 2
        col_vars = num_vars - row_vars
        
        # Create figure and axes
        fig, ax = plt.subplots(figsize=(max(8, cols*1.5), max(6, rows*1.5)))
        
        # Set up the plot
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        
        # Generate labels for rows and columns using Gray code
        row_labels = [format(code, f'0{row_vars}b') for code in row_gray]
        col_labels = [format(code, f'0{col_vars}b') for code in col_gray]
        
        # Add row and column headers
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels[::-1])  # Reverse row labels to match traditional K-map
        
        # Set variable labels
        row_var_str = ''.join(var_names[:row_vars])
        col_var_str = ''.join(var_names[row_vars:])
        ax.set_xlabel(f"Variables: {col_var_str}")
        ax.set_ylabel(f"Variables: {row_var_str}")
        
        # Add grid
        ax.grid(True, linestyle='-', alpha=0.7)
        
        # Fill cells with values
        for r in range(rows):
            for c in range(cols):
                y = rows - 1 - r  # Invert for visual representation
                if kmap[r, c] == 0:
                    text = "0"
                    color = 'white'
                elif kmap[r, c] == 1:
                    text = "1"
                    color = 'lightblue'
                else:  # Don't care
                    text = "X"
                    color = 'lightgray'
                
                ax.add_patch(Rectangle((c-0.5, y-0.5), 1, 1, facecolor=color, alpha=0.5))
                ax.text(c, y, text, ha='center', va='center', fontsize=12, fontweight='bold')
                
                # Get decimal value of the cell and add it as small text
                row_bits = format(row_gray[r], f'0{row_vars}b')
                col_bits = format(col_gray[c], f'0{col_vars}b')
                decimal = int(row_bits + col_bits, 2)
                ax.text(c, y-0.3, str(decimal), ha='center', va='center', fontsize=8, alpha=0.7)
        
        # Highlight implicant groups if provided
        if implicant_groups:
            self._draw_implicant_groups(ax, kmap, row_gray, col_gray, implicant_groups, rows, cols)
        
        plt.title(f"K-Map ({num_vars} variables)")
        plt.tight_layout()
        plt.show()
    
    def _draw_implicant_groups(self, ax, kmap, row_gray, col_gray, implicant_groups, rows, cols):
        """Draw rectangles around implicant groups"""
        color_idx = 0
        num_vars = len(bin(row_gray[0])[2:]) + len(bin(col_gray[0])[2:])
        row_vars = num_vars // 2
        col_vars = num_vars - row_vars
        
        for i, (group, size) in enumerate(implicant_groups):
            # Convert decimal values to row, col positions
            positions = []
            for decimal in group:
                binary = format(decimal, f'0{num_vars}b')
                row_bits = binary[:row_vars]
                col_bits = binary[row_vars:]
                # Find position in Gray code
                row_idx = row_gray.index(int(row_bits, 2))
                col_idx = col_gray.index(int(col_bits, 2))
                positions.append((row_idx, col_idx))
            
            # Determine if it's a rectangular group
            if self._is_rectangular_group(positions, rows, cols):
                # Draw rectangle around the group
                color = self.colors[color_idx % len(self.colors)]
                color_idx += 1
                
                # Get rectangle bounds (with wrap-around handling)
                min_row, max_row, min_col, max_col = self._get_group_bounds(positions, rows, cols)
                
                # Adjust for inverted y-axis
                min_y = rows - 1 - max_row - 0.5
                max_y = rows - 1 - min_row + 0.5
                
                if self._is_wrapped_group(positions, rows, cols):
                    # For wrapped groups, draw multiple rectangles
                    self._draw_wrapped_group(ax, positions, rows, cols, color)
                else:
                    # Draw single rectangle
                    width = (max_col - min_col) + 1
                    height = (max_row - min_row) + 1
                    rect = Rectangle((min_col-0.5, min_y), width, height, 
                                    fill=False, edgecolor=color, linewidth=2.5)
                    ax.add_patch(rect)
    
    def _is_rectangular_group(self, positions, rows, cols):
        """Check if positions form a rectangular group (possibly wrapped)"""
        # This is a simplified check - full implementation would detect valid K-map groups
        # For now, return True for all groups to show them
        return True
    
    def _get_group_bounds(self, positions, rows, cols):
        """Get min/max row and column, handling wrapped groups"""
        row_positions = [r for r, _ in positions]
        col_positions = [c for _, c in positions]
        
        min_row, max_row = min(row_positions), max(row_positions)
        min_col, max_col = min(col_positions), max(col_positions)
        
        return min_row, max_row, min_col, max_col
    
    def _is_wrapped_group(self, positions, rows, cols):
        """Check if the group wraps around the K-map edges"""
        row_positions = [r for r, _ in positions]
        col_positions = [c for _, c in positions]
        
        row_diff = max(row_positions) - min(row_positions)
        col_diff = max(col_positions) - min(col_positions)
        
        # If the difference is almost the entire dimension, it might be wrapped
        return row_diff >= rows-1 or col_diff >= cols-1
    
    def _draw_wrapped_group(self, ax, positions, rows, cols, color):
        """Draw rectangles for wrapped groups"""
        # Convert positions to inverted y coordinates
        positions = [(r, c, rows-1-r) for r, c in positions]
        
        # For each position, draw a small rectangle
        for r, c, y in positions:
            rect = Rectangle((c-0.5, y-0.5), 1, 1,
                            fill=False, edgecolor=color, linewidth=2.5)
            ax.add_patch(rect)
    
    def find_implicants(self, kmap, row_gray, col_gray, minterms, dont_cares):
        """Find prime implicants in the K-map using Quine-McCluskey inspired approach"""
        rows, cols = kmap.shape
        row_vars = len(format(row_gray[0], 'b'))  # Calculate row bits
        col_vars = len(format(col_gray[0], 'b'))  # Calculate col bits
        num_vars = row_vars + col_vars
        
        # Helper function to get decimal value of a cell
        def get_decimal(r, c):
            row_bits = format(row_gray[r], f'0{row_vars}b')
            col_bits = format(col_gray[c], f'0{col_vars}b')
            return int(row_bits + col_bits, 2)
        
        # Helper to check if position is valid with wrapping
        def is_valid_pos(r, c):
            wrapped_r = r % rows
            wrapped_c = c % cols
            return kmap[wrapped_r, wrapped_c] > 0
        
        # Find all possible groups of sizes 2^n
        all_groups = []
        
        # Start with single cells
        for r in range(rows):
            for c in range(cols):
                if kmap[r, c] > 0:  # 1 or don't care
                    decimal = get_decimal(r, c)
                    all_groups.append(([decimal], 1))
        
        # Check powers of 2 up to the size of the K-map
        max_size = min(2**num_vars, rows*cols)
        size = 2
        while size <= max_size:
            height_options = [1]
            if size >= rows:
                height_options.append(rows)
            for h in range(2, rows+1):
                if h & (h-1) == 0 and h <= size:  # If h is a power of 2
                    height_options.append(h)
            
            for height in height_options:
                width = size // height
                if width > cols:
                    continue
                if width & (width-1) != 0:  # If width is not a power of 2
                    continue
                
                # Check each possible position
                for r in range(rows):
                    for c in range(cols):
                        valid_group = True
                        cells = []
                        
                        # Check all cells in the potential group
                        for dr in range(height):
                            for dc in range(width):
                                if not is_valid_pos(r+dr, c+dc):
                                    valid_group = False
                                    break
                                cells.append(get_decimal((r+dr) % rows, (c+dc) % cols))
                            if not valid_group:
                                break
                        
                        if valid_group:
                            all_groups.append((sorted(cells), size))
            
            size *= 2
        
        # Remove duplicates and filter covered groups
        essential_groups = []
        seen_groups = set()
        
        # Sort by group size (largest first)
        all_groups.sort(key=lambda x: -x[1])
        
        # Track which minterms are covered
        covered_minterms = set()
        
        for group, size in all_groups:
            # Convert to tuple for hashing
            group_tuple = tuple(group)
            
            # Skip if we've seen this group before
            if group_tuple in seen_groups:
                continue
            
            seen_groups.add(group_tuple)
            
            # Check if this group covers any uncovered minterms
            uncovered = [m for m in group if m in minterms and m not in covered_minterms]
            
            if uncovered:
                essential_groups.append((group, size))
                covered_minterms.update(uncovered)
        
        return essential_groups
    
    def group_to_expression(self, group, size, num_vars, var_names):
        """Convert a group of minterms to a Boolean expression"""
        # Convert all minterms to binary
        binary_terms = [format(m, f'0{num_vars}b') for m in group]
        
        # Find which bits stay the same across all terms
        pattern = list(binary_terms[0])
        for i in range(len(pattern)):
            if any(term[i] != pattern[i] for term in binary_terms[1:]):
                pattern[i] = 'x'  # Mark varying bit with 'x'
        
        # Create the expression
        expr = []
        for i, bit in enumerate(pattern):
            var = var_names[i]
            if bit == '1':
                expr.append(var)
            elif bit == '0':
                expr.append(f"{var}'")
            # Skip 'x' positions - these variables don't matter
        
        return ''.join(expr) if expr else "1"  # Empty means all vars are 'x'
    
    def get_user_input(self):
        """Get variables and minterms from user input with improved handling"""
        print("\n===== Enhanced K-Map Solver =====\n")
        
        # Get number of variables
        while True:
            try:
                num_vars = int(input(f"How many variables? (2-{self.max_vars}): "))
                if num_vars < 2 or num_vars > self.max_vars:
                    print(f"Only 2 to {self.max_vars} variables are supported. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Get variable names or use defaults
        default_var_names = ['A', 'B', 'C', 'D', 'E', 'F'][:num_vars]
        default_names_str = ", ".join(default_var_names)
        
        custom_vars = input(f"\nUse custom variable names? (default: {default_names_str}) [y/N]: ").strip().lower()
        
        if custom_vars == 'y':
            print(f"Enter {num_vars} variable names separated by spaces: ")
            while True:
                var_input = input().strip().split()
                if len(var_input) != num_vars:
                    print(f"Please enter exactly {num_vars} variable names.")
                    continue
                variables = var_input
                break
        else:
            variables = default_var_names
        
        # Show total number of possible states
        max_value = 2 ** num_vars - 1
        print(f"\nFor {num_vars} variables, there are {max_value + 1} possible states (0-{max_value}).")
        
        # Get minterms
        print("\nEnter minterms separated by spaces (e.g., 0 1 4 5): ")
        while True:
            try:
                minterm_input = input().strip()
                if not minterm_input:
                    minterms = []
                    break
                
                minterms = [int(m) for m in minterm_input.split()]
                
                # Validate minterms are within range
                if any(m < 0 or m > max_value for m in minterms):
                    print(f"Minterms must be between 0 and {max_value}. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter valid minterm numbers separated by spaces.")
        
        # Get don't cares (optional)
        dont_cares_yn = input("\nDo you have don't care terms? [y/N]: ").strip().lower()
        
        if dont_cares_yn == 'y':
            print("Enter don't care terms separated by spaces: ")
            while True:
                try:
                    dont_care_input = input().strip()
                    if not dont_care_input:
                        dont_cares = []
                        break
                    
                    dont_cares = [int(d) for d in dont_care_input.split()]
                    
                    # Validate don't cares are within range and not in minterms
                    if any(d < 0 or d > max_value for d in dont_cares):
                        print(f"Don't care terms must be between 0 and {max_value}. Please try again.")
                        continue
                    
                    if any(d in minterms for d in dont_cares):
                        print("Don't care terms cannot be in the minterm list. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Please enter valid don't care term numbers separated by spaces.")
        else:
            dont_cares = []
        
        return num_vars, variables, minterms, dont_cares

    def run(self):
        """Run the K-map solver with all steps"""
        try:
            while True:
                # Get user inputs
                num_vars, variables, minterms, dont_cares = self.get_user_input()
                
                # Create K-map
                kmap, var_names, row_gray, col_gray = self.create_kmap(num_vars, minterms, dont_cares)
                
                # Find prime implicants
                groups = self.find_implicants(kmap, row_gray, col_gray, minterms, dont_cares)
                
                # Display results in text form
                print("\n----- Prime Implicants -----")
                expressions = []
                
                for group, size in groups:
                    expr = self.group_to_expression(group, size, num_vars, var_names)
                    expressions.append(expr)
                    
                    # Format the group for display
                    group_str = ", ".join(str(m) for m in sorted(group))
                    print(f"{expr}: {group_str}")
                
                # Display minimal expression
                print("\n----- Minimal Sum of Products -----")
                if not expressions:
                    print("0")  # All minterms are 0
                elif "1" in expressions:
                    print("1")  # Expression is always true
                else:
                    minimal_sop = " + ".join(expressions)
                    print(minimal_sop)
                
                # Plot the K-map with the groups highlighted
                self.plot_kmap(kmap, var_names, row_gray, col_gray, groups)
                
                # Ask if user wants to try another K-map
                response = input("\nWould you like to create another K-map? (y/n): ").strip().lower()
                if response != 'y':
                    break
            
            print("\nThank you for using the Enhanced K-Map Solver!")
            
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            import traceback
            traceback.print_exc()


# Run the solver if executed directly
if __name__ == "__main__":
    solver = KMapSolver()
    solver.run()