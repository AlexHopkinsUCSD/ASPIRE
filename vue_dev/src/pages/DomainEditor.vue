<script>
export default {
    name: 'DomainEditor',
    friendly_name: "Domain Editor",
    icon: "/static/assets/icon-DomainEditor.png",
    props: {
        msg: String
    }
}
</script>

<script setup>
import NewConceptModal from "../components/NewConceptModal.vue";
import DomainDag from "../components/domain_dag/DomainDag.vue"
import DomainDagUtilities from "../utils/DagUtils.js"
import ModuleMenu from "../components/module_menu/ModuleMenu.vue"
import { ref } from "vue"


const nodes = {
    'concept_1': {'name': 'Classify a real number as a natural, whole, integer, rational, or irrational number', 'id': 'concept_1', 'module': [], 'params': {}},
    'concept_2': {'name': 'Introduction to Fractions', 'id': 'concept_2', 'module': [], 'params': {}},
    'concept_3': {'name': 'Perform calculations using the order of operations', 'id': 'concept_3', 'module': [], 'params': {}},
    'concept_4': {'name': 'Introduction to Exponents', 'id': 'concept_4', 'module': [], 'params': {}},
    'concept_5': {'name': 'Use the commutative, associative, distributive, inverse, and identity properties of real numbers', 'id': 'concept_5', 'module': [], 'params': {}},
    'concept_6': {'name': 'Evaluate algebraic expressions', 'id': 'concept_6', 'module': [], 'params': {}},
    'concept_7': {'name': 'Substitution', 'id': 'concept_7', 'module': [], 'params': {}},
    'concept_8': {'name': 'Simplify algebraic expressions', 'id': 'concept_8', 'module': [], 'params': {}},
    'concept_9': {'name': 'Use the product rule of exponents for same base multiplication', 'id': 'concept_9', 'module': [], 'params': {}},
    'concept_10': {'name': 'Concept of Exponents', 'id': 'concept_10', 'module': [], 'params': {}},
    'concept_11': {'name': 'Use the quotient rule of exponents for same base division', 'id': 'concept_11', 'module': [], 'params': {}},
    'concept_12': {'name': 'Use the power rule for raising exponents to another power', 'id': 'concept_12', 'module': [], 'params': {}},
    'concept_13': {'name': 'Apply the zero exponent rule', 'id': 'concept_13', 'module': [], 'params': {}},
    'concept_14': {'name': 'Apply the negative exponent rule for reciprocal expressions', 'id': 'concept_14', 'module': [], 'params': {}},
    'concept_15': {'name': 'Find the power of a product and quotient', 'id': 'concept_15', 'module': [], 'params': {}},
    'concept_16': {'name': 'Simplify exponential expressions', 'id': 'concept_16', 'module': [], 'params': {}},
    'concept_17': {'name': 'Use scientific notation for very large or small numbers', 'id': 'concept_17', 'module': [], 'params': {}},
    'concept_18': {'name': 'Evaluate square roots', 'id': 'concept_18', 'module': [], 'params': {}},
    'concept_19': {'name': 'Definition of Square Root', 'id': 'concept_19', 'module': [], 'params': {}},
    'concept_20': {'name': 'Use the product rule to simplify square roots', 'id': 'concept_20', 'module': [], 'params': {}},
    'concept_21': {'name': 'Prime Factorization', 'id': 'concept_21', 'module': [], 'params': {}},
    'concept_22': {'name': 'Use the quotient rule to simplify square roots', 'id': 'concept_22', 'module': [], 'params': {}},
    'concept_23': {'name': 'Simplifying Fractions', 'id': 'concept_23', 'module': [], 'params': {}},
    'concept_24': {'name': 'Add and subtract square roots', 'id': 'concept_24', 'module': [], 'params': {}},
    'concept_25': {'name': 'Combining Like Terms', 'id': 'concept_25', 'module': [], 'params': {}},
    'concept_26': {'name': 'Rationalize denominators', 'id': 'concept_26', 'module': [], 'params': {}},
    'concept_27': {'name': 'Use rational roots', 'id': 'concept_27', 'module': [], 'params': {}},
    'concept_28': {'name': 'Properties of Exponents', 'id': 'concept_28', 'module': [], 'params': {}},
    'concept_29': {'name': 'Identify the degree and leading coefficient of polynomials', 'id': 'concept_29', 'module': [], 'params': {}},
    'concept_30': {'name': 'Add and subtract polynomials', 'id': 'concept_30', 'module': [], 'params': {}},
    'concept_31': {'name': 'Multiply polynomials', 'id': 'concept_31', 'module': [], 'params': {}},
    'concept_32': {'name': 'Use FOIL to multiply binomials', 'id': 'concept_32', 'module': [], 'params': {}},
    'concept_33': {'name': 'Definition of a Binomial', 'id': 'concept_33', 'module': [], 'params': {}},
    'concept_34': {'name': 'Perform operations with polynomials of several variables', 'id': 'concept_34', 'module': [], 'params': {}},
    'concept_35': {'name': 'Basic Arithmetic Operations with Variables', 'id': 'concept_35', 'module': [], 'params': {}},
    'concept_36': {'name': 'Factor the greatest common factor of a polynomial', 'id': 'concept_36', 'module': [], 'params': {}},
    'concept_37': {'name': 'Understanding Multiples and Factors', 'id': 'concept_37', 'module': [], 'params': {}},
    'concept_38': {'name': 'Greatest Common Factor (GCF)', 'id': 'concept_38', 'module': [], 'params': {}},
    'concept_39': {'name': 'Distributive Property', 'id': 'concept_39', 'module': [], 'params': {}},
    'concept_40': {'name': 'Factor a trinomial', 'id': 'concept_40', 'module': [], 'params': {}},
    'concept_41': {'name': 'Recognizing Trinomials', 'id': 'concept_41', 'module': [], 'params': {}},
    'concept_42': {'name': 'Factor by grouping', 'id': 'concept_42', 'module': [], 'params': {}},
    'concept_43': {'name': 'Grouping Terms', 'id': 'concept_43', 'module': [], 'params': {}},
    'concept_44': {'name': 'Factor a perfect square trinomial', 'id': 'concept_44', 'module': [], 'params': {}},
    'concept_45': {'name': 'Factor a difference of squares', 'id': 'concept_45', 'module': [], 'params': {}},
    'concept_46': {'name': 'Factor the sum and difference of cubes', 'id': 'concept_46', 'module': [], 'params': {}},
    'concept_47': {'name': 'Factor expressions using fractional or negative exponents', 'id': 'concept_47', 'module': [], 'params': {}},
    'concept_48': {'name': 'Basic Properties of Exponents', 'id': 'concept_48', 'module': [], 'params': {}},
    'concept_49': {'name': 'Simplify rational expressions by canceling common factors', 'id': 'concept_49', 'module': [], 'params': {}},
    'concept_50': {'name': 'Basic Properties of Fractions', 'id': 'concept_50', 'module': [], 'params': {}},
    'concept_51': {'name': 'Multiply rational expressions', 'id': 'concept_51', 'module': [], 'params': {}},
    'concept_52': {'name': 'Divide rational expressions by multiplying by the reciprocal', 'id': 'concept_52', 'module': [], 'params': {}},
    'concept_53': {'name': 'Reciprocal Concept', 'id': 'concept_53', 'module': [], 'params': {}},
    'concept_54': {'name': 'Add or subtract rational expressions with a common denominator', 'id': 'concept_54', 'module': [], 'params': {}},
    'concept_55': {'name': 'Simplify complex rational expressions', 'id': 'concept_55', 'module': [], 'params': {}},
    'concept_56': {'name': 'Operations with fractions', 'id': 'concept_56', 'module': [], 'params': {}},
    'concept_57': {'name': 'Determine whether a relation represents a function', 'id': 'concept_57', 'module': [], 'params': {}},
    'concept_58': {'name': 'Understanding of Sets and Pairs', 'id': 'concept_58', 'module': [], 'params': {}},
    'concept_59': {'name': 'Basic Idea of Mapping', 'id': 'concept_59', 'module': [], 'params': {}},
    'concept_60': {'name': 'Find the value of a function', 'id': 'concept_60', 'module': [], 'params': {}},
    'concept_61': {'name': 'Determine whether a function is one-to-one', 'id': 'concept_61', 'module': [], 'params': {}},
    'concept_62': {'name': 'Basic Set Theory', 'id': 'concept_62', 'module': [], 'params': {}},
    'concept_63': {'name': 'Use the vertical line test to identify functions', 'id': 'concept_63', 'module': [], 'params': {}},
    'concept_64': {'name': 'Graph Reading', 'id': 'concept_64', 'module': [], 'params': {}},
    'concept_65': {'name': 'Graph the functions listed in the library of functions', 'id': 'concept_65', 'module': [], 'params': {}},
    'concept_66': {'name': 'Scale and Plotting on Cartesian Plane', 'id': 'concept_66', 'module': [], 'params': {}},
    'concept_67': {'name': 'Shape Recognition', 'id': 'concept_67', 'module': [], 'params': {}},
    'concept_68': {'name': 'Find the domain of a function defined by an equation', 'id': 'concept_68', 'module': [], 'params': {}},
    'concept_69': {'name': 'Understanding of Real Numbers', 'id': 'concept_69', 'module': [], 'params': {}},
    'concept_70': {'name': 'Graph piecewise-defined functions', 'id': 'concept_70', 'module': [], 'params': {}},
    'concept_71': {'name': 'Find the average rate of change of a function', 'id': 'concept_71', 'module': [], 'params': {}},
    'concept_72': {'name': 'Coordinate Systems', 'id': 'concept_72', 'module': [], 'params': {}},
    'concept_73': {'name': 'Use a graph to determine where a function is increasing, decreasing, or constant', 'id': 'concept_73', 'module': [], 'params': {}},
    'concept_74': {'name': 'Use a graph to locate local maxima and local minima', 'id': 'concept_74', 'module': [], 'params': {}},
    'concept_75': {'name': 'Use a graph to locate the absolute maximum and absolute minimum', 'id': 'concept_75', 'module': [], 'params': {}},
    'concept_76': {'name': 'Combine functions using algebraic operations', 'id': 'concept_76', 'module': [], 'params': {}},
    'concept_77': {'name': 'Create a new function by composition of functions', 'id': 'concept_77', 'module': [], 'params': {}},
    'concept_78': {'name': 'Evaluate composite functions', 'id': 'concept_78', 'module': [], 'params': {}},
    'concept_79': {'name': 'Find the domain of a composite function', 'id': 'concept_79', 'module': [], 'params': {}},
    'concept_80': {'name': 'Understanding Restrictions on Domains', 'id': 'concept_80', 'module': [], 'params': {}},
    'concept_81': {'name': 'Set Theory and Interval Notation', 'id': 'concept_81', 'module': [], 'params': {}},
    'concept_82': {'name': 'Decompose a composite function into its component functions', 'id': 'concept_82', 'module': [], 'params': {}},
    'concept_83': {'name': 'Graph functions using vertical and horizontal shifts', 'id': 'concept_83', 'module': [], 'params': {}},
    'concept_84': {'name': 'Coordinate Plane Knowledge', 'id': 'concept_84', 'module': [], 'params': {}},
    'concept_85': {'name': 'Graph functions using reflections about the x-axis and the y-axis', 'id': 'concept_85', 'module': [], 'params': {}},
    'concept_86': {'name': 'Determine whether a function is even, odd, or neither from its graph', 'id': 'concept_86', 'module': [], 'params': {}},
    'concept_87': {'name': 'Graph functions using compressions and stretches', 'id': 'concept_87', 'module': [], 'params': {}},
    'concept_88': {'name': 'Combine transformations', 'id': 'concept_88', 'module': [], 'params': {}},
    'concept_89': {'name': 'Graph an absolute value function', 'id': 'concept_89', 'module': [], 'params': {}},
    'concept_90': {'name': 'Understanding of Absolute Value', 'id': 'concept_90', 'module': [], 'params': {}},
    'concept_91': {'name': 'Solve an absolute value equation', 'id': 'concept_91', 'module': [], 'params': {}},
    'concept_92': {'name': 'Absolute Value Properties', 'id': 'concept_92', 'module': [], 'params': {}},
    'concept_93': {'name': 'Verify inverse functions', 'id': 'concept_93', 'module': [], 'params': {}},
    'concept_94': {'name': 'Understanding of Functions', 'id': 'concept_94', 'module': [], 'params': {}},
    'concept_95': {'name': 'Composition of Functions', 'id': 'concept_95', 'module': [], 'params': {}},
    'concept_96': {'name': 'Determine the domain and range of an inverse function, and restrict the domain of a function to make it one-to-one', 'id': 'concept_96', 'module': [], 'params': {}},
    'concept_97': {'name': 'Domain and Range', 'id': 'concept_97', 'module': [], 'params': {}},
    'concept_98': {'name': 'One-to-One Functions', 'id': 'concept_98', 'module': [], 'params': {}},
    'concept_99': {'name': 'Horizontal Line Test', 'id': 'concept_99', 'module': [], 'params': {}},
    'concept_100': {'name': 'Find or evaluate the inverse of a function', 'id': 'concept_100', 'module': [], 'params': {}},
    'concept_101': {'name': 'Use the graph of a one-to-one function to graph its inverse function on the same axes', 'id': 'concept_101', 'module': [], 'params': {}},
    'concept_102': {'name': 'Represent a linear function', 'id': 'concept_102', 'module': [], 'params': {}},
    'concept_103': {'name': 'Understanding of a function as a mapping from inputs to outputs', 'id': 'concept_103', 'module': [], 'params': {}},
    'concept_104': {'name': 'Determine whether a linear function is increasing, decreasing, or constant', 'id': 'concept_104', 'module': [], 'params': {}},
    'concept_105': {'name': 'Interpret slope as a rate of change', 'id': 'concept_105', 'module': [], 'params': {}},
    'concept_106': {'name': 'Understanding ratios and proportions', 'id': 'concept_106', 'module': [], 'params': {}},
    'concept_107': {'name': 'Write and interpret an equation for a linear function', 'id': 'concept_107', 'module': [], 'params': {}},
    'concept_108': {'name': 'Substitution', 'id': 'concept_108', 'module': [], 'params': {}},
    'concept_109': {'name': 'Understanding of coordinate systems (x and y axes)', 'id': 'concept_109', 'module': [], 'params': {}},
    'concept_110': {'name': 'Graph linear functions', 'id': 'concept_110', 'module': [], 'params': {}},
    'concept_111': {'name': 'Determine whether lines are parallel or perpendicular', 'id': 'concept_111', 'module': [], 'params': {}},
    'concept_112': {'name': 'Write the equation of a line parallel or perpendicular to a given line', 'id': 'concept_112', 'module': [], 'params': {}},
    'concept_113': {'name': 'Knowledge of slope (m)', 'id': 'concept_113', 'module': [], 'params': {}},
    'concept_114': {'name': 'Basic understanding of the slope-intercept form y = mx + b and how to calculate slope (m) and intercept (b)', 'id': 'concept_114', 'module': [], 'params': {}},
    'concept_115': {'name': 'Knowledge of slope characteristics', 'id': 'concept_115', 'module': [], 'params': {}},
    'concept_116': {'name': 'Understanding how to find a slope from an equation', 'id': 'concept_116', 'module': [], 'params': {}},
    'concept_117': {'name': 'Skills to apply the point-slope form of a line equation when given a point and a slope', 'id': 'concept_117', 'module': [], 'params': {}},
    'concept_118': {'name': 'Solve a system of linear equations', 'id': 'concept_118', 'module': [], 'params': {}},
    'concept_119': {'name': 'Build linear models from verbal descriptions', 'id': 'concept_119', 'module': [], 'params': {}},
    'concept_120': {'name': 'Basic understanding of linear relationships', 'id': 'concept_120', 'module': [], 'params': {}},
    'concept_121': {'name': 'Model a set of data with a linear function', 'id': 'concept_121', 'module': [], 'params': {}},
    'concept_122': {'name': 'Understanding of best-fit lines and the method of least squares', 'id': 'concept_122', 'module': [], 'params': {}},
    'concept_123': {'name': 'Use problem strategies for any type of function, focusing on identifying variables and key values such as slope and initial value', 'id': 'concept_123', 'module': [], 'params': {}},
    'concept_124': {'name': 'Fundamental understanding of functions', 'id': 'concept_124', 'module': [], 'params': {}},
    'concept_125': {'name': 'Draw and interpret scatter diagrams', 'id': 'concept_125', 'module': [], 'params': {}},
    'concept_126': {'name': 'Use a graphing utility to find the line of best fit', 'id': 'concept_126', 'module': [], 'params': {}},
    'concept_127': {'name': 'Distinguish between linear and nonlinear relations', 'id': 'concept_127', 'module': [], 'params': {}},
    'concept_128': {'name': 'Fit a regression line to a set of data and use the linear model to make predictions', 'id': 'concept_128', 'module': [], 'params': {}},
    'concept_129': {'name': 'Express square roots of negative numbers as multiples of i', 'id': 'concept_129', 'module': [], 'params': {}},
    'concept_130': {'name': 'Understanding of square roots and radicals', 'id': 'concept_130', 'module': [], 'params': {}},
    'concept_131': {'name': 'Basic number theory', 'id': 'concept_131', 'module': [], 'params': {}},
    'concept_132': {'name': 'Plot complex numbers on the complex plane', 'id': 'concept_132', 'module': [], 'params': {}},
    'concept_133': {'name': 'Cartesian coordinate system', 'id': 'concept_133', 'module': [], 'params': {}},
    'concept_134': {'name': 'Basic geometry', 'id': 'concept_134', 'module': [], 'params': {}},
    'concept_135': {'name': 'Add and subtract complex numbers', 'id': 'concept_135', 'module': [], 'params': {}},
    'concept_136': {'name': 'Multiply and divide complex numbers', 'id': 'concept_136', 'module': [], 'params': {}},
    'concept_137': {'name': 'Use of the distributive property', 'id': 'concept_137', 'module': [], 'params': {}},
    'concept_138': {'name': 'Conjugates and rationalizing denominators', 'id': 'concept_138', 'module': [], 'params': {}},
    'concept_139': {'name': 'Recognize characteristics of parabolas', 'id': 'concept_139', 'module': [], 'params': {}},
    'concept_140': {'name': 'Basic understanding of functions', 'id': 'concept_140', 'module': [], 'params': {}},
    'concept_141': {'name': 'Understand how the graph of a parabola is related to its quadratic function', 'id': 'concept_141', 'module': [], 'params': {}},
    'concept_142': {'name': 'Coordinate plane knowledge', 'id': 'concept_142', 'module': [], 'params': {}},
    'concept_143': {'name': 'Concept of intercepts', 'id': 'concept_143', 'module': [], 'params': {}},
    'concept_144': {'name': 'Determine a quadratic function’s minimum or maximum value', 'id': 'concept_144', 'module': [], 'params': {}},
    'concept_145': {'name': 'Concept of extrema in mathematics', 'id': 'concept_145', 'module': [], 'params': {}},
    'concept_146': {'name': 'Solve problems involving a quadratic function’s minimum or maximum value', 'id': 'concept_146', 'module': [], 'params': {}},
    'concept_147': {'name': 'Algebraic manipulation', 'id': 'concept_147', 'module': [], 'params': {}},
    'concept_148': {'name': 'Identify power functions', 'id': 'concept_148', 'module': [], 'params': {}},
    'concept_149': {'name': 'Exponents and powers', 'id': 'concept_149', 'module': [], 'params': {}},
    'concept_150': {'name': 'Function concept', 'id': 'concept_150', 'module': [], 'params': {}},
    'concept_151': {'name': 'Identify end behavior of power functions', 'id': 'concept_151', 'module': [], 'params': {}},
    'concept_152': {'name': 'Infinity', 'id': 'concept_152', 'module': [], 'params': {}},
    'concept_153': {'name': 'Behavior of exponential growth and decay', 'id': 'concept_153', 'module': [], 'params': {}},
    'concept_154': {'name': 'Identify polynomial functions', 'id': 'concept_154', 'module': [], 'params': {}},
    'concept_155': {'name': 'Identify the degree and leading coefficient of polynomial functions', 'id': 'concept_155', 'module': [], 'params': {}},
    'concept_156': {'name': 'Recognize characteristics of graphs of polynomial functions', 'id': 'concept_156', 'module': [], 'params': {}},
    'concept_157': {'name': 'Understanding basic graph shapes', 'id': 'concept_157', 'module': [], 'params': {}},
    'concept_158': {'name': 'Use factoring to find zeros of polynomial functions', 'id': 'concept_158', 'module': [], 'params': {}},
    'concept_159': {'name': 'Factoring techniques', 'id': 'concept_159', 'module': [], 'params': {}},
    'concept_160': {'name': 'Identify zeros and their multiplicities', 'id': 'concept_160', 'module': [], 'params': {}},
    'concept_161': {'name': 'Determine end behavior', 'id': 'concept_161', 'module': [], 'params': {}},
    'concept_162': {'name': 'Behavior of functions as x approaches infinity', 'id': 'concept_162', 'module': [], 'params': {}},
    'concept_163': {'name': 'Understand the relationship between degree and turning points', 'id': 'concept_163', 'module': [], 'params': {}},
    'concept_164': {'name': 'Graph polynomial functions', 'id': 'concept_164', 'module': [], 'params': {}},
    'concept_165': {'name': 'Use the Intermediate Value Theorem', 'id': 'concept_165', 'module': [], 'params': {}},
    'concept_166': {'name': 'Use long division to divide polynomials', 'id': 'concept_166', 'module': [], 'params': {}},
    'concept_167': {'name': 'Long division of numbers', 'id': 'concept_167', 'module': [], 'params': {}},
    'concept_168': {'name': 'Use synthetic division to divide polynomials', 'id': 'concept_168', 'module': [], 'params': {}},
    'concept_169': {'name': 'Basic operations with polynomials', 'id': 'concept_169', 'module': [], 'params': {}},
    'concept_170': {'name': 'Zeroes of polynomials', 'id': 'concept_170', 'module': [], 'params': {}},
    'concept_171': {'name': 'Evaluate a polynomial using the Remainder Theorem', 'id': 'concept_171', 'module': [], 'params': {}},
    'concept_172': {'name': 'Substitution', 'id': 'concept_172', 'module': [], 'params': {}},
    'concept_173': {'name': 'Basic division', 'id': 'concept_173', 'module': [], 'params': {}},
    'concept_174': {'name': 'Use the Factor Theorem to solve a polynomial equation', 'id': 'concept_174', 'module': [], 'params': {}},
    'concept_175': {'name': 'Factorization skills', 'id': 'concept_175', 'module': [], 'params': {}},
    'concept_176': {'name': 'Understanding of roots and zeros', 'id': 'concept_176', 'module': [], 'params': {}},
    'concept_177': {'name': 'Use the Rational Zero Theorem to find rational zeros', 'id': 'concept_177', 'module': [], 'params': {}},
    'concept_178': {'name': 'Prime factorization', 'id': 'concept_178', 'module': [], 'params': {}},
    'concept_179': {'name': 'Find zeros of a polynomial function', 'id': 'concept_179', 'module': [], 'params': {}},
    'concept_180': {'name': 'Algebraic solving techniques', 'id': 'concept_180', 'module': [], 'params': {}},
    'concept_181': {'name': 'Use the Linear Factorization Theorem to find polynomials with given zeros', 'id': 'concept_181', 'module': [], 'params': {}},
    'concept_182': {'name': 'Use Descartes’ Rule of Signs', 'id': 'concept_182', 'module': [], 'params': {}},
    'concept_183': {'name': 'Solve real-world applications of polynomial equations', 'id': 'concept_183', 'module': [], 'params': {}},
    'concept_184': {'name': 'Use arrow notation', 'id': 'concept_184', 'module': [], 'params': {}},
    'concept_185': {'name': 'Understanding of function behavior', 'id': 'concept_185', 'module': [], 'params': {}},
    'concept_186': {'name': 'Solve applied problems involving rational functions', 'id': 'concept_186', 'module': [], 'params': {}},
    'concept_187': {'name': 'Find the domains of rational functions', 'id': 'concept_187', 'module': [], 'params': {}},
    'concept_188': {'name': 'Algebraic manipulation', 'id': 'concept_188', 'module': [], 'params': {}},
    'concept_189': {'name': 'Identify vertical asymptotes', 'id': 'concept_189', 'module': [], 'params': {}},
    'concept_190': {'name': 'Identify horizontal asymptotes', 'id': 'concept_190', 'module': [], 'params': {}},
    'concept_191': {'name': 'Graph rational functions', 'id': 'concept_191', 'module': [], 'params': {}},
    'concept_192': {'name': 'Find the inverse of an invertible polynomial function', 'id': 'concept_192', 'module': [], 'params': {}},
    'concept_193': {'name': 'Understanding of functions and inverses', 'id': 'concept_193', 'module': [], 'params': {}},
    'concept_194': {'name': 'Restrict the domain to find the inverse of a polynomial function', 'id': 'concept_194', 'module': [], 'params': {}},
    'concept_195': {'name': 'Domain and range concepts', 'id': 'concept_195', 'module': [], 'params': {}},
    'concept_196': {'name': 'Solve direct variation problems', 'id': 'concept_196', 'module': [], 'params': {}},
    'concept_197': {'name': 'Algebraic equations', 'id': 'concept_197', 'module': [], 'params': {}},
    'concept_198': {'name': 'Solve inverse variation problems', 'id': 'concept_198', 'module': [], 'params': {}},
    'concept_199': {'name': 'Inverse relationships', 'id': 'concept_199', 'module': [], 'params': {}},
    'concept_200': {'name': 'Manipulation of rational expressions', 'id': 'concept_200', 'module': [], 'params': {}},
    'concept_201': {'name': 'Solve problems involving joint variation', 'id': 'concept_201', 'module': [], 'params': {}},
    'concept_202': {'name': 'Evaluate exponential functions', 'id': 'concept_202', 'module': [], 'params': {}},
    'concept_203': {'name': 'Understanding of powers and indices', 'id': 'concept_203', 'module': [], 'params': {}},
    'concept_204': {'name': 'Find the equation of an exponential function', 'id': 'concept_204', 'module': [], 'params': {}},
    'concept_205': {'name': 'Understanding of the form of an exponential function y = ab^x', 'id': 'concept_205', 'module': [], 'params': {}},
    'concept_206': {'name': 'Basic algebraic skills to manipulate equations and solve for unknowns', 'id': 'concept_206', 'module': [], 'params': {}},
    'concept_207': {'name': 'Use compound interest formulas', 'id': 'concept_207', 'module': [], 'params': {}},
    'concept_208': {'name': 'Basic understanding of percentages and their conversion to decimal form for calculation purposes', 'id': 'concept_208', 'module': [], 'params': {}},
    'concept_209': {'name': 'Ability to substitute values into formulas and solve using basic algebra', 'id': 'concept_209', 'module': [], 'params': {}},
    'concept_210': {'name': 'Evaluate exponential functions with base e', 'id': 'concept_210', 'module': [], 'params': {}},
    'concept_211': {'name': 'Understanding that e is an irrational number approximately equal to 2.71828', 'id': 'concept_211', 'module': [], 'params': {}},
    'concept_212': {'name': 'Comprehension of natural logarithms', 'id': 'concept_212', 'module': [], 'params': {}},
    'concept_213': {'name': 'Graph exponential functions', 'id': 'concept_213', 'module': [], 'params': {}},
    'concept_214': {'name': 'Basic understanding of the Cartesian coordinate system, including the ability to plot points on a graph', 'id': 'concept_214', 'module': [], 'params': {}},
    'concept_215': {'name': 'Recognition of how the values of x affect the output of functions y = ab^x', 'id': 'concept_215', 'module': [], 'params': {}},
    'concept_216': {'name': 'Graph exponential functions using transformations', 'id': 'concept_216', 'module': [], 'params': {}},
    'concept_217': {'name': 'Convert from logarithmic to exponential form', 'id': 'concept_217', 'module': [], 'params': {}},
    'concept_218': {'name': 'Basic understanding of the relationship between exponentials and logarithms', 'id': 'concept_218', 'module': [], 'params': {}},
    'concept_219': {'name': 'Convert from exponential to logarithmic form', 'id': 'concept_219', 'module': [], 'params': {}},
    'concept_220': {'name': 'Evaluate logarithms', 'id': 'concept_220', 'module': [], 'params': {}},
    'concept_221': {'name': 'Use common logarithms', 'id': 'concept_221', 'module': [], 'params': {}},
    'concept_222': {'name': 'Understanding that common logarithms (base 10)', 'id': 'concept_222', 'module': [], 'params': {}},
    'concept_223': {'name': 'Use natural logarithms', 'id': 'concept_223', 'module': [], 'params': {}},
    'concept_224': {'name': 'Knowledge of natural logarithms ln, which have the base e', 'id': 'concept_224', 'module': [], 'params': {}},
    'concept_225': {'name': 'Identify the domain of a logarithmic function', 'id': 'concept_225', 'module': [], 'params': {}},
    'concept_226': {'name': 'Basic knowledge of set notation to express domains', 'id': 'concept_226', 'module': [], 'params': {}},
    'concept_227': {'name': 'Behavior of logarithmic functions', 'id': 'concept_227', 'module': [], 'params': {}},
    'concept_228': {'name': 'Graph logarithmic functions', 'id': 'concept_228', 'module': [], 'params': {}},
    'concept_229': {'name': 'Knowledge of transformations such as translations, reflections, and scaling as they apply to logarithmic functions', 'id': 'concept_229', 'module': [], 'params': {}},
    'concept_230': {'name': 'Use the product rule for logarithms', 'id': 'concept_230', 'module': [], 'params': {}},
    'concept_231': {'name': 'Use the quotient rule for logarithms', 'id': 'concept_231', 'module': [], 'params': {}},
    'concept_232': {'name': 'Use the power rule for logarithms', 'id': 'concept_232', 'module': [], 'params': {}},
    'concept_233': {'name': 'Expand logarithmic expressions', 'id': 'concept_233', 'module': [], 'params': {}},
    'concept_234': {'name': 'Condense logarithmic expressions', 'id': 'concept_234', 'module': [], 'params': {}},
    'concept_235': {'name': 'Use the change-of-base formula for logarithms', 'id': 'concept_235', 'module': [], 'params': {}},
    'concept_236': {'name': 'Use like bases to solve exponential equations', 'id': 'concept_236', 'module': [], 'params': {}},
    'concept_237': {'name': 'Use logarithms to solve exponential equations', 'id': 'concept_237', 'module': [], 'params': {}},
    'concept_238': {'name': 'Use the definition of a logarithm to solve logarithmic equations', 'id': 'concept_238', 'module': [], 'params': {}},
    'concept_239': {'name': 'Use the one-to-one property of logarithms to solve logarithmic equations', 'id': 'concept_239', 'module': [], 'params': {}},
    'concept_240': {'name': 'Solve applied problems involving exponential and logarithmic equations', 'id': 'concept_240', 'module': [], 'params': {}},
    'concept_241': {'name': 'Model exponential growth and decay', 'id': 'concept_241', 'module': [], 'params': {}},
    'concept_242': {'name': 'Use Newton’s Law of Cooling', 'id': 'concept_242', 'module': [], 'params': {}},
    'concept_243': {'name': 'Use logistic-growth models', 'id': 'concept_243', 'module': [], 'params': {}},
    'concept_244': {'name': 'Knowledge of logistic growth', 'id': 'concept_244', 'module': [], 'params': {}},
    'concept_245': {'name': 'Choose an appropriate model for data', 'id': 'concept_245', 'module': [], 'params': {}},
    'concept_246': {'name': 'Express an exponential model in base e', 'id': 'concept_246', 'module': [], 'params': {}},
    'concept_247': {'name': 'Draw angles in standard position', 'id': 'concept_247', 'module': [], 'params': {}},
    'concept_248': {'name': 'Cartesian Coordinate System', 'id': 'concept_248', 'module': [], 'params': {}},
    'concept_249': {'name': 'Ray Concepts', 'id': 'concept_249', 'module': [], 'params': {}},
    'concept_250': {'name': 'Determine coterminal angles', 'id': 'concept_250', 'module': [], 'params': {}},
    'concept_251': {'name': 'Degree Measurement', 'id': 'concept_251', 'module': [], 'params': {}},
    'concept_252': {'name': 'Convert between degrees and radians', 'id': 'concept_252', 'module': [], 'params': {}},
    'concept_253': {'name': 'Pi (π) Concept', 'id': 'concept_253', 'module': [], 'params': {}},
    'concept_254': {'name': 'Proportional Reasoning', 'id': 'concept_254', 'module': [], 'params': {}},
    'concept_255': {'name': 'Find the length of a circular arc', 'id': 'concept_255', 'module': [], 'params': {}},
    'concept_256': {'name': 'Determine the area of a sector of a circle', 'id': 'concept_256', 'module': [], 'params': {}},
    'concept_257': {'name': 'Area Calculation', 'id': 'concept_257', 'module': [], 'params': {}},
    'concept_258': {'name': 'Define and use the unit circle', 'id': 'concept_258', 'module': [], 'params': {}},
    'concept_259': {'name': 'Understanding of π (Pi)', 'id': 'concept_259', 'module': [], 'params': {}},
    'concept_260': {'name': 'Radians and Degrees', 'id': 'concept_260', 'module': [], 'params': {}},
    'concept_261': {'name': 'Define sine and cosine functions using the unit circle', 'id': 'concept_261', 'module': [], 'params': {}},
    'concept_262': {'name': 'Periodic Functions', 'id': 'concept_262', 'module': [], 'params': {}},
    'concept_263': {'name': 'Use the domain and period to sketch graphs of sine and cosine functions', 'id': 'concept_263', 'module': [], 'params': {}},
    'concept_264': {'name': 'Understanding of Periodicity in Functions', 'id': 'concept_264', 'module': [], 'params': {}},
    'concept_265': {'name': 'Use sine and cosine functions to model real-life data', 'id': 'concept_265', 'module': [], 'params': {}},
    'concept_266': {'name': 'Define the tangent function', 'id': 'concept_266', 'module': [], 'params': {}},
    'concept_267': {'name': 'Concept of Slope', 'id': 'concept_267', 'module': [], 'params': {}},
    'concept_268': {'name': 'Relationships between Sides of Right Triangles', 'id': 'concept_268', 'module': [], 'params': {}},
    'concept_269': {'name': 'Define the reciprocal trigonometric functions', 'id': 'concept_269', 'module': [], 'params': {}},
    'concept_270': {'name': 'Reciprocal Relationships', 'id': 'concept_270', 'module': [], 'params': {}},
    'concept_271': {'name': 'Use the domain and period to sketch graphs of all six trigonometric functions', 'id': 'concept_271', 'module': [], 'params': {}},
    'concept_272': {'name': 'Periodic Behavior of Functions', 'id': 'concept_272', 'module': [], 'params': {}},
    'concept_273': {'name': 'Apply trigonometric functions to solve real-life problems', 'id': 'concept_273', 'module': [], 'params': {}},
    'concept_274': {'name': 'Use right triangles to evaluate trigonometric functions', 'id': 'concept_274', 'module': [], 'params': {}},
    'concept_275': {'name': 'Ratios and Proportions', 'id': 'concept_275', 'module': [], 'params': {}},
    'concept_276': {'name': 'Find function values for π/3, π/6, π/4', 'id': 'concept_276', 'module': [], 'params': {}},
    'concept_277': {'name': 'Use cofunctions of complementary angles', 'id': 'concept_277', 'module': [], 'params': {}},
    'concept_278': {'name': 'Use the definitions of trigonometric functions of any angle', 'id': 'concept_278', 'module': [], 'params': {}},
    'concept_279': {'name': 'Use right triangle trigonometry to solve applied problems', 'id': 'concept_279', 'module': [], 'params': {}},
    'concept_280': {'name': 'Proportions and Ratios', 'id': 'concept_280', 'module': [], 'params': {}},
    'concept_281': {'name': 'Concept of fractions and how to simplify them', 'id': 'concept_281', 'module': [], 'params': {}},
    'concept_282': {'name': 'Percentage Calculation', 'id': 'concept_282', 'module': [], 'params': {}},
    'concept_283': {'name': 'Understanding of decimals and their relation to percentages', 'id': 'concept_283', 'module': [], 'params': {}},
    'concept_284': {'name': 'Basic arithmetic operations with decimals', 'id': 'concept_284', 'module': [], 'params': {}},
    'concept_285': {'name': 'Rounding', 'id': 'concept_285', 'module': [], 'params': {}},
    'concept_286': {'name': 'Alternate Interior Angles', 'id': 'concept_286', 'module': [], 'params': {}},
    'concept_287': {'name': 'Basic understanding of angles (acute, obtuse, right)', 'id': 'concept_287', 'module': [], 'params': {}},
    'concept_288': {'name': 'Concepts of parallel lines', 'id': 'concept_288', 'module': [], 'params': {}},
    'concept_289': {'name': 'Corresponding Angles', 'id': 'concept_289', 'module': [], 'params': {}},
    'concept_290': {'name': 'Identification of angles in various geometric figures', 'id': 'concept_290', 'module': [], 'params': {}},
    'concept_291': {'name': 'Basic angle measurement using a protractor', 'id': 'concept_291', 'module': [], 'params': {}},
    'concept_292': {'name': 'Supplementary Angles', 'id': 'concept_292', 'module': [], 'params': {}},
    'concept_293': {'name': 'Angle Relationships with Parallel Lines', 'id': 'concept_293', 'module': [], 'params': {}},
    'concept_294': {'name': 'Basic definitions of intersecting lines and points', 'id': 'concept_294', 'module': [], 'params': {}},
    'concept_295': {'name': 'Concept of a transversal cutting through parallel lines', 'id': 'concept_295', 'module': [], 'params': {}},
    'concept_296': {'name': 'Trigonometric Ratios', 'id': 'concept_296', 'module': [], 'params': {}},
    'concept_297': {'name': 'Basic understanding of ratios', 'id': 'concept_297', 'module': [], 'params': {}},
    'concept_298': {'name': 'Definition of sine, cosine, and tangent (in right triangles)', 'id': 'concept_298', 'module': [], 'params': {}},
    'concept_299': {'name': 'Right Triangle Properties', 'id': 'concept_299', 'module': [], 'params': {}},
    'concept_300': {'name': 'Similar Triangles', 'id': 'concept_300', 'module': [], 'params': {}},
    'concept_301': {'name': 'Concept of scaling and resizing in geometry', 'id': 'concept_301', 'module': [], 'params': {}},
    'concept_302': {'name': 'Trigonometry', 'id': 'concept_302', 'module': [], 'params': {}},
    'concept_303': {'name': 'Concept of angle and its measurement (degrees)', 'id': 'concept_303', 'module': [], 'params': {}},
    'concept_304': {'name': 'Properties of Equilateral Triangles', 'id': 'concept_304', 'module': [], 'params': {}},
    'concept_305': {'name': 'Understanding of congruent sides and angles in triangles', 'id': 'concept_305', 'module': [], 'params': {}},
    'concept_306': {'name': 'Formula for the Area of an Equilateral Triangle', 'id': 'concept_306', 'module': [], 'params': {}},
    'concept_307': {'name': 'Basic area calculation', 'id': 'concept_307', 'module': [], 'params': {}},
    'concept_308': {'name': 'Pythagorean Theorem', 'id': 'concept_308', 'module': [], 'params': {}},
    'concept_309': {'name': 'Concept of squares and square roots', 'id': 'concept_309', 'module': [], 'params': {}},
    'concept_310': {'name': "Heron's Formula", 'id': 'concept_310', 'module': [], 'params': {}},
    'concept_311': {'name': 'Basic algebraic manipulation and square root operations', 'id': 'concept_311', 'module': [], 'params': {}},
    'concept_312': {'name': 'Area of a Trapezoid', 'id': 'concept_312', 'module': [], 'params': {}},
    'concept_313': {'name': 'Understanding of parallel sides and height in figures', 'id': 'concept_313', 'module': [], 'params': {}},
    'concept_314': {'name': 'Properties of Trapezoids', 'id': 'concept_314', 'module': [], 'params': {}},
    'concept_315': {'name': 'Perimeter of a Rectangle', 'id': 'concept_315', 'module': [], 'params': {}},
    'concept_316': {'name': 'Area of a Rectangle', 'id': 'concept_316', 'module': [], 'params': {}},
    'concept_317': {'name': 'Perimeter of Composite Shapes', 'id': 'concept_317', 'module': [], 'params': {}},
    'concept_318': {'name': 'Area of Composite Shapes', 'id': 'concept_318', 'module': [], 'params': {}},
    'concept_319': {'name': 'Basic area calculations for simple geometric shapes (squares, rectangles, triangles)', 'id': 'concept_319', 'module': [], 'params': {}},
    'concept_320': {'name': 'Circle Geometry', 'id': 'concept_320', 'module': [], 'params': {}},
    'concept_321': {'name': 'Understanding of radius, diameter, and the concept of pi', 'id': 'concept_321', 'module': [], 'params': {}},
    'concept_322': {'name': 'Distance Formula', 'id': 'concept_322', 'module': [], 'params': {}},
    'concept_323': {'name': 'Understanding of the coordinate plane', 'id': 'concept_323', 'module': [], 'params': {}},
    'concept_324': {'name': 'Linear Pair', 'id': 'concept_324', 'module': [], 'params': {}},
    'Radicals and Rational Exponents': {'name': 'Radicals and Rational Exponents', 'id': 'Radicals and Rational Exponents', 'module': [], 'params': {}},
    'Exponents and Scientific Notation': {'name': 'Exponents and Scientific Notation', 'id': 'Exponents and Scientific Notation', 'module': [], 'params': {}},
    'Polynomials': {'name': 'Polynomials', 'id': 'Polynomials', 'module': [], 'params': {}},
    'Factoring Polynomials': {'name': 'Factoring Polynomials', 'id': 'Factoring Polynomials', 'module': [], 'params': {}},
    'concept_325': {'name': 'Rational Expressions', 'id': 'concept_325', 'module': [], 'params': {}},
    'concept_326': {'name': 'Functions and Function Notation', 'id': 'concept_326', 'module': [], 'params': {}},
    'concept_327': {'name': 'Rates of Change and Behavior of Graphs', 'id': 'concept_327', 'module': [], 'params': {}},
    'concept_328': {'name': 'Composition of Functions', 'id': 'concept_328', 'module': [], 'params': {}},
    'concept_329': {'name': 'Transformation of Functions', 'id': 'concept_329', 'module': [], 'params': {}},
    'concept_330': {'name': 'Absolute Value Functions', 'id': 'concept_330', 'module': [], 'params': {}},
    'concept_331': {'name': 'Inverse Functions', 'id': 'concept_331', 'module': [], 'params': {}},
    'concept_332': {'name': 'Complex Numbers', 'id': 'concept_332', 'module': [], 'params': {}},
    'concept_333': {'name': 'Quadratic Functions', 'id': 'concept_333', 'module': [], 'params': {}},
    'concept_334': {'name': 'Power Functions and Polynomial Functions', 'id': 'concept_334', 'module': [], 'params': {}},
    'concept_335': {'name': 'Graphs of Polynomial Functions', 'id': 'concept_335', 'module': [], 'params': {}},
    'concept_336': {'name': 'Dividing Polynomials', 'id': 'concept_336', 'module': [], 'params': {}},
    'concept_337': {'name': 'Zeros of Polynomial Functions', 'id': 'concept_337', 'module': [], 'params': {}},
    'concept_338': {'name': 'Rational Functions', 'id': 'concept_338', 'module': [], 'params': {}},
    'concept_339': {'name': 'Inverses and Radical Functions', 'id': 'concept_339', 'module': [], 'params': {}},
    'concept_340': {'name': 'Modeling Using Variation', 'id': 'concept_340', 'module': [], 'params': {}},
    'concept_341': {'name': 'Exponential Functions', 'id': 'concept_341', 'module': [], 'params': {}},
    'concept_342': {'name': 'Graph of Exponential Functions', 'id': 'concept_342', 'module': [], 'params': {}},
    'concept_343': {'name': 'Logarithmic Functions', 'id': 'concept_343', 'module': [], 'params': {}},
    'concept_344': {'name': 'Graph of Logarithmic Functions', 'id': 'concept_344', 'module': [], 'params': {}},
    'concept_345': {'name': 'Logarithms Properties', 'id': 'concept_345', 'module': [], 'params': {}},
    'concept_346': {'name': 'Exponential and Logarithmic Equations', 'id': 'concept_346', 'module': [], 'params': {}},
    'concept_347': {'name': 'Exponential and Logarithmic Models', 'id': 'concept_347', 'module': [], 'params': {}},
    'concept_348': {'name': 'Angles', 'id': 'concept_348', 'module': [], 'params': {}},
    'concept_349': {'name': 'Unit Circle: Sine and Cosine Functions', 'id': 'concept_349', 'module': [], 'params': {}},
    'concept_350': {'name': 'The Other Trigonometric Functions', 'id': 'concept_350', 'module': [], 'params': {}},
    'concept_351': {'name': 'Right Triangle Trigonometry', 'id': 'concept_351', 'module': [], 'params': {}},
    'concept_353': {'name': 'Real Numbers: Algebra Essentials', 'id': 'concept_353', 'module': [], 'params': {}},
}

