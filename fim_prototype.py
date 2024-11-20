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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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
    'C1_Utilitarianism': ['UtilityCalculation', 'Cost-BenefitAnalysis'],
    'C2_DeontologicalEthics': ['DutyFulfillment', 'RuleAdherence'],
    'C3_VirtueEthics': ['CharacterDevelopment', 'MoralIntegrity'],
    'D1_Existence': ['Being', 'Reality'],
    'D2_Causality': ['CauseEffect', 'Determinism'],
    'D3_Time': ['TemporalDynamics', 'Chronology'],
    'E1_DeductiveReasoning': ['Syllogism', 'LogicalInference'],
    'E2_InductiveReasoning': ['Generalization', 'PatternRecognition'],
    'E3_AbductiveReasoning': ['BestExplanation', 'HypothesisFormation'],
    'F1_Beauty': ['AestheticAppeal', 'Symmetry'],
    'F2_ArtisticExpression': ['CreativeArts', 'ArtisticStyles'],
    'F3_SensoryPerception': ['SensoryInput', 'PerceptualProcesses'],
    'G1_Justice': ['Fairness', 'LawCompliance'],
    'G2_Authority': ['PowerStructures', 'Governance'],
    'G3_Freedom': ['Autonomy', 'Liberty'],
    'H1_Consciousness': ['Awareness', 'SelfPerception'],
    'H2_Intentionality': ['GoalSetting', 'PurposeDriven'],
    'H3_MentalRepresentation': ['CognitiveMaps', 'InternalModels'],
    'I1_Meaning': ['SemanticUnderstanding', 'Significance'],
    'I2_Reference': ['Denotation', 'Connotation'],
    'I3_TruthConditions': ['TruthValue', 'Accuracy'],
    'J1_AlgorithmDesign': ['AlgorithmEfficiency', 'Optimization'],
    'J2_ProcessOptimization': ['WorkflowImprovement', 'ResourceManagement'],
    'J3_ProcedureFormalization': ['StandardOperatingProcedures', 'ProtocolDevelopment'],
    'K1_SituationalAnalysis': ['ContextAssessment', 'EnvironmentScanning'],
    'K2_CulturalInfluence': ['SocietalNorms', 'CulturalTrends'],
    'K3_EnvironmentalFactors': ['ClimateImpact', 'EcologicalVariables'],
    'L1_Long-termPlanning': ['StrategicVision', 'GoalSetting'],
    'L2_DecisionMaking': ['ChoiceArchitecture', 'DecisionFrameworks'],
    'L3_ResourceAllocation': ['Budgeting', 'ResourceDistribution']
    # Add tokens for other subcategories similarly
    # ...
}

