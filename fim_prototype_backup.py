import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb
from collections import defaultdict
import string
import re
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

# Define color codes for each main category to enhance visual differentiation
COLOR_MAP = {
    'Interpretability': '#000000',          # Black
    'Epistemology': '#0000FF',              # Blue
    'Ethics': '#008000',                     # Green
    'Metaphysics': '#800080',                # Purple
    'Logic': '#FFFF00',                      # Yellow
    'Aesthetics': '#FFA500',                 # Orange
    'Political Philosophy': '#FFD700',       # Gold
    'Philosophy of Mind': '#FF0000',         # Red
    'Semantic': '#008080',                   # Teal
    'Procedural': '#00FFFF',                 # Cyan
    'Contextual': '#FF00FF',                 # Magenta
    'Strategic': '#A52A2A',                  # Brown
    # Add more categories as needed with valid hex codes
}

# Assign a unique letter to each main category
MAIN_CATEGORY_LETTERS = list(string.ascii_uppercase)  # ['A', 'B', 'C', ...]

# Define main categories and their respective subcategories
MAIN_CATEGORIES = {
    'A': {
        'name': 'Interpretability',
        'subcategories': ['Feature Attribution', 'Model Transparency', 'User Comprehension']
    },
    'B': {
        'name': 'Epistemology',
        'subcategories': ['Knowledge Structures', 'Belief Formation', 'Justification Processes']
    },
    'C': {
        'name': 'Ethics',
        'subcategories': ['Utilitarianism', 'Deontological Ethics', 'Virtue Ethics']
    },
    'D': {
        'name': 'Metaphysics',
        'subcategories': ['Existence', 'Causality', 'Time']
    },
    'E': {
        'name': 'Logic',
        'subcategories': ['Deductive Reasoning', 'Inductive Reasoning', 'Abductive Reasoning']
    },
    'F': {
        'name': 'Aesthetics',
        'subcategories': ['Beauty', 'Artistic Expression', 'Sensory Perception']
    },
    'G': {
        'name': 'Political Philosophy',
        'subcategories': ['Justice', 'Authority', 'Freedom']
    },
    'H': {
        'name': 'Philosophy of Mind',
        'subcategories': ['Consciousness', 'Intentionality', 'Mental Representation']
    },
    'I': {
        'name': 'Semantic',
        'subcategories': ['Meaning', 'Reference', 'Truth Conditions']
    },
    'J': {
        'name': 'Procedural',
        'subcategories': ['Algorithm Design', 'Process Optimization', 'Procedure Formalization']
    },
    'K': {
        'name': 'Contextual',
        'subcategories': ['Situational Analysis', 'Cultural Influence', 'Environmental Factors']
    },
    'L': {
        'name': 'Strategic',
        'subcategories': ['Long-term Planning', 'Decision Making', 'Resource Allocation']
    }
    # Add more main categories as needed
}

# Define tokens for each subcategory
TOKENS = {
    'A1_FeatureAttribution': ['DashboardDesign', 'UserFeedback', 'AccessibilityFeatures'],
    'A2_ModelTransparency': ['ModelAuditing', 'ExplainableAI', 'TransparencyReports'],
    'A3_UserComprehension': ['UserGuides', 'InteractiveTutorials', 'ComprehensionTests'],
    'B1_KnowledgeStructures': ['DataModels', 'OntologyDesign', 'KnowledgeGraphs'],
    'B2_BeliefFormation': ['CognitiveBiases', 'BeliefRevision', 'ReasoningProcesses'],
    'B3_JustificationProcesses': ['EvidenceEvaluation', 'ArgumentationTheory', 'ProofMechanisms'],
    # Add tokens for other subcategories similarly
    # ...
}