const edges = {
    'edge-concept_2-concept_1': {'source': 'concept_2', 'target': 'concept_1'},
'edge-concept_4-concept_3': {'source': 'concept_4', 'target': 'concept_3'},
'edge-concept_7-concept_6': {'source': 'concept_7', 'target': 'concept_6'},
'edge-concept_10-concept_9': {'source': 'concept_10', 'target': 'concept_9'},
'edge-concept_10-concept_11': {'source': 'concept_10', 'target': 'concept_11'},
'edge-concept_19-concept_18': {'source': 'concept_19', 'target': 'concept_18'},
'edge-concept_21-concept_20': {'source': 'concept_21', 'target': 'concept_20'},
'edge-concept_23-concept_22': {'source': 'concept_23', 'target': 'concept_22'},
'edge-concept_25-concept_24': {'source': 'concept_25', 'target': 'concept_24'},
'edge-concept_28-concept_27': {'source': 'concept_28', 'target': 'concept_27'},
'edge-concept_35-concept_34': {'source': 'concept_35', 'target': 'concept_34'},
'edge-concept_25-concept_34': {'source': 'concept_25', 'target': 'concept_34'},
'edge-concept_33-concept_32': {'source': 'concept_33', 'target': 'concept_32'},
'edge-concept_39-concept_36': {'source': 'concept_39', 'target': 'concept_36'},
'edge-concept_38-concept_36': {'source': 'concept_38', 'target': 'concept_36'},
'edge-concept_37-concept_36': {'source': 'concept_37', 'target': 'concept_36'},
'edge-concept_41-concept_40': {'source': 'concept_41', 'target': 'concept_40'},
'edge-concept_43-concept_42': {'source': 'concept_43', 'target': 'concept_42'},
'edge-concept_48-concept_47': {'source': 'concept_48', 'target': 'concept_47'},
'edge-concept_50-concept_49': {'source': 'concept_50', 'target': 'concept_49'},
'edge-concept_53-concept_52': {'source': 'concept_53', 'target': 'concept_52'},
'edge-concept_58-concept_57': {'source': 'concept_58', 'target': 'concept_57'},
'edge-concept_59-concept_57': {'source': 'concept_59', 'target': 'concept_57'},
'edge-concept_62-concept_61': {'source': 'concept_62', 'target': 'concept_61'},
'edge-concept_64-concept_63': {'source': 'concept_64', 'target': 'concept_63'},
'edge-concept_66-concept_65': {'source': 'concept_66', 'target': 'concept_65'},
'edge-concept_67-concept_65': {'source': 'concept_67', 'target': 'concept_65'},
'edge-concept_69-concept_68': {'source': 'concept_69', 'target': 'concept_68'},
'edge-concept_72-concept_71': {'source': 'concept_72', 'target': 'concept_71'},
'edge-concept_80-concept_79': {'source': 'concept_80', 'target': 'concept_79'},
'edge-concept_81-concept_79': {'source': 'concept_81', 'target': 'concept_79'},
'edge-concept_84-concept_83': {'source': 'concept_84', 'target': 'concept_83'},
'edge-concept_84-concept_85': {'source': 'concept_84', 'target': 'concept_85'},
'edge-concept_90-concept_89': {'source': 'concept_90', 'target': 'concept_89'},
'edge-concept_92-concept_91': {'source': 'concept_92', 'target': 'concept_91'},
'edge-concept_94-concept_93': {'source': 'concept_94', 'target': 'concept_93'},
'edge-concept_95-concept_93': {'source': 'concept_95', 'target': 'concept_93'},
'edge-concept_97-concept_96': {'source': 'concept_97', 'target': 'concept_96'},
'edge-concept_98-concept_96': {'source': 'concept_98', 'target': 'concept_96'},
'edge-concept_99-concept_96': {'source': 'concept_99', 'target': 'concept_96'},
'edge-concept_103-concept_102': {'source': 'concept_103', 'target': 'concept_102'},
'edge-concept_106-concept_105': {'source': 'concept_106', 'target': 'concept_105'},
'edge-concept_108-concept_107': {'source': 'concept_108', 'target': 'concept_107'},
'edge-concept_109-concept_107': {'source': 'concept_109', 'target': 'concept_107'},
'edge-concept_113-concept_112': {'source': 'concept_113', 'target': 'concept_112'},
'edge-concept_114-concept_112': {'source': 'concept_114', 'target': 'concept_112'},
'edge-concept_115-concept_112': {'source': 'concept_115', 'target': 'concept_112'},
'edge-concept_116-concept_112': {'source': 'concept_116', 'target': 'concept_112'},
'edge-concept_117-concept_112': {'source': 'concept_117', 'target': 'concept_112'},
'edge-concept_120-concept_119': {'source': 'concept_120', 'target': 'concept_119'},
'edge-concept_122-concept_121': {'source': 'concept_122', 'target': 'concept_121'},
'edge-concept_124-concept_123': {'source': 'concept_124', 'target': 'concept_123'},
'edge-concept_130-concept_129': {'source': 'concept_130', 'target': 'concept_129'},
'edge-concept_131-concept_129': {'source': 'concept_131', 'target': 'concept_129'},
'edge-concept_133-concept_132': {'source': 'concept_133', 'target': 'concept_132'},
'edge-concept_134-concept_132': {'source': 'concept_134', 'target': 'concept_132'},
'edge-concept_137-concept_136': {'source': 'concept_137', 'target': 'concept_136'},
'edge-concept_138-concept_136': {'source': 'concept_138', 'target': 'concept_136'},
'edge-concept_140-concept_139': {'source': 'concept_140', 'target': 'concept_139'},
'edge-concept_142-concept_141': {'source': 'concept_142', 'target': 'concept_141'},
'edge-concept_143-concept_141': {'source': 'concept_143', 'target': 'concept_141'},
'edge-concept_145-concept_144': {'source': 'concept_145', 'target': 'concept_144'},
'edge-concept_147-concept_146': {'source': 'concept_147', 'target': 'concept_146'},
'edge-concept_149-concept_148': {'source': 'concept_149', 'target': 'concept_148'},
'edge-concept_150-concept_148': {'source': 'concept_150', 'target': 'concept_148'},
'edge-concept_152-concept_151': {'source': 'concept_152', 'target': 'concept_151'},
'edge-concept_153-concept_151': {'source': 'concept_153', 'target': 'concept_151'},
'edge-concept_157-concept_156': {'source': 'concept_157', 'target': 'concept_156'},
'edge-concept_159-concept_158': {'source': 'concept_159', 'target': 'concept_158'},
'edge-concept_162-concept_161': {'source': 'concept_162', 'target': 'concept_161'},
'edge-concept_167-concept_166': {'source': 'concept_167', 'target': 'concept_166'},
'edge-concept_169-concept_168': {'source': 'concept_169', 'target': 'concept_168'},
'edge-concept_170-concept_168': {'source': 'concept_170', 'target': 'concept_168'},
'edge-concept_172-concept_171': {'source': 'concept_172', 'target': 'concept_171'},
'edge-concept_173-concept_171': {'source': 'concept_173', 'target': 'concept_171'},
'edge-concept_175-concept_174': {'source': 'concept_175', 'target': 'concept_174'},
'edge-concept_176-concept_174': {'source': 'concept_176', 'target': 'concept_174'},
'edge-concept_178-concept_177': {'source': 'concept_178', 'target': 'concept_177'},
'edge-concept_180-concept_179': {'source': 'concept_180', 'target': 'concept_179'},
'edge-concept_185-concept_184': {'source': 'concept_185', 'target': 'concept_184'},
'edge-concept_188-concept_187': {'source': 'concept_188', 'target': 'concept_187'},
'edge-concept_193-concept_192': {'source': 'concept_193', 'target': 'concept_192'},
'edge-concept_195-concept_194': {'source': 'concept_195', 'target': 'concept_194'},
'edge-concept_197-concept_196': {'source': 'concept_197', 'target': 'concept_196'},
'edge-concept_199-concept_198': {'source': 'concept_199', 'target': 'concept_198'},
'edge-concept_200-concept_198': {'source': 'concept_200', 'target': 'concept_198'},
'edge-concept_203-concept_202': {'source': 'concept_203', 'target': 'concept_202'},
'edge-concept_205-concept_204': {'source': 'concept_205', 'target': 'concept_204'},
'edge-concept_206-concept_204': {'source': 'concept_206', 'target': 'concept_204'},
'edge-concept_208-concept_207': {'source': 'concept_208', 'target': 'concept_207'},
'edge-concept_209-concept_207': {'source': 'concept_209', 'target': 'concept_207'},
'edge-concept_211-concept_210': {'source': 'concept_211', 'target': 'concept_210'},
'edge-concept_212-concept_210': {'source': 'concept_212', 'target': 'concept_210'},
'edge-concept_214-concept_213': {'source': 'concept_214', 'target': 'concept_213'},
'edge-concept_215-concept_213': {'source': 'concept_215', 'target': 'concept_213'},
'edge-concept_218-concept_217': {'source': 'concept_218', 'target': 'concept_217'},
'edge-concept_218-concept_219': {'source': 'concept_218', 'target': 'concept_219'},
'edge-concept_222-concept_221': {'source': 'concept_222', 'target': 'concept_221'},
'edge-concept_224-concept_223': {'source': 'concept_224', 'target': 'concept_223'},
'edge-concept_226-concept_225': {'source': 'concept_226', 'target': 'concept_225'},
'edge-concept_227-concept_225': {'source': 'concept_227', 'target': 'concept_225'},
'edge-concept_229-concept_228': {'source': 'concept_229', 'target': 'concept_228'},
'edge-concept_230-concept_233': {'source': 'concept_230', 'target': 'concept_233'},
'edge-concept_231-concept_233': {'source': 'concept_231', 'target': 'concept_233'},
'edge-concept_232-concept_233': {'source': 'concept_232', 'target': 'concept_233'},
'edge-concept_230-concept_234': {'source': 'concept_230', 'target': 'concept_234'},
'edge-concept_231-concept_234': {'source': 'concept_231', 'target': 'concept_234'},
'edge-concept_232-concept_234': {'source': 'concept_232', 'target': 'concept_234'},
'edge-concept_238-concept_237': {'source': 'concept_238', 'target': 'concept_237'},
'edge-concept_248-concept_247': {'source': 'concept_248', 'target': 'concept_247'},
'edge-concept_249-concept_247': {'source': 'concept_249', 'target': 'concept_247'},
'edge-concept_253-concept_252': {'source': 'concept_253', 'target': 'concept_252'},
'edge-concept_254-concept_252': {'source': 'concept_254', 'target': 'concept_252'},
'edge-concept_259-concept_258': {'source': 'concept_259', 'target': 'concept_258'},
'edge-concept_260-concept_258': {'source': 'concept_260', 'target': 'concept_258'},
'edge-concept_267-concept_266': {'source': 'concept_267', 'target': 'concept_266'},
'edge-concept_268-concept_266': {'source': 'concept_268', 'target': 'concept_266'},
'edge-concept_275-concept_274': {'source': 'concept_275', 'target': 'concept_274'},
'edge-concept_281-concept_280': {'source': 'concept_281', 'target': 'concept_280'},
'edge-concept_283-concept_282': {'source': 'concept_283', 'target': 'concept_282'},
'edge-concept_284-concept_282': {'source': 'concept_284', 'target': 'concept_282'},
'edge-concept_287-concept_286': {'source': 'concept_287', 'target': 'concept_286'},
'edge-concept_288-concept_286': {'source': 'concept_288', 'target': 'concept_286'},
'edge-concept_290-concept_289': {'source': 'concept_290', 'target': 'concept_289'},
'edge-concept_291-concept_289': {'source': 'concept_291', 'target': 'concept_289'},
'edge-concept_294-concept_293': {'source': 'concept_294', 'target': 'concept_293'},
'edge-concept_295-concept_293': {'source': 'concept_295', 'target': 'concept_293'},
'edge-concept_297-concept_296': {'source': 'concept_297', 'target': 'concept_296'},
'edge-concept_298-concept_296': {'source': 'concept_298', 'target': 'concept_296'},
'edge-concept_301-concept_300': {'source': 'concept_301', 'target': 'concept_300'},
'edge-concept_305-concept_304': {'source': 'concept_305', 'target': 'concept_304'},
'edge-concept_307-concept_306': {'source': 'concept_307', 'target': 'concept_306'},
'edge-concept_309-concept_308': {'source': 'concept_309', 'target': 'concept_308'},
'edge-concept_311-concept_310': {'source': 'concept_311', 'target': 'concept_310'},
'edge-concept_313-concept_312': {'source': 'concept_313', 'target': 'concept_312'},
'edge-concept_319-concept_318': {'source': 'concept_319', 'target': 'concept_318'},
'edge-concept_321-concept_320': {'source': 'concept_321', 'target': 'concept_320'},
'edge-concept_323-concept_322': {'source': 'concept_323', 'target': 'concept_322'},
'edge-concept_3-concept_5': {'source': 'concept_3', 'target': 'concept_5'},
'edge-concept_5-concept_8': {'source': 'concept_5', 'target': 'concept_8'},
'edge-concept_5-concept_6': {'source': 'concept_5', 'target': 'concept_6'},
'edge-concept_6-concept_8': {'source': 'concept_6', 'target': 'concept_8'},
'edge-concept_10-concept_12': {'source': 'concept_10', 'target': 'concept_12'},
'edge-concept_10-concept_13': {'source': 'concept_10', 'target': 'concept_13'},
'edge-concept_10-concept_14': {'source': 'concept_10', 'target': 'concept_14'},
'edge-concept_18-Radicals and Rational Exponents': {'source': 'concept_18', 'target': 'Radicals and Rational Exponents'},
'edge-concept_20-Radicals and Rational Exponents': {'source': 'concept_20', 'target': 'Radicals and Rational Exponents'},
'edge-concept_22-Radicals and Rational Exponents': {'source': 'concept_22', 'target': 'Radicals and Rational Exponents'},
'edge-concept_27-Radicals and Rational Exponents': {'source': 'concept_27', 'target': 'Radicals and Rational Exponents'},
'edge-concept_24-Radicals and Rational Exponents': {'source': 'concept_24', 'target': 'Radicals and Rational Exponents'},
'edge-concept_26-Radicals and Rational Exponents': {'source': 'concept_26', 'target': 'Radicals and Rational Exponents'},
'edge-Exponents and Scientific Notation-Radicals and Rational Exponents': {'source': 'Exponents and Scientific Notation', 'target': 'Radicals and Rational Exponents'},
'edge-concept_1-concept_3': {'source': 'concept_1', 'target': 'concept_3'},
'edge-concept_16-concept_6': {'source': 'concept_16', 'target': 'concept_6'},
'edge-concept_9-concept_16': {'source': 'concept_9', 'target': 'concept_16'},
'edge-concept_11-concept_16': {'source': 'concept_11', 'target': 'concept_16'},
'edge-concept_12-concept_16': {'source': 'concept_12', 'target': 'concept_16'},
'edge-concept_13-concept_16': {'source': 'concept_13', 'target': 'concept_16'},
'edge-concept_14-concept_16': {'source': 'concept_14', 'target': 'concept_16'},
'edge-concept_9-concept_15': {'source': 'concept_9', 'target': 'concept_15'},
'edge-concept_11-concept_15': {'source': 'concept_11', 'target': 'concept_15'},
'edge-concept_12-concept_15': {'source': 'concept_12', 'target': 'concept_15'},
'edge-concept_15-concept_16': {'source': 'concept_15', 'target': 'concept_16'},
'edge-concept_29-Polynomials': {'source': 'concept_29', 'target': 'Polynomials'},
'edge-concept_30-Polynomials': {'source': 'concept_30', 'target': 'Polynomials'},
'edge-concept_31-Polynomials': {'source': 'concept_31', 'target': 'Polynomials'},
'edge-concept_32-Polynomials': {'source': 'concept_32', 'target': 'Polynomials'},
'edge-concept_34-Polynomials': {'source': 'concept_34', 'target': 'Polynomials'},
'edge-concept_10-concept_28': {'source': 'concept_10', 'target': 'concept_28'},
'edge-concept_10-concept_17': {'source': 'concept_10', 'target': 'concept_17'},
'edge-concept_19-concept_20': {'source': 'concept_19', 'target': 'concept_20'},
'edge-concept_19-concept_22': {'source': 'concept_19', 'target': 'concept_22'},
'edge-concept_19-concept_24': {'source': 'concept_19', 'target': 'concept_24'},
'edge-concept_36-Factoring Polynomials': {'source': 'concept_36', 'target': 'Factoring Polynomials'},
'edge-concept_40-Factoring Polynomials': {'source': 'concept_40', 'target': 'Factoring Polynomials'},
'edge-concept_42-Factoring Polynomials': {'source': 'concept_42', 'target': 'Factoring Polynomials'},
'edge-concept_44-Factoring Polynomials': {'source': 'concept_44', 'target': 'Factoring Polynomials'},
'edge-concept_45-Factoring Polynomials': {'source': 'concept_45', 'target': 'Factoring Polynomials'},
'edge-concept_46-Factoring Polynomials': {'source': 'concept_46', 'target': 'Factoring Polynomials'},
'edge-concept_47-Factoring Polynomials': {'source': 'concept_47', 'target': 'Factoring Polynomials'},
'edge-concept_9-concept_17': {'source': 'concept_9', 'target': 'concept_17'},
'edge-concept_12-concept_17': {'source': 'concept_12', 'target': 'concept_17'},
'edge-concept_14-concept_17': {'source': 'concept_14', 'target': 'concept_17'},
'edge-concept_13-concept_17': {'source': 'concept_13', 'target': 'concept_17'},
'edge-concept_17-concept_220': {'source': 'concept_17', 'target': 'concept_220'},
'edge-Radicals and Rational Exponents-concept_220': {'source': 'Radicals and Rational Exponents', 'target': 'concept_220'},
'edge-Polynomials-concept_154': {'source': 'Polynomials', 'target': 'concept_154'},
'edge-concept_25-concept_30': {'source': 'concept_25', 'target': 'concept_30'},
'edge-concept_25-concept_31': {'source': 'concept_25', 'target': 'concept_31'},
'edge-concept_30-concept_34': {'source': 'concept_30', 'target': 'concept_34'},
'edge-concept_31-concept_34': {'source': 'concept_31', 'target': 'concept_34'},
'edge-Radicals and Rational Exponents-concept_327': {'source': 'Radicals and Rational Exponents', 'target': 'concept_327'},
'edge-Polynomials-concept_332': {'source': 'Polynomials', 'target': 'concept_332'},
'edge-Factoring Polynomials-concept_333': {'source': 'Factoring Polynomials', 'target': 'concept_333'},
'edge-Polynomials-concept_334': {'source': 'Polynomials', 'target': 'concept_334'},
'edge-Factoring Polynomials-concept_335': {'source': 'Factoring Polynomials', 'target': 'concept_335'},
'edge-concept_329-concept_335': {'source': 'concept_329', 'target': 'concept_335'},
'edge-Factoring Polynomials-concept_336': {'source': 'Factoring Polynomials', 'target': 'concept_336'},
'edge-concept_325-concept_336': {'source': 'concept_325', 'target': 'concept_336'},
'edge-Factoring Polynomials-concept_337': {'source': 'Factoring Polynomials', 'target': 'concept_337'},
'edge-concept_325-concept_338': {'source': 'concept_325', 'target': 'concept_338'},
'edge-concept_331-concept_339': {'source': 'concept_331', 'target': 'concept_339'},
'edge-Exponents and Scientific Notation-concept_341': {'source': 'Exponents and Scientific Notation', 'target': 'concept_341'},
'edge-concept_97-concept_342': {'source': 'concept_97', 'target': 'concept_342'},
'edge-concept_327-concept_342': {'source': 'concept_327', 'target': 'concept_342'},
'edge-Exponents and Scientific Notation-concept_343': {'source': 'Exponents and Scientific Notation', 'target': 'concept_343'},
'edge-Radicals and Rational Exponents-concept_343': {'source': 'Radicals and Rational Exponents', 'target': 'concept_343'},
'edge-concept_97-concept_344': {'source': 'concept_97', 'target': 'concept_344'},
'edge-concept_327-concept_344': {'source': 'concept_327', 'target': 'concept_344'},
'edge-Exponents and Scientific Notation-concept_345': {'source': 'Exponents and Scientific Notation', 'target': 'concept_345'},
'edge-Radicals and Rational Exponents-concept_345': {'source': 'Radicals and Rational Exponents', 'target': 'concept_345'},
'edge-Exponents and Scientific Notation-concept_346': {'source': 'Exponents and Scientific Notation', 'target': 'concept_346'},
'edge-Radicals and Rational Exponents-concept_346': {'source': 'Radicals and Rational Exponents', 'target': 'concept_346'},
'edge-Exponents and Scientific Notation-concept_347': {'source': 'Exponents and Scientific Notation', 'target': 'concept_347'},
'edge-Radicals and Rational Exponents-concept_347': {'source': 'Radicals and Rational Exponents', 'target': 'concept_347'},
'edge-concept_329-concept_332': {'source': 'concept_329', 'target': 'concept_332'},
'edge-concept_329-concept_333': {'source': 'concept_329', 'target': 'concept_333'},
'edge-concept_329-concept_334': {'source': 'concept_329', 'target': 'concept_334'},
'edge-concept_329-concept_336': {'source': 'concept_329', 'target': 'concept_336'},
'edge-concept_329-concept_337': {'source': 'concept_329', 'target': 'concept_337'},
'edge-concept_329-concept_338': {'source': 'concept_329', 'target': 'concept_338'},
'edge-concept_329-concept_339': {'source': 'concept_329', 'target': 'concept_339'},
'edge-concept_329-concept_340': {'source': 'concept_329', 'target': 'concept_340'},
'edge-concept_329-concept_341': {'source': 'concept_329', 'target': 'concept_341'},
'edge-concept_329-concept_342': {'source': 'concept_329', 'target': 'concept_342'},
'edge-concept_329-concept_343': {'source': 'concept_329', 'target': 'concept_343'},
'edge-concept_329-concept_344': {'source': 'concept_329', 'target': 'concept_344'},
'edge-concept_329-concept_345': {'source': 'concept_329', 'target': 'concept_345'},
'edge-concept_329-concept_346': {'source': 'concept_329', 'target': 'concept_346'},
'edge-concept_329-concept_347': {'source': 'concept_329', 'target': 'concept_347'},
'edge-concept_329-concept_348': {'source': 'concept_329', 'target': 'concept_348'},
'edge-concept_329-concept_349': {'source': 'concept_329', 'target': 'concept_349'},
'edge-concept_329-concept_350': {'source': 'concept_329', 'target': 'concept_350'},
'edge-concept_329-concept_351': {'source': 'concept_329', 'target': 'concept_351'},
'edge-concept_1-concept_352': {'source': 'concept_1', 'target': 'concept_352'},
'edge-concept_1-concept_353': {'source': 'concept_1', 'target': 'concept_353'},
'edge-concept_1-concept_354': {'source': 'concept_1', 'target': 'concept_354'},
'edge-concept_1-concept_355': {'source': 'concept_1', 'target': 'concept_355'}
}
const dagUtil = new DomainDagUtilities(nodes, edges)


