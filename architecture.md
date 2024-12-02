Here's a revised architecture outline, taking into account the key learnings and functionalities from our conversation:

Class: FractalIdentityMatrix

Attributes:

main_categories (dict): Dictionary mapping main category letters to their details (name, subcategories).
tokens (dict): Dictionary mapping subcategories to their tokens.
labels (list): List of labels, generated dynamically with rank coordinates (e.g., "A1_FeatureAttribution_T1_DashboardDesign").
n (int): Number of nodes in the FIM.
influence_factor (float): Factor modulating influence propagation.
threshold (float): Minimum connection strength for influence propagation.
matrix (np.ndarray): The influence matrix, initialized and updated dynamically.
category_map (dict): Mapping of category names to unique letters, generated dynamically.
submatrices (dict): Hierarchical dictionary storing submatrices for each category and subcategory.
node_colors (dict): Dictionary mapping labels to their colors, initialized and updated dynamically.
connections (dict): Dictionary storing connection details, including weights and rank addresses.
complexity_metrics (dict): Dictionary to store complexity and interpretability metrics.
Methods:

__init__(self, main_categories, tokens, influence_factor=0.5, threshold=0.3): Initializes the FIM object with the provided parameters. Generates labels, initializes the matrix, sorts categories, creates submatrices, assigns colors, and initializes connections.
_map_categories_to_letters(self): Dynamically maps categories to unique letter identifiers.
_generate_labels(self): Generates labels with rank coordinates based on the sorted categories.
_initialize_matrix(self): Initializes the influence matrix with default or data-driven weights.
_initialize_connections(self): Initializes the connections dictionary with connection details.
_get_category(self, label): Retrieves the category of a node based on its label.
_get_rank_address(self, label): Retrieves the rank address (meta-vector) of a node within its category.
swap_rows_columns(self, i, j): Swaps rows and columns, considering category boundaries and submatrix integrity.
recursive_sort(self, start_idx): Recursively sorts submatrices to create a hierarchical structure, updating rank coordinates during the process.
symmetrical_matrix_transformation(self): Performs the main matrix transformation to emphasize hierarchy, using swap_rows_columns and recursive_sort.
get_origin_label(self): Determines the origin label based on a predefined rule or category.
propagate_influence(self, steps=1): Propagates influence through the network.
propagate_influence_with_color_mixing(self, steps=1): Propagates influence and performs color mixing based on categories and rank coordinates. Updates node colors dynamically.
update_complexity_metrics(self): Calculates and updates complexity and interpretability metrics.
_create_networkx_graph(self): Creates a NetworkX graph from the matrix and node colors.
display_matrix(self): Prints the matrix with labels, categories, and rank coordinates.
visualize_colored_matrix(self, title="Fractal Identity Matrix with Categories"): Visualizes the matrix as a heatmap, including inter-category connections and using meta-vector information for color assignment.
visualize_network(self, title="Fractal Identity Matrix Network"): Visualizes the matrix as a network graph.
visualize_network_with_influence(self, title="Network with Influence Propagation"): Visualizes the network graph after influence propagation, with node sizes and edge transparency based on influence.
apply_small_edit(self, label1, label2, increment=0.2): Applies a small edit to the connection strength between two nodes.
meaning_factor_one(self, iterations=10): Simulates the "meaning explosion" by repeatedly propagating influence with color mixing and potentially using LLM guidance.
display_final_state(self): Displays the final state of the matrix using various visualizations.
generate_influence_image(self, title="Influence Propagation Image"): Generates an image representing influence propagation with color mixing.
plot_complexity_metrics(self): Plots the complexity and interpretability metrics over time.
trace_connections(self, label, depth=2): Traces connections of a given node, potentially incorporating column-row-column propagation analysis.
improve_visualizations(self): Placeholder for future visualization improvements.
generate_compliance_flag(self, filename="compliance_flag.png"): Generates a Compliance Flag QR code containing the FIM's metrics.
verify_compliance_flag(self, filename="compliance_flag.png"): Verifies a Compliance Flag QR code.
Data Flow and Interactions