class FractalIdentityMatrix:
    def __init__(self, categories, influence_factor=0.5, threshold=0.3):
        self.categories = categories
        self.labels = self._generate_full_label_list(categories)
        self.n = len(self.labels)
        self.influence_factor = influence_factor
        self.threshold = threshold
        self.matrix = self.initialize_matrix()
        self.sort_categories_iteratively()
        self._create_submatrices()
        self.node_colors = self._assign_colors()
        self.connections = self._initialize_connections()

    def _generate_labels(self, main_categories, tokens):
        """
        Generates hierarchical labels with rank coordinates.

        Parameters:
        - main_categories (dict): Dictionary mapping main category letters to their details.
        - tokens (dict): Dictionary mapping subcategories to their tokens.

        Returns:
        - list: Hierarchically structured labels.
        """
        categories = []
        for letter, details in main_categories.items():
            main_cat_name = details['name']
            subcategories = details['subcategories']
            for idx, sub_cat in enumerate(subcategories, start=1):
                sub_label = f"{letter}{idx}_{sub_cat.replace(' ', '')}"
                categories.append(sub_label)
                # Add tokens if defined
                if sub_label in tokens:
                    for t_idx, token in enumerate(tokens[sub_label], start=1):
                        token_label = f"{sub_label}_T{t_idx}_{token.replace(' ', '')}"
                        categories.append(token_label)
        return categories

    def _generate_full_label_list(self, categories):
        """
        Generates a complete list of labels.

        Parameters:
        - categories (list): List of hierarchical labels.

        Returns:
        - list: Sorted list of labels.
        """
        return sorted(categories, key=lambda x: self._hierarchical_sort_key(x))

    def _hierarchical_sort_key(self, label):
        """
        Generates a sort key based on hierarchical ranking for sorting.

        Parameters:
        - label (str): The label to generate a sort key for.

        Returns:
        - tuple: A tuple representing the hierarchical sorting order.
        """
        parts = label.split('_')
        main_part = parts[0]  # e.g., 'A1'
        main_letter = main_part[0]
        main_num = int(main_part[1]) if len(main_part) > 1 and main_part[1].isdigit() else 0

        sub_num = 0
        token_num = 0
        for part in parts[1:]:
            if part.startswith('T'):
                token_num = int(re.findall(r'\d+', part)[0]) if re.findall(r'\d+', part) else 0
            else:
                sub_num = int(re.findall(r'\d+', part)[0]) if re.findall(r'\d+', part) else 0

        return (main_letter, main_num, sub_num, token_num)

    def sort_categories_iteratively(self):
        """
        Iteratively sorts categories to create hierarchical submatrices while maintaining symmetry.
        """
        # Sort labels based on hierarchical ranking
        self.labels.sort(key=lambda x: self._hierarchical_sort_key(x))
        self.index_map = {label: idx for idx, label in enumerate(self.labels)}
        
        # Reorder the matrix based on the sorted labels using NumPy's ix_ for symmetry
        sorted_indices = [self.index_map[label] for label in self.labels]
        self.matrix = self.matrix[np.ix_(sorted_indices, sorted_indices)]

        print("Categories sorted iteratively to create hierarchical submatrices.")
        print("Sorted Labels:")
        for label in self.labels:
            print(label)

    def _create_submatrices(self):
        """
        Organizes the main matrix into hierarchical submatrices based on categories.
        """
        self.submatrices = defaultdict(dict)
        for label in self.labels:
            parts = label.split('_')
            main_cat = parts[0][:1]  # Extract main category letter
            sub_cat = parts[0][1:]   # Extract subcategory number
            
            if 'T' in parts[1]:
                token_part = parts[1]  # e.g., 'T1_DashboardDesign'
                self.submatrices[main_cat][f"Sub{sub_cat}"]["Tokens"] = self.submatrices[main_cat][f"Sub{sub_cat}"].get("Tokens", []) + [label]
            else:
                self.submatrices[main_cat][f"Sub{sub_cat}"] = self.submatrices[main_cat].get(f"Sub{sub_cat}", {})
        
        print("Submatrices created based on hierarchical categories.")

    def initialize_matrix(self):
        """
        Initializes the influence matrix with default weights.
        """
        matrix = np.zeros((self.n, self.n))
        
        # Example: Set higher weights for labels within the same main category
        for i, label1 in enumerate(self.labels):
            for j, label2 in enumerate(self.labels):
                if label1 == label2:
                    matrix[i][j] = 1.0  # Maximum influence
                elif label1.split('_')[0][0] == label2.split('_')[0][0]:
                    matrix[i][j] = 0.5  # Moderate influence within the same main category
                else:
                    matrix[i][j] = 0.1  # Minimal influence across different main categories
        print("Initialized influence matrix with default weights.")
        return matrix

    def _assign_colors(self):
        """
        Assigns colors to each node based on their hierarchical level and influence strength.

        Returns:
        - dict: Mapping from label to hex color code.
        """
        label_colors = {}
        for label in self.labels:
            parts = label.split('_')
            main_letter = parts[0][0]  # Extract main category letter
            sub_num = parts[0][1]      # Extract subcategory number
            
            # Retrieve base color from COLOR_MAP using main category name
            main_category_name = MAIN_CATEGORIES[main_letter]['name']
            base_color = COLOR_MAP.get(main_category_name, '#FFFFFF')
            
            if 'T' in parts[1]:
                # Token Level: Lighten the color based on influence strength
                influence_strength = self._get_influence_strength(label)
                blended_color = self._blend_colors(base_color, '#FFFFFF', influence_strength)
                label_colors[label] = blended_color
            elif len(parts) == 1:
                # Main Category Level
                label_colors[label] = base_color
            else:
                # Subcategory Level: Slightly lighten the base color
                blended_color = self._blend_colors(base_color, '#FFFFFF', 0.2)
                label_colors[label] = blended_color
        return label_colors

    def _blend_colors(self, color1, color2, influence_strength):
        """
        Blends two hex colors based on influence strength.

        Parameters:
        - color1 (str): Hex color code of the first color.
        - color2 (str): Hex color code of the second color.
        - influence_strength (float): Weight of influence from color2.

        Returns:
        - str: Blended hex color code.
        """
        try:
            rgb1 = np.array(mcolors.to_rgb(color1))
            rgb2 = np.array(mcolors.to_rgb(color2))
            blended_rgb = (1 - influence_strength) * rgb1 + influence_strength * rgb2
            blended_hex = mcolors.to_hex(blended_rgb)
            return blended_hex
        except ValueError as e:
            print(f"Error blending colors: {e}")
            return '#FFFFFF'  # Default to white on error

    def _get_influence_strength(self, label):
        """
        Retrieves the influence strength for a given label.

        Parameters:
        - label (str): The label to retrieve influence strength for.

        Returns:
        - float: Influence strength between 0 and 1.
        """
        try:
            index = self.labels.index(label)
            # Normalize the influence strength to a value between 0 and 1
            influence_strength = min(self.matrix[index].max(), 1.0)
            # Example: Influence strength could be proportional to the maximum weight in the row
            return influence_strength * 0.5  # Adjust the scaling factor as needed
        except ValueError:
            print(f"Label '{label}' not found in labels list.")
            return 0.0

    def propagate_influence_with_color_mixing(self, iterations=1):
        """
        Propagates influence through the matrix with color mixing based on hierarchical ranks.

        Parameters:
        - iterations (int): Number of propagation iterations.
        """
        for it in range(iterations):
            print(f"Propagation iteration {it + 1}")
            new_matrix = self.matrix.copy()
            for i in range(self.n):
                for j in range(self.n):
                    if self.matrix[i][j] > self.threshold:
                        # Calculate influence based on current weight
                        influence = self.influence_factor * (self.matrix[i][j])
                        new_matrix[i][j] += influence
            # Ensure matrix remains symmetric
            self.matrix = (new_matrix + new_matrix.T) / 2
            print(f"Matrix after iteration {it + 1}:")
            print(self.matrix)
            print(f"Propagation iteration {it + 1} completed.")

            # Update colors based on new influence weights
            self.node_colors = self._assign_colors()
            print(f"Updated node colors after iteration {it + 1}.")

    def display_matrix(self):
        """
        Displays the current state of the influence matrix.
        """
        print("Influence Matrix:")
        print(self.matrix)

    def visualize_colored_matrix(self, title="Fractal Identity Matrix with Hierarchical Categories"):
        """
        Visualizes the matrix using Matplotlib with color coding based on categories.

        Parameters:
        - title (str): Title of the plot.
        """
        # Create a color matrix based on node_colors
        color_matrix = []
        for label1 in self.labels:
            row = []
            for label2 in self.labels:
                # Determine the color based on the connection weight
                weight = self.matrix[self.labels.index(label1)][self.labels.index(label2)]
                color = self.node_colors[label1]  # Simplification: color based on the source node
                row.append(color)
            color_matrix.append(row)
        
        # Convert hex color codes to RGB tuples
        try:
            rgb_matrix = np.array([[mcolors.to_rgb(color) for color in row] for row in color_matrix])
        except ValueError as e:
            print(f"Error converting hex to RGB: {e}")
            return  # Exit the function if conversion fails
        
        # Plot using Matplotlib
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Display the RGB matrix
        cax = ax.imshow(rgb_matrix, aspect='auto')
        
        # Set labels
        ax.set_xticks(range(self.n))
        ax.set_yticks(range(self.n))
        ax.set_xticklabels(self.labels, rotation=90)
        ax.set_yticklabels(self.labels)
        
        # Create a legend for main categories
        handles = []
        unique_main_categories = set([label.split('_')[0][0] for label in self.labels])
        for letter in unique_main_categories:
            category_name = MAIN_CATEGORIES[letter]['name']
            patch = mpatches.Patch(color=COLOR_MAP.get(category_name, '#FFFFFF'), label=category_name)
            handles.append(patch)
        ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.title(title)
        plt.tight_layout()
        plt.show()

    def _initialize_connections(self):
        """
        Initializes connections between categories based on predefined relationships.

        Returns:
        - dict: Nested dictionary representing connections and their weights.
        """
        connections = defaultdict(dict)
        # Example: Define connections manually or load from a predefined structure
        # connections['A1_FeatureAttribution_T1_DashboardDesign']['B1_KnowledgeStructures'] = 0.85
        # Add more connections as needed
        return connections

    def visualize_network_with_influence(self, title="Network with Influence Propagation"):
        """
        Visualizes the FIM as a network graph using NetworkX.

        Parameters:
        - title (str): Title of the graph.
        """
        G = nx.Graph()

        # Add nodes with colors
        for label in self.labels:
            G.add_node(label, color=self.node_colors.get(label, '#FFFFFF'))

        # Add edges based on connections
        for i, label1 in enumerate(self.labels):
            for j, label2 in enumerate(self.labels):
                if self.matrix[i][j] > self.threshold:
                    G.add_edge(label1, label2, weight=self.matrix[i][j])

        # Extract colors
        colors = [G.nodes[node]['color'] for node in G.nodes()]

        # Define edge widths based on weights
        edges = G.edges(data=True)
        weights = [edge_attr['weight'] * 5 for _, _, edge_attr in edges]  # Adjust scaling as needed

        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G, k=0.15, iterations=20)
        nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500, alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
        plt.title(title)
        plt.axis('off')
        plt.show()