const defaultSettings = {
    nodeColor: "#00629B",
    focusColor: "#ffdd00",
    moduleColor: "#FC8900",
    edgeColor: "",
    textColor: "#00000",
    nodeSize: 30,
    selectable: true,
    showModules: true
}

const modalOpen = ref(false)
const isMenuOpen = ref(false)

</script>

<template>
    <div class="domain-editor">
        <div class="left-section" :data-state="isMenuOpen ? 'min' : 'max'">
            <div class="menu-collapse" @click="isMenuOpen = !isMenuOpen">
                <img src="/static/assets/icon-chevron.png"/>
            </div>
            <div class="graph roboto-bold">
                <DomainDag 
                    :nodes="dagUtil.nodes.value" 
                    :edges="dagUtil.edges.value" 
                    :focus-node="dagUtil.focusNode.value"
                    :selectedNodes="dagUtil.selectedNodes.value" 
                    :selectedModule="dagUtil.selectedModule.value"
                    :defaultSettings="defaultSettings"
                    :selected-edges="dagUtil.selectedEdges.value"
                    @update-nodes="dagUtil.updateNodes"
                    @update-selected-nodes="dagUtil.updateSelectedNodes" 
                    @update-focus-nodes="dagUtil.updateFocusNodes"
                    @update-selected-edges="dagUtil.updateSelectedEdges" 
                    @delete-concepts="dagUtil.deleteSelectedNodes"
                    @join-concepts="dagUtil.addSelectedEdges" 
                    @junction-delete="dagUtil.deleteSelectedEdges"
                    @add-concept="modalOpen = true" 
                    @undo="dagUtil.undoChange" 
                    @redo="dagUtil.redoChange" 
                    @module-concept-add="dagUtil.addSelectedNodesToModule"
                    @module-concept-delete="dagUtil.RemoveSelectedNodesFromModule"
                    @transitive-reduction="dagUtil.transitiveReduction"
                    />
            </div>
            <NewConceptModal @add-node="dagUtil.addNode" @update-open="val => modalOpen = val" :modal-open="modalOpen" />
        </div>
        <div class="right-section" :data-state="isMenuOpen ? 'max' : 'min'">
            <ModuleMenu 
                :concepts="dagUtil.nodes.value" 
                :selected-concepts="dagUtil.selectedNodes"
                @update-selected-module="dagUtil.updateSelectedModule" 
                @update-selected-nodes="dagUtil.updateSelectedNodes"
                @save-domain="dagUtil.saveDomain" 
                @add-file="dagUtil.uploadDomain"
                />
        </div>
        <div v-if="dagUtil.saving.value" class="save-overlay">
        </div>
    </div>