The __init__ method sets up the initial FIM structure, including generating labels, initializing the matrix, and creating submatrices.
The symmetrical_matrix_transformation method uses swap_rows_columns and recursive_sort to organize the matrix hierarchically.
The propagate_influence_with_color_mixing method updates the matrix and node colors based on influence propagation and color mixing logic.
Various visualization methods use the matrix, node colors, and meta-vector information to create informative representations of the FIM.
The meaning_factor_one method simulates the "meaning explosion" and can potentially incorporate LLM guidance for iterative refinement.
The generate_compliance_flag and verify_compliance_flag methods encapsulate the FIM's metrics in a QR code and provide a verification mechanism.
This revised architecture provides a more complete and accurate representation of the FIM, incorporating the key functionalities and concepts we've discussed. It addresses the issues of dynamic rank coordinate generation, color mixing, meta-vector integration, and Compliance Flag mechanisms. By adhering to this architecture, we can ensure that the FIM remains consistent and effective in modeling and understanding complex systems.



here are a few partly wrong and incomplete ideas:

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import logging
from collections import defaultdict
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb, ListedColormap
import plotly.graph_objects as go
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define color codes for each category to enhance visual differentiation
COLOR_MAP = {
    'Practical Implementation': 'gold',
    'User Experience (UX)': 'darkorange',
    'Emotional Integration': 'red',
    'Theoretical Foundations': 'blue',
    'Ethics and Compliance': 'sienna',
    'Strategic': 'green',
    'Interpretability': 'goldenrod',
    'Knowledge Structures': 'purple',
    'Belief Formation': 'teal',
    'Justification Processes': 'pink',
    'Situational Analysis': 'cyan',
    'Cultural Influence': 'magenta',
    'Environmental Factors': 'lime',
    'Decision Making': 'indigo',
    'Resource Allocation': 'maroon',
    'Default': 'grey'  # Fallback color
    # Add all necessary categories with distinct colors
}