# Define a function to verify color assignments
def verify_color_assignments(categories, color_map):
    """
    Verifies that all main categories have assigned colors.

    Parameters:
    - categories (list): List of hierarchical labels.
    - color_map (dict): Mapping of category names to color codes.
    """
    main_categories_present = set([label.split('_')[0][0] for label in categories])
    missing_colors = []
    for letter in main_categories_present:
        main_cat_name = MAIN_CATEGORIES[letter]['name']
        if main_cat_name not in color_map:
            missing_colors.append(main_cat_name)
    if missing_colors:
        print("Missing color assignments for the following main categories:")
        for cat in missing_colors:
            print(cat)
    else:
        print("All main categories have assigned colors.")

# Example usage (from the provided code snippet without line numbers)
if __name__ == "__main__":
    # Initialize the FIM instance with an empty category list
    fim_instance = FractalIdentityMatrix(categories=[])

    # Generate hierarchical labels
    categories = fim_instance._generate_labels(MAIN_CATEGORIES, TOKENS)
    print("Generated Categories:")
    for category in categories:
        print(category)

    # Verify color assignments
    verify_color_assignments(categories, COLOR_MAP)

    # Initialize the Fractal Identity Matrix (FIM) with the defined categories
    fim = FractalIdentityMatrix(categories, influence_factor=0.5, threshold=0.3)

    # Perform matrix transformation to emphasize hierarchical relationships
    fim.symmetrical_matrix_transformation()

    # Display the transformed matrix with labels and color codes
    fim.display_matrix()

    # Visualize the transformed matrix with category colors
    fim.visualize_colored_matrix(title="Transformed Fractal Identity Matrix with Subcategories")

    # Propagate influence through the matrix for 5 iterations
    fim.propagate_influence_with_color_mixing(iterations=5)

    # Display and visualize the propagated influence matrix
    fim.display_matrix()
    fim.visualize_network_with_influence(title="Network with Influence Propagation")
    fim.visualize_colored_matrix(title="Propagated Influence Matrix with Subcategories")