</template>

<style scoped>

.menu-collapse {
    position: absolute;
    top: calc(50% - 2rem);
    right:-1rem;
    width: 2rem;
    height: 4rem;
    z-index: 999;
    background-color: var(--core-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
}

.menu-collapse > img {
    height: 100%;
}
.left-section[data-state='max'] > .menu-collapse > img {
    transform: rotate(270deg);
    transition: transform .5s ease-out;
}

.left-section[data-state='min'] > .menu-collapse > img {
    transform: rotate(90deg);
    transition: transform .5s ease-out;
}
.save-overlay {
    position: relative;
    top: 0;
    left: 0;
    background-color: rgba(128, 128, 128, 0.508);
    width: 100vw;
    height: 100vh;
    z-index: 999;
}

.domain-editor {
    display: flex;
    flex-direction: row;
    height: 100% !important;
    width: 100%;
    min-height: 100% !important;
}

.left-section[data-state='max'] {
    animation: slide-out 1s ease-out;
    width: 100%;
}
.left-section[data-state='min'] {
    width: 75%;
    animation: slide-in 1s ease-out;
}
.left-section {
    position: relative;
}
@keyframes slide-out {
    from {
        width: 75%;
    }
    to {
        width: 100%;
    }
}

@keyframes slide-in {
    from {
        width: 100%;
    }
    to {
        width: 75%;
    }
}

@keyframes slide-out-menu {
    from {
        width: 0%;
        visibility: collapse;
    }
    to {
        width: 25%;
        visibility: visible;
    }
}

@keyframes slide-in-menu {
    from {
        width: 25%;
        visibility: visible;
    }
    to {
        width: 0%;
        visibility: collapse;
    }
}
.right-section {
    box-shadow: 1px 1px 2px 0px rgb(169, 169, 169);
    /* width: 25%; */
    display: flex;
    flex-direction: column;
    align-items: center;
    height: calc(100% - 1rem);
    overflow: hidden;
    background-color: var(--bg-color);
    border-radius: 8px;
}

.right-section[data-state='min'] {
    width: 0%;
    margin-left: 0px;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    visibility: collapse;
    animation: slide-in-menu 1s ease-out;
}

.right-section[data-state='max'] {
    margin-left: 5px;
    padding: .5rem;
    width: 25%;
    animation: slide-out-menu 1s ease-out;
}

.bottom-menu {
    margin: .5rem;
}

.graph {
    height: 100%;
    position: relative;
    top: 0;
    left: 0;

}
</style>