class FractalIdentityMatrix:
    def __init__(self, main_categories, tokens, influence_factor=0.5, threshold=0.3):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.main_categories = main_categories
        self.tokens = tokens
        self.labels = self._generate_labels(main_categories, tokens)
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

    def sort_categories_iteratively(self):
        """
        Sorts categories iteratively to create hierarchical submatrices while maintaining symmetry.
        """
        # Sort labels based on hierarchical ranking: Main Category Letter, Subcategory Number, Token Number
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
        Generates a sort key based on hierarchical ranking for sorting.

        Parameters:
        - label (str): The label to generate a sort key for.

        Returns:
        - tuple: A tuple representing the hierarchical sorting order.
        """
        parts = label.split('_')
        main_part = parts[0]  # e.g., 'A1'
        main_letter = main_part[0]
        main_num = int(main_part[1:]) if len(main_part) > 1 and main_part[1:].isdigit() else 0

        sub_num = 0
        token_num = 0
        for part in parts[1:]:
            if part.startswith('T'):
                token_num = int(re.findall(r'\d+', part)[0]) if re.findall(r'\d+', part) else 0
            else:
                sub_num = int(re.findall(r'\d+', part)[0]) if re.findall(r'\d+', part) else 0

        return (main_letter, main_num, sub_num, token_num)

    def _create_submatrices(self):
        """
        Organizes the main matrix into hierarchical submatrices based on categories.
        """
        self.submatrices = defaultdict(lambda: defaultdict(dict))
        for label in self.labels:
            parts = label.split('_')
            main_cat = parts[0][0]  # Extract main category letter, e.g., 'A' from 'A1_FeatureAttribution'
            sub_cat = parts[0][1:]   # Extract subcategory number, e.g., '1' from 'A1_FeatureAttribution'
            
            if 'T' in parts[1]:
                # It's a token
                self.submatrices[main_cat][f"Sub{sub_cat}"]["Tokens"] = self.submatrices[main_cat][f"Sub{sub_cat}"].get("Tokens", []) + [label]
            else:
                # It's a subcategory; ensure it's initialized
                self.submatrices[main_cat][f"Sub{sub_cat}"] = self.submatrices[main_cat].get(f"Sub{sub_cat}", {})
        
        self.logger.info("Submatrices created based on hierarchical categories.")

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
        self.logger.info("Initialized influence matrix with default weights.")
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
            sub_num = parts[0][1:]      # Extract subcategory number
            
            # Retrieve base color from COLOR_MAP using main category name
            main_category_name = self.main_categories[main_letter]['name']
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

    def _get_influence_strength(self, label):
        """
        Placeholder for obtaining influence strength based on the label.
        Implement your own logic as needed.
        """
        return 0.2  # Example fixed value

    def _blend_colors(self, color1, color2, influence_strength):
        """
        Blends two hex colors based on the influence strength.

        Parameters:
        - color1 (str): Hex color code of the first color.
        - color2 (str): Hex color code of the second color.
        - influence_strength (float): Weight of influence from color2.

        Returns:
        - str: Blended hex color code.
        """
        try:
            rgb1 = np.array(self._hex_to_rgb(color1))
            rgb2 = np.array(self._hex_to_rgb(color2))
            blended_rgb = (1 - influence_strength) * rgb1 + influence_strength * rgb2
            return self._rgb_to_hex(blended_rgb)
        except Exception as e:
            self.logger.error(f"Error blending colors: {e}")
            return '#FFFFFF'  # Default to white on error

    def _hex_to_rgb(self, hex_color):
        """
        Converts a hex color code to an RGB tuple.

        Parameters:
        - hex_color (str): Hex color code.

        Returns:
        - tuple: RGB values.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        """
        Converts an RGB tuple to a hex color code.

        Parameters:
        - rgb (tuple): RGB values.

        Returns:
        - str: Hex color code.
        """
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def display_matrix(self):
        """
        Placeholder method to display the matrix.
        Implement your own visualization logic here.
        """
        pass  # Implement as needed

    def symmetrical_matrix_transformation(self):
        """
        Transforms the matrix to emphasize hierarchical relationships by ensuring symmetry.
        """
        # Example Transformation: Amplify intra-category connections
        for i, label1 in enumerate(self.labels):
            for j, label2 in enumerate(self.labels):
                if label1.split('_')[0][0] == label2.split('_')[0][0]:
                    self.matrix[i][j] *= 1.2  # Increase the weight for the same main category
        self.logger.info("Symmetrical matrix transformation applied to emphasize hierarchical relationships.")

    def _initialize_connections(self):
        """
        Placeholder method to initialize connections.
        Implement your own logic here if needed.
        """
        pass  # Implement as needed

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
    # Initialize the Fractal Identity Matrix (FIM) with the defined categories and tokens
    fim = FractalIdentityMatrix(
        main_categories=MAIN_CATEGORIES,
        tokens=TOKENS,
        influence_factor=0.5,
        threshold=0.3
    )

    # Perform symmetrical matrix transformation to emphasize hierarchical relationships
    fim.symmetrical_matrix_transformation()

    # Display the influence matrix
    fim.display_matrix()

    # Additional operations like visualization can be called here