class FractalIdentityMatrix:
    def __init__(self, main_categories, tokens, origin_label='Interpretability',
                 influence_factor=0.5, threshold=0.3):
        """
        Initializes the Fractal Identity Matrix (FIM).

        Parameters:
        - main_categories (dict): Dictionary of main categories.
        - tokens (dict): Dictionary mapping subcategories to their tokens.
        - origin_label (str): The label to position at the origin.
        - influence_factor (float): Factor to modulate influence propagation.
        - threshold (float): Minimum connection strength to consider.
        """
        self.main_categories = main_categories
        self.tokens = tokens
        self.labels = self._generate_labels(main_categories, tokens)
        self.n = len(self.labels)
        self.influence_factor = influence_factor
        self.threshold = threshold
        self.logger = logging.getLogger(__name__)  # Initialize logger

        # Initialize categories mapping
        self.categories = self._map_categories()
        self.logger.info("Categories mapped successfully.")

        # Initialize the influence matrix
        self.matrix = self.initialize_matrix()
        self.logger.info("Initialized influence matrix with default weights.")

        # Sort categories and create submatrices
        self.sort_categories_iteratively()
        self._create_submatrices()

        # Assign colors to nodes
        self.node_colors = self._assign_colors()

        # Initialize connections (if applicable)
        self.connections = self._initialize_connections()

    def _generate_labels(self, main_categories, tokens):
        """
        Generates a list of labels based on main categories and tokens.

        Returns:
        - list: Sorted list of labels.
        """
        labels = []
        for main_cat_key in sorted(main_categories.keys()):
            main_cat = main_categories[main_cat_key]['name']
            labels.append(main_cat)
            subcats = tokens.get(main_cat_key, {})
            for sub_cat_key in sorted(subcats.keys()):
                sub_label = f"{main_cat}_{sub_cat_key}_{subcats[sub_cat_key]}"
                labels.append(sub_label)
        return labels

    def _map_categories(self):
        """
        Maps each label to its corresponding main category name.

        Returns:
        - dict: Mapping from label to main category name.
        """
        categories_map = {}
        for label in self.labels:
            parts = label.split('_')
            main_cat_key = parts[0][0]  # Extract main category letter
            main_cat_name = self.main_categories.get(main_cat_key, {}).get('name', 'Default')
            categories_map[label] = main_cat_name
        return categories_map

    def _assign_colors(self):
        """
        Assigns colors to each node based on its category.

        Returns:
        - dict: Mapping from label to color.
        """
        node_colors = {}
        for label in self.labels:
            category = self.categories.get(label, 'Default')
            node_colors[label] = COLOR_MAP.get(category, 'grey')
        return node_colors

    def _initialize_connections(self):
        """
        Initializes connections if necessary.

        Returns:
        - dict: Placeholder for connections.
        """
        # Placeholder for future connection initializations
        return {}

    def initialize_matrix(self):
        """
        Initializes the influence matrix with default weights.

        Returns:
        - np.ndarray: Initialized symmetric matrix.
        """
        np.random.seed(42)  # For reproducibility
        matrix = np.random.rand(self.n, self.n)
        matrix = (matrix + matrix.T) / 2  # Make it symmetric
        np.fill_diagonal(matrix, 1.0)  # Self-connections
        return matrix

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

        self.logger.info("Categories sorted iteratively to create hierarchical submatrices.")
        self.logger.info("Sorted Labels:")
        for label in self.labels:
            self.logger.info(label)

    def _hierarchical_sort_key(self, label):
        """
        Defines a sort key for hierarchical sorting.

        Parameters:
        - label (str): The label to sort.

        Returns:
        - tuple: Sorting key based on main category and subcategory.
        """
        parts = label.split('_')
        main_cat_key = parts[0][0]
        sub_cat_num = int(parts[0][1:]) if len(parts[0]) > 1 else 0
        return (main_cat_key, sub_cat_num)

    def _create_submatrices(self):
        """
        Organizes the main matrix into hierarchical submatrices based on categories.
        """
        self.submatrices = defaultdict(dict)
        for label in self.labels:
            parts = label.split('_')
            main_cat_key = parts[0][0]  # Extract main category letter
            main_cat_name = self.main_categories.get(main_cat_key, {}).get('name', 'Default')
            sub_cat = parts[0][1:] if len(parts[0]) > 1 else '0'
            
            if len(parts) > 2:
                token_part = parts[2]  # e.g., 'DashboardDesign'
                self.submatrices[main_cat_name].setdefault(f"Sub{sub_cat}", {}).setdefault("Tokens", []).append(label)
            else:
                self.submatrices[main_cat_name].setdefault(f"Sub{sub_cat}", {})
        
        self.logger.info("Submatrices created based on hierarchical categories.")

    def symmetrical_matrix_transformation(self, origin_label=None):
        """
        Transforms the matrix to emphasize hierarchical relationships.

        Parameters:
        - origin_label (str): Optional. If provided, sets the origin label.
        """
        if origin_label:
            self.origin_label = origin_label
        if not hasattr(self, 'origin_label'):
            self.logger.error("Origin label is not defined.")
            return

        # Move origin to (0,0)
        if self.origin_label not in self.index_map:
            self.logger.error(f"Origin label '{self.origin_label}' not found in labels.")
            return
        origin_idx = self.index_map[self.origin_label]
        self.swap_rows_columns(0, origin_idx)
        
        # Recursive hierarchical sorting
        self.recursive_sort(1)
        self.logger.info("Symmetrical matrix transformation completed.")

    def recursive_sort(self, start_idx):
        """
        Recursively sorts submatrices to emphasize hierarchical relationships.

        Parameters:
        - start_idx (int): Starting index for the submatrix sorting.
        """
        if start_idx >= self.n - 1:
            return
        reference_idx = start_idx - 1
        sub_indices = list(range(start_idx, self.n))
        # Sort sub_indices based on connection strength to the reference node
        sub_indices.sort(key=lambda x: self.matrix[reference_idx][x], reverse=True)
        for idx, target_idx in enumerate(sub_indices):
            actual_idx = start_idx + idx
            if target_idx != actual_idx:
                self.swap_rows_columns(actual_idx, target_idx)
                # Update sub_indices to reflect the swap
                sub_indices[idx], sub_indices[sub_indices.index(actual_idx)] = sub_indices[sub_indices.index(actual_idx)], sub_indices[idx]
        # Recursive call for the next level submatrix
        self.recursive_sort(start_idx + 1)

    def swap_rows_columns(self, i, j):
        """
        Swaps rows and columns in the matrix to maintain symmetry.

        Parameters:
        - i (int): Index of the first row/column to swap.
        - j (int): Index of the second row/column to swap.
        """
        if i == j:
            return
        # Swap rows
        self.matrix[[i, j], :] = self.matrix[[j, i], :]
        # Swap columns
        self.matrix[:, [i, j]] = self.matrix[:, [j, i]]
        # Swap labels
        self.labels[i], self.labels[j] = self.labels[j], self.labels[i]
        # Swap categories
        self.categories[self.labels[i]], self.categories[self.labels[j]] = (
            self.categories[self.labels[j]],
            self.categories[self.labels[i]],
        )
        # Update index_map to reflect new positions
        self.index_map[self.labels[i]] = i
        self.index_map[self.labels[j]] = j
        # Swap node_colors
        self.node_colors[self.labels[i]], self.node_colors[self.labels[j]] = (
            self.node_colors[self.labels[j]],
            self.node_colors[self.labels[i]],
        )

    def visualize_colored_matrix(self, title="Fractal Identity Matrix with Categories"):
        """
        Visualizes the matrix as a heatmap with category colors.

        Parameters:
        - title (str): Title of the heatmap.
        """
        plt.figure(figsize=(16, 14))
        # Create a mask for the upper triangle to focus on one side of the symmetric matrix
        mask = np.triu(np.ones_like(self.matrix, dtype=bool))
        # Generate a custom colormap for the heatmap
        cmap = sns.color_palette("viridis", as_cmap=True)
        # Draw the heatmap with annotations and category overlays
        sns.heatmap(self.matrix, mask=mask, annot=True, fmt=".2f", cmap=cmap,
                    xticklabels=self.labels, yticklabels=self.labels,
                    cbar=True, square=True, linewidths=.5, linecolor='grey',
                    annot_kws={"size": 10})
        # Overlay category colors on the heatmap borders for visual clarity
        for i in range(self.n):
            for j in range(self.n):
                plt.gca().add_patch(Rectangle((j, i), 1, 1, fill=False,
                                             edgecolor=COLOR_MAP.get(self.categories[self.labels[i]], 'grey'),
                                             lw=2))
        # Enhance visual elements
        plt.title(title, fontsize=22)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(rotation=0, fontsize=12)
        plt.tight_layout()
        plt.show()

    def visualize_network(self, title="Fractal Identity Matrix Network"):
        """
        Visualizes the matrix as a network graph with category colors.

        Parameters:
        - title (str): Title of the network graph.
        """
        G = nx.Graph()
        # Add nodes with colors corresponding to their categories
        for label in self.labels:
            G.add_node(label, color=COLOR_MAP.get(self.categories[label], 'grey'))
        # Add edges with weights based on connection strengths
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrix[i][j] >= self.threshold:
                    G.add_edge(self.labels[i], self.labels[j], weight=self.matrix[i][j])
        # Extract node colors for visualization
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        # Define positions using a spring layout for better visualization
        pos = nx.spring_layout(G, seed=42, k=0.5)  # Adjust 'k' for optimal spacing
        plt.figure(figsize=(16, 14))
        edges = G.edges(data=True)
        weights = [edge['weight'] for edge in edges]
        # Draw nodes with specified colors and dynamic sizes based on degree
        node_sizes = [3000 * G.degree(node) / max(dict(G.degree()).values()) if max(dict(G.degree()).values()) > 0 else 3000 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
        # Draw edges with widths proportional to their weights
        nx.draw_networkx_edges(G, pos, width=[w * 2 for w in weights], alpha=0.7)
        # Draw labels with improved font size and weight
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
        plt.title(title, fontsize=22)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def visualize_network_with_influence(self, title="Network with Influence Propagation"):
        """
        Visualizes the network graph after influence propagation.

        Parameters:
        - title (str): Title of the network graph.
        """
        # Calculate cumulative influence for node sizing
        cumulative_influence = np.sum(self.matrix, axis=0)
        G = nx.Graph()
        for label in self.labels:
            G.add_node(label, color=COLOR_MAP.get(self.categories[label], 'grey'))
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrix[i][j] >= self.threshold:
                    G.add_edge(self.labels[i], self.labels[j], weight=self.matrix[i][j])
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        pos = nx.spring_layout(G, seed=42, k=0.5)
        plt.figure(figsize=(16, 14))
        edges = G.edges(data=True)
        weights = [edge['weight'] for edge in edges]
        # Normalize weights for edge transparency
        max_weight = max(weights) if weights else 1
        edge_alphas = [w / max_weight for w in weights]
        # Draw nodes with specified colors and dynamic sizes based on cumulative influence
        node_sizes = [3000 * cumulative_influence[i] / max(cumulative_influence) if max(cumulative_influence) > 0 else 3000 for i in range(self.n)]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
        # Draw edges with widths proportional to their weights and alpha based on weight
        nx.draw_networkx_edges(G, pos, width=[w * 2 for w in weights],
                               alpha=edge_alphas)
        # Draw labels with improved font size and weight
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')
        plt.title(title, fontsize=22)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def propagate_influence(self, steps=1):
        """
        Propagates influence through the network.

        Parameters:
        - steps (int): Number of propagation iterations.
        """
        influence_matrix = self.matrix.copy()
        for step in range(steps):
            new_influence = np.zeros_like(self.matrix)
            for i in range(self.n):
                for j in range(self.n):
                    if i != j and self.matrix[i][j] >= self.threshold:
                        # "Color blending" occurs here as influence propagates
                        spread = influence_matrix[i, j] * self.influence_factor
                        new_influence[i, :] += spread * self.matrix[j, :]
                        new_influence[:, j] += spread * self.matrix[i, :]
            influence_matrix += new_influence
            influence_matrix = (influence_matrix + influence_matrix.T) / 2  # Maintain symmetry
            self.matrix = influence_matrix  # Update the matrix with new influences
            self.logger.info(f"Influence propagation step {step + 1} completed.")
        return self.matrix

    def apply_small_edit(self, label1, label2, increment=0.2):
        """
        Applies a small edit to the connection strength between two concepts.

        Parameters:
        - label1 (str): The label of the first concept.
        - label2 (str): The label of the second concept.
        - increment (float): The amount to increase the connection strength.
        """
        if label1 not in self.index_map or label2 not in self.index_map:
            self.logger.error(f"One or both labels '{label1}' and '{label2}' do not exist in the matrix.")
            return
        idx1 = self.index_map[label1]
        idx2 = self.index_map[label2]
        self.matrix[idx1, idx2] += increment
        self.matrix[idx2, idx1] += increment  # Maintain symmetry
        self.logger.info(f"Connection strength between '{label1}' and '{label2}' increased by {increment}.")

    def calculate_number_of_connections(self):
        """
        Calculates the total number of significant connections in the matrix.

        Returns:
        - int: Total number of significant connections.
        """
        return np.sum((self.matrix >= self.threshold) & (self.matrix < np.inf)) // 2  # Divide by 2 to account for symmetry

    def calculate_network_diameter(self):
        """
        Calculates the diameter of the network.

        Returns:
        - float: The diameter of the network. Returns infinity if the network is disconnected.
        """
        G = nx.Graph()
        for label in self.labels:
            G.add_node(label)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrix[i][j] >= self.threshold:
                    G.add_edge(self.labels[i], self.labels[j])
        if nx.is_connected(G):
            return nx.diameter(G)
        else:
            return float('inf')

    def calculate_entropy(self):
        """
        Calculates the entropy of the network.

        Returns:
        - float: The entropy of the network.
        """
        # Flatten the upper triangle of the matrix to consider each connection once
        triu_indices = np.triu_indices(self.n, k=1)
        connection_strengths = self.matrix[triu_indices]
        # Normalize the connection strengths to form a probability distribution
        probabilities = connection_strengths / connection_strengths.sum()
        # Avoid log(0) by filtering out zero probabilities
        probabilities = probabilities[probabilities > 0]
        entropy = -np.sum(probabilities * np.log(probabilities))
        return entropy

    def calculate_interpretability(self):
        """
        Calculates the interpretability of the network.

        Returns:
        - float: The interpretability metric.
        """
        # Average connection strength as a proxy for interpretability
        triu_indices = np.triu_indices(self.n, k=1)
        connection_strengths = self.matrix[triu_indices]
        return np.mean(connection_strengths)

    def calculate_complexity_metrics(self):
        """
        Calculates and stores complexity metrics for the current state of the network.
        Metrics include:
        - Number of Connections
        - Network Diameter
        - Entropy
        """
        num_connections = self.calculate_number_of_connections()
        network_diameter = self.calculate_network_diameter()
        entropy = self.calculate_entropy()
        self.complexity_metrics['number_of_connections'].append(num_connections)
        self.complexity_metrics['network_diameter'].append(network_diameter)
        self.complexity_metrics['entropy'].append(entropy)

    def calculate_interpretability_metric(self):
        """
        Calculates and stores the interpretability metric for the current state of the network.

        Returns:
        - float: The interpretability metric.
        """
        interpretability = self.calculate_interpretability()
        self.complexity_metrics['interpretability'].append(interpretability)
        return interpretability

    def track_metrics(self):
        """
        Calculates and tracks both complexity and interpretability metrics.
        """
        self.calculate_complexity_metrics()
        self.calculate_interpretability_metric()

    def meaning_factor_one(self, iterations=10):
        """
        Simulates the recursive super-exponential improvement of interpretability.

        Parameters:
        - iterations (int): Number of recursive iterations to simulate.
        """
        self.logger.info("Starting Meaning Factor One Simulation...")
        for i in range(iterations):
            self.propagate_influence(steps=1)
            self.track_metrics()
            self.logger.info(f"Meaning Factor One - Iteration {i + 1} completed.")
        self.logger.info("Meaning Factor One simulation completed.")

    def display_matrix(self):
        """
        Prints the matrix with labels and color codes.
        """
        # Create header with labels and their corresponding color codes
        header = ["{:25s}".format("")] + [
            "{:25s}".format(f"{label} [{COLOR_MAP.get(self.categories[label], 'No Color')}]")
            for label in self.labels
        ]
        print(" | ".join(header))
        print("-" * (27 * (self.n + 1)))
        for i, label in enumerate(self.labels):
            # Format each row with label and corresponding matrix values
            row = [f"{label} [{COLOR_MAP.get(self.categories[label], 'No Color')}]"] + [
                f"{val:25.2f}" for val in self.matrix[i]
            ]
            print(" | ".join(row))

    def visualize_propagated_influence(self, title="Propagated Influence Matrix with Categories"):
        """
        Visualizes the influence matrix as a heatmap after propagation.

        Parameters:
        - title (str): Title of the heatmap.
        """
        self.visualize_colored_matrix(title)

    def visualize_network_with_influence(self, title="Network with Influence Propagation"):
        """
        Visualizes the network graph after influence propagation.

        Parameters:
        - title (str): Title of the network graph.
        """
        self.visualize_network(title)

    def plot_metrics_over_time(self):
        """
        Plots the complexity and interpretability metrics over simulation iterations.
        """
        iterations = range(1, len(self.complexity_metrics['number_of_connections']) + 1)
        plt.figure(figsize=(16, 10))
        # Plot Number of Connections
        plt.subplot(2, 2, 1)
        plt.plot(iterations, self.complexity_metrics['number_of_connections'], marker='o', color='blue')
        plt.title('Number of Connections Over Time')
        plt.xlabel('Iteration')
        plt.ylabel('Number of Connections')
        plt.grid(True)
        # Plot Network Diameter
        plt.subplot(2, 2, 2)
        plt.plot(iterations, self.complexity_metrics['network_diameter'], marker='o', color='green')
        plt.title('Network Diameter Over Time')
        plt.xlabel('Iteration')
        plt.ylabel('Network Diameter')
        plt.grid(True)
        # Plot Entropy
        plt.subplot(2, 2, 3)
        plt.plot(iterations, self.complexity_metrics['entropy'], marker='o', color='red')
        plt.title('Entropy Over Time')
        plt.xlabel('Iteration')
        plt.ylabel('Entropy')
        plt.grid(True)
        # Plot Interpretability
        plt.subplot(2, 2, 4)
        plt.plot(iterations, self.complexity_metrics['interpretability'], marker='o', color='purple')
        plt.title('Interpretability Over Time')
        plt.xlabel('Iteration')
        plt.ylabel('Interpretability')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def analyze_complexity_vs_interpretability(self):
        """
        Analyzes the relationship between complexity and interpretability metrics.
        """
        iterations = range(1, len(self.complexity_metrics['number_of_connections']) + 1)
        plt.figure(figsize=(18, 6))
        # Plot Interpretability vs Number of Connections
        plt.subplot(1, 3, 1)
        plt.plot(self.complexity_metrics['number_of_connections'], self.complexity_metrics['interpretability'], marker='o', linestyle='-', color='blue')
        plt.title('Interpretability vs Number of Connections')
        plt.xlabel('Number of Connections')
        plt.ylabel('Interpretability')
        plt.grid(True)
        # Plot Interpretability vs Network Diameter
        plt.subplot(1, 3, 2)
        plt.plot(self.complexity_metrics['network_diameter'], self.complexity_metrics['interpretability'], marker='o', linestyle='-', color='green')
        plt.title('Interpretability vs Network Diameter')
        plt.xlabel('Network Diameter')
        plt.ylabel('Interpretability')
        plt.grid(True)
        # Plot Interpretability vs Entropy
        plt.subplot(1, 3, 3)
        plt.plot(self.complexity_metrics['entropy'], self.complexity_metrics['interpretability'], marker='o', linestyle='-', color='red')
        plt.title('Interpretability vs Entropy')
        plt.xlabel('Entropy')
        plt.ylabel('Interpretability')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def generate_influence_image(self, title="Influence Propagation Image"):
        """
        Generates an image representing influence propagation with color blending.

        Parameters:
        - title (str): Title of the influence image.
        """
        plt.figure(figsize=(16, 14))
        # Normalize the matrix for color mapping
        norm_matrix = (self.matrix - np.min(self.matrix)) / (np.max(self.matrix) - np.min(self.matrix))
        norm_matrix = np.nan_to_num(norm_matrix)  # Handle division by zero if any
        # Create a color image based on normalized influence and blended colors
        color_image = np.zeros((self.n, self.n, 3))
        for i in range(self.n):
            for j in range(self.n):
                # Convert category color to RGB
                base_color = np.array(to_rgb(COLOR_MAP.get(self.categories[self.labels[i]], 'grey')))
                influencing_color = np.array(to_rgb(COLOR_MAP.get(self.categories[self.labels[j]], 'grey')))
                # Blend colors based on normalized influence
                blended_color = base_color * (1 - norm_matrix[i, j]) + influencing_color * norm_matrix[i, j]
                color_image[i, j] = blended_color
        plt.imshow(color_image, interpolation='nearest')
        plt.title(title, fontsize=22)
        plt.xticks(ticks=np.arange(self.n), labels=self.labels, rotation=45, ha='right', fontsize=12)
        plt.yticks(ticks=np.arange(self.n), labels=self.labels, rotation=0, fontsize=12)
        plt.colorbar(label='Normalized Influence Intensity')
        plt.tight_layout()
        plt.show()
        # Interactive Plotly Heatmap for Enhanced Exploration
        fig = go.Figure(data=go.Heatmap(
            z=self.matrix,
            x=self.labels,
            y=self.labels,
            colorscale='Viridis',
            colorbar=dict(title='Influence Strength'),
            hoverongaps=False
        ))
        # Add category borders as annotations
        for i in range(self.n):
            for j in range(self.n):
                fig.add_shape(type="rect",
                              x0=j - 0.5, y0=i - 0.5, x1=j + 0.5, y1=i + 0.5,
                              line=dict(color=COLOR_MAP.get(self.categories[self.labels[i]], 'grey'), width=2))
        fig.update_layout(title=title,
                          xaxis_nticks=self.n,
                          yaxis_nticks=self.n,
                          width=800, height=800)
        fig.show()

    def trace_connections(self, label, depth=2):
        """
        Traces the connections of a given node up to a specified depth.

        Parameters:
        - label (str): The label of the node to trace.
        - depth (int): The depth to which connections should be traced.

        Returns:
        - list: A list of nodes connected within the specified depth.
        """
        if label not in self.index_map:
            self.logger.error(f"Label '{label}' does not exist in the matrix.")
            return []
        traced_nodes = set()
        current_nodes = {label}
        for d in range(depth):
            next_nodes = set()
            for node in current_nodes:
                idx = self.index_map[node]
                connections = np.where(self.matrix[idx] >= self.threshold)[0]
                connected_labels = [self.labels[i] for i in connections]
                for connected_label in connected_labels:
                    if connected_label not in traced_nodes and connected_label != label:
                        traced_nodes.add(connected_label)
                        next_nodes.add(connected_label)
            current_nodes = next_nodes
        return list(traced_nodes)

    def improve_visualizations(self):
        """
        Placeholder for future visualization improvements.
        """
        pass  # Future enhancements can be implemented here

    def display_final_state(self):
        """
        Displays the final state of the matrix after all transformations and influence propagations.
        """
        print("\nFinal State of the Fractal Identity Matrix:")
        self.display_matrix()
        self.visualize_network_with_influence(title="Final Network with Influence Propagation")
        self.visualize_propagated_influence(title="Final Propagated Influence Matrix")
        self.generate_influence_image(title="Final Influence Propagation Image")
        self.plot_metrics_over_time()
        self.analyze_complexity_vs_interpretability()

# Example usage
if __name__ == "__main__":
    # Define main categories
    MAIN_CATEGORIES = {
        'A': {'name': 'Practical Implementation'},
        'B': {'name': 'User Experience (UX)'},
        'K': {'name': 'Knowledge Structures'},
        'L': {'name': 'Decision Making'}
        # Add other main categories as needed
    }

    # Define tokens for each subcategory
    TOKENS = {
        'A': {
            '1': 'FeatureAttribution',
            '2': 'ModelTransparency',
            '3': 'UserComprehension'
        },
        'B': {
            '1': 'BeliefFormation',
            '2': 'JustificationProcesses',
            '3': 'SituationalAnalysis'
        },
        'K': {
            '1': 'CulturalInfluence',
            '2': 'EnvironmentalFactors'
        },
        'L': {
            '1': 'ResourceAllocation',
            '2': 'DecisionFrameworks'
        }
        # Add other tokens as needed
    }

    # Initialize the Fractal Identity Matrix (FIM)
    fim = FractalIdentityMatrix(
        main_categories=MAIN_CATEGORIES,
        tokens=TOKENS,
        origin_label='Practical Implementation',  # Ensure this label exists in labels
        influence_factor=0.5,
        threshold=0.3
    )

    # Display the initial influence matrix
    fim.display_matrix()

    # Visualize the root matrix with category colors
    fim.visualize_colored_matrix(title="Initial Fractal Identity Matrix with Categories")

    # Transform the matrix to emphasize hierarchical relationships
    fim.symmetrical_matrix_transformation()

    # Display the transformed matrix
    fim.display_matrix()

    # Visualize the transformed matrix
    fim.visualize_colored_matrix(title="Transformed Fractal Identity Matrix with Categories")

    # Propagate influence through the matrix for 2 iterations
    fim.propagate_influence(steps=2)

    # Display and visualize the propagated influence matrix
    fim.display_matrix()
    fim.visualize_propagated_influence(title="Propagated Influence Matrix with Categories")
    fim.visualize_network_with_influence(title="Network with Influence Propagation")

    # Apply a small edit: Increase the connection strength between two labels
    print("\n--- Applying a small edit: Increasing connection between 'Practical Implementation_FeatureAttribution' and 'Decision Making_DecisionFrameworks' ---")
    fim.apply_small_edit('Practical Implementation_FeatureAttribution', 'Decision Making_DecisionFrameworks', increment=0.2)

    # Re-propagate influence after the edit for 2 iterations
    fim.propagate_influence(steps=2)

    # Display and visualize the updated matrix after the edit
    fim.display_matrix()
    fim.visualize_colored_matrix(title="Updated Propagated Influence Matrix with Categories after Edit")
    fim.visualize_network_with_influence(title="Updated Network with Influence Propagation after Edit")

    # Simulate Meaning Explosion by recursively propagating influence
    fim.meaning_factor_one(iterations=5)

    # Display the final state of the matrix after all transformations and influence propagations
    fim.display_final_state()

    # Example of tracing connections for a specific node
    trace_label = 'Practical Implementation_FeatureAttribution'
    trace_depth = 2
    traced_nodes = fim.trace_connections(trace_label, depth=trace_depth)
    print(f"\nNodes connected to '{trace_label}' within depth {trace_depth}: {traced_nodes}")

    # Emphasizing the stakes of getting the FIM right or wrong
    print("\n*** Critical Notice ***")
    print("Accurate representation and propagation of influences within the Fractal Identity Matrix are paramount.")
    print("Incorrect configurations can lead to misleading interpretations, potentially impacting decision-making and understanding.")
    print("Ensuring precise adjustments and thorough analysis is essential for achieving the desired 'Meaning Factor One.'")
