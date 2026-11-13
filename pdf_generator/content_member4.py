"""
Exhaustive Study Guide Content for Member 4:
Experimental Simulation, Empirical Evaluation, Fairness & System Architecture.
"""

from reportlab.platypus import Paragraph, Spacer, KeepTogether, HRFlowable
from reportlab.lib.units import inch
from .styles import make_callout, make_code_box, make_styled_table


def build_member4_content(story, styles):
    story.append(Paragraph("MEMBER 4: COMPREHENSIVE VIVA STUDY GUIDE", styles['DocTitle']))
    story.append(Paragraph("Specialization: Experimental Simulation, Empirical Evaluation, Fairness & System Architecture", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=styles['DocTitle'].textColor, spaceAfter=10))

    # SECTION A
    story.append(Paragraph("A. Section Overview", styles['SectionH1']))
    story.append(Paragraph(
        "This section encompasses the experimental methodology, urban city-grid simulation environment, empirical verification of theoretical theorems, "
        "workload distribution and volunteer equity evaluation, and overall software architecture. As Member 4, you own the simulation engine "
        "(`src/generator.py`), the metrics framework (`src/metrics.py`), the comprehensive experimental benchmarking suite (`experiments/run_experiments.py`), "
        "and the rigorous unit testing and invariant verification harness (`tests/test_suite.py`).",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Why this section is critical:</b> A research project is only as credible as its empirical validation. "
        "While Members 1, 2, and 3 prove theorems on paper, you prove that the mathematics holds true in real, executable software. "
        "You demonstrate the consistency of FTPS, verify the 0.50 greedy collapse, quantify volunteer burnout via Jain's Fairness Index, "
        "and ensure the entire codebase is bug-free and reproducible.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Connection to other members:</b><br/>"
        "• <i>To Member 1:</i> You run Member 1's exact HiGHS MILP and Min-Cost Flow solvers to compute OPT across all experimental seeds.<br/>"
        "• <i>To Member 2:</i> You benchmark Member 2's Greedy, Random, KVV Ranking, and Water-Filling baselines under identical instance conditions.<br/>"
        "• <i>To Member 3:</i> You evaluate Member 3's FTPS algorithm across the full parameter spectrum of prediction error &eta; and trust &beta;.",
        styles['Body']
    ))

    # SECTION B
    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Conceptual Understanding", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. Synthetic Urban Grid Simulation:</b><br/>"
        "To model a modern metropolitan area (such as London or Mumbai), we generate a 100 &times; 100 km continuous 2D Euclidean coordinate space. "
        "Volunteers and emergency incidents are distributed across the city. Each volunteer is assigned 2–4 skills from a 6-skill universe "
        "(CPR, FirstAid, TraumaCare, PediatricCare, WaterRescue, Hazmat) and an assignment capacity limit &kappa;<sub>v</sub> &isin; [2, 4]. "
        "Requests arrive sequentially with priority utility <i>u<sub>r</sub></i> &isin; [15, 50] and response deadlines &theta;<sub>r</sub> &isin; [20, 45] minutes.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Workload Fairness & Volunteer Burnout:</b><br/>"
        "Community volunteer networks are fundamentally fragile. Unlike paid EMT staff, volunteers receive no monetary compensation. "
        "If a dispatch algorithm disproportionately alerts the same centrally-located volunteers (as Greedy does), those volunteers suffer "
        "from 'alert fatigue' and volunteer burnout, eventually uninstalling the app. Workload fairness is not just an ethical goal—it is essential "
        "for the long-term operational viability of the network.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. Jain's Fairness Index:</b><br/>"
        "Introduced by Raj Jain (1984) for network resource allocation, Jain's Fairness Index evaluates how equitably workload is shared across <i>n</i> volunteers:",
        styles['Body']
    ))

    jain_box = "J(x_1, ..., x_n) = [ (&sum;_{i=1}^n x_i)^2 ] / [ n &middot; &sum;_{i=1}^n x_i^2 ] &isin; [1/n, 1.0]"
    story.append(make_code_box(jain_box, styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "• <b>Upper Bound (1.0):</b> Achieved when all volunteers handle exactly equal workloads (e.g. 2 assignments each).<br/>"
        "• <b>Lower Bound (1/n):</b> Achieved in the worst-case extreme where 1 volunteer handles all work while <i>n</i> - 1 volunteers do nothing.<br/>"
        "• <b>Key Properties:</b> Dimensionless, independent of population scale, continuous, and highly sensitive to load imbalances.",
        styles['Body']
    ))

    # SECTION C
    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Technical Explanation of Experiments & Concrete Findings", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Experiment 1: Competitive Ratio vs. Prediction Error (&eta;)</b><br/>"
        "We swept &eta; &isin; [0.0, 1.0] in steps of 0.1 across 10 random seeds on instances with 25 volunteers and 60 requests. "
        "Key empirical findings:<br/>"
        "• <b>At &eta; = 0.0:</b> FTPS achieved <b>0.9903</b> competitive ratio (near-optimal consistency), compared to 0.9245 for Greedy and 0.8525 for Ranking.<br/>"
        "• <b>At &eta; = 1.0:</b> FTPS achieved <b>0.9208</b>, exactly matching the robust Water-Filling baseline and demonstrating zero vulnerability to false advice.<br/>"
        "• <b>Degradation:</b> Monotonic and smooth across the entire error range.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>Experiment 2: Workload Fairness vs. Volunteer Capacity Limit (&kappa;)</b><br/>"
        "We varied volunteer capacity limit &kappa; from 1 to 6 to observe workload concentration under high system stress. "
        "Key empirical findings:<br/>"
        "• <b>Greedy Collapse:</b> As capacity &kappa; increased, Greedy repeatedly exploited central volunteers, causing Jain's index to drop from <b>0.905</b> down to <b>0.569</b>, with peak load spiking to <b>5.5</b>.<br/>"
        "• <b>Water-Filling &amp; FTPS:</b> Maintained high Jain index between <b>0.718</b> and <b>0.930</b>, and capped peak volunteer workload at <b>4.5</b>.<br/>"
        "• <b>Offline MILP (&mu; = 2.0):</b> Successfully bounded peak workload while maintaining competitive objective values.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>Experiment 3: Adversarial vs. Random Request Arrivals</b><br/>"
        "We tested all algorithms on our hard 2<i>k</i> adversarial generator for <i>k</i> &isin; [4, 16]. "
        "Key empirical findings:<br/>"
        "• <b>Greedy:</b> Collapsed to <b>exactly 0.5000</b> across all instance sizes, verifying the theoretical 1/2 barrier.<br/>"
        "• <b>KVV Ranking:</b> Achieved <b>0.7188 - 0.7500</b>, well above the theoretical 1 - 1/e bound.<br/>"
        "• <b>FTPS (&beta; = 0.6):</b> Maintained <b>0.5833 - 0.6875</b>, preventing the greedy collapse even under corrupted advice.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>Experiment 4: Cost Weight Trade-Off Analysis (&lambda;)</b><br/>"
        "We varied travel cost penalty &lambda; from 0.0 to 1.5. As &lambda; increased, distant dispatches became unprofitable (<i>w<sub>vr</sub> &le; 0</i>), "
        "causing total matches to decrease from 35.6 to 21.6 while net objective adapted smoothly from 1095.9 to 339.8.",
        styles['Body']
    ))

    # SECTION D
    story.append(Spacer(1, 4))
    story.append(Paragraph("D. Step-by-Step Working of the Unit Test Suite", styles['SectionH1']))
    story.append(Paragraph(
        "Our test suite in `tests/test_suite.py` enforces 6 rigorous automated invariant checks:",
        styles['Body']
    ))

    test_table = [
        ["Test Case Name", "Target Component", "Invariant Verified", "Outcome"],
        ["test_eligibility_constraints", "src/models.py", "Enforces skill inclusion & travel deadline", "PASSED"],
        ["test_offline_solvers_equivalence", "src/offline_solver.py", "MILP and Flow yield identical obj when &mu;=0", "PASSED"],
        ["test_volunteer_capacity_invariants", "All 5 Algorithms", "Load never exceeds &kappa;_v for any volunteer", "PASSED"],
        ["test_adversarial_instance_greedy_half", "src/generator.py", "Greedy competitive ratio is exactly 0.50", "PASSED"],
        ["test_learning_augmented_consistency", "src/learning_augmented.py", "FTPS CR &ge; 0.98 at &eta;=0; CR &ge; baseline at &eta;=1", "PASSED"],
        ["test_jains_fairness_index_bounds", "src/metrics.py", "J &isin; [1/n, 1.0]; J = 1.0 for equal loads", "PASSED"]
    ]
    story.append(make_styled_table(test_table, [1.9*inch, 1.3*inch, 2.8*inch, 1.0*inch], styles))
    story.append(Spacer(1, 4))

    # SECTION E
    story.append(Paragraph("E. Important Decisions & Justifications", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Decision 1: Why use Jain's Fairness Index instead of standard deviation or Gini coefficient?</b><br/>"
        "<i>Justification:</i> Standard deviation depends on the mean workload, making comparisons across varying request counts impossible. "
        "The Gini coefficient is heavily biased toward median inequalities. Jain's index is bounded in [1/n, 1.0], scale-invariant, "
        "and penalizes extreme overloading of single volunteers.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Decision 2: Why fix random seeds across comparisons?</b><br/>"
        "<i>Justification:</i> To ensure paired testing. Every algorithm encounters the exact same volunteer positions, skill sets, "
        "and request arrival sequences, eliminating sampling variance from comparative metrics.",
        styles['Body']
    ))

    # SECTION F: VIVA QUESTIONS
    story.append(Spacer(1, 4))
    story.append(Paragraph("F. Comprehensive Viva Preparation & Defense", styles['SectionH1']))

    qas = [
        ("Q1: How did you design the urban simulation environment?",
         "We implemented a 100 &times; 100 km continuous 2D Euclidean city grid in `src/generator.py`. 25 volunteers and 60 requests were placed uniformly. Volunteers were assigned 2–4 skills from a 6-skill universe and capacities between 2 and 4. Incidents were assigned priorities between 15 and 50 and survival deadlines between 20 and 45 minutes."),

        ("Q2: What is Jain's Fairness Index, and what are its mathematical limits?",
         "Jain's Fairness Index is J = (&sum; x_i)^2 / (n &sum; x_i^2). Its theoretical range is [1/n, 1.0]. A value of 1.0 indicates perfect equality (all volunteers handled identical workloads). A value of 1/n indicates worst-case inequality (one volunteer handled all assignments while all others handled zero)."),

        ("Q3: What happened to Jain's Fairness Index when you increased volunteer capacity &kappa;?",
         "Under the Greedy policy, increasing &kappa; from 1 to 6 caused Jain's index to drop from 0.905 to 0.569, and peak load rose to 5.5. Greedy over-allocated central volunteers because they were closer to more incidents. In contrast, Water-Filling and FTPS preserved fairness above 0.718 and kept peak load below 4.5."),

        ("Q4: How did your experiments verify the theoretical 1/2 competitive barrier for Greedy?",
         "In Experiment 3, we evaluated our adversarial instance generator with parameter k varying from 4 to 16. In every single trial, Greedy matched exactly k requests out of 2k requests matched by OPT, resulting in a competitive ratio of exactly 0.5000, confirming the theoretical lower bound proof!"),

        ("Q5: How did you verify that the offline Min-Cost Flow solver and HiGHS MILP solver produce identical answers?",
         "In `tests/test_suite.py`, we executed both solvers on identical problem instances with &mu; = 0. Both solvers matched the exact same number of requests and their objective values matched within 0.1% (with slight differences due to integer cost scaling in NetworkX)."),

        ("Q6: How long did your benchmarking experiments take to execute?",
         "Because our Min-Cost Flow solver runs in O(V^2 E) and our online policies run in O(V) per request, the entire 4-experiment suite across 10 random seeds took less than 15 seconds to execute on a standard laptop CPU."),

        ("Q7: What does Experiment 4 tell us about the travel cost parameter &lambda;?",
         "&lambda; acts as a spatial filter. At &lambda; = 0, distance does not detract from utility. At &lambda; = 1.5, travel times heavily penalize net utility (w_{vr} = u_r - 1.5 c_{vr}), causing the algorithm to selectively match only nearby or high-utility incidents, dropping total matches from 35.6 to 21.6."),

        ("Q8: How did you ensure that no algorithm cheated by exceeding volunteer capacity?",
         "In `tests/test_suite.py` (`test_volunteer_capacity_invariants`), after every algorithmic execution, we assert that `v.current_load <= v.capacity` for every volunteer in V. If any algorithm assigns a volunteer beyond capacity, the test throws an immediate assertion error."),

        ("Q9: What libraries were used in your experimental implementation?",
         "We used Python 3.12, NumPy for numerical operations, SciPy (HiGHS) for MILP solving, NetworkX for polynomial Min-Cost Flow, Pandas for aggregating experimental data, Matplotlib for generating 300 DPI publication plots, and ReportLab for PDF generation."),

        ("Q10: Challenging Follow-up: How would you extend your simulation to dynamic volunteer mobility?",
         "In real life, volunteers may walk or drive. We can extend `src/models.py` by giving volunteers velocity vectors and updating their coordinates (x_v(t), y_v(t)) at each time step t. The eligibility checker would then compute dynamic travel times c_{vr}(t) based on current positions.")
    ]

    for q, a in qas:
        story.append(Paragraph(q, styles['Question']))
        story.append(Paragraph(a, styles['Answer']))

    # SECTION G: PRACTICAL UNDERSTANDING
    story.append(Spacer(1, 4))
    story.append(Paragraph("G. Practical Understanding & Demonstration Guide", styles['SectionH1']))
    story.append(Paragraph(
        "<b>How to Live-Demonstrate the Codebase to the Professor:</b><br/>"
        "1. <b>Run Unit Tests:</b> Execute `python3 -m unittest tests/test_suite.py`. Point out that all 6 invariant tests pass in under 0.1 seconds.<br/>"
        "2. <b>Run Experiments:</b> Execute `python3 experiments/run_experiments.py`. Show the 4 generated CSV files and high-resolution PNG plots in `experiments/plots/`.<br/>"
        "3. <b>Highlight Verification:</b> Open `exp3_adversarial_results.csv` and show the professor the `Greedy_CR` column: exactly `0.5000` across all scales!",
        styles['Body']
    ))

    code_snippet = (
        "# Jain's Fairness Index computation in src/metrics.py\n"
        "def compute_jains_index(loads: List[int]) -> float:\n"
        "    arr = np.array(loads, dtype=float)\n"
        "    total = np.sum(arr)\n"
        "    if total == 0:\n"
        "        return 1.0\n"
        "    n = len(arr)\n"
        "    sum_sq = np.sum(arr ** 2)\n"
        "    return float((total ** 2) / (n * sum_sq))"
    )
    story.append(make_code_box(code_snippet, styles))
    story.append(Spacer(1, 4))

    # SECTION H: QUICK REVISION
    story.append(Paragraph("H. Quick Revision & Experimental Fact Sheet", styles['SectionH1']))
    rev_table = [
        ["Experimental Parameter", "Configuration / Value", "Key Observed Outcome"],
        ["City Grid Bounds", "100 &times; 100 km", "Continuous 2D Euclidean metric"],
        ["Skill Universe", "6 skills, 2–4 per volunteer", "Realistic specialization bottleneck"],
        ["Consistency (&eta;=0)", "FTPS CR = <b>0.9903</b>", "Outperforms online heuristics by ~7%"],
        ["Robustness (&eta;=1)", "FTPS CR = <b>0.9208</b>", "Matches robust Water-Filling baseline"],
        ["Adversarial Greedy CR", "Exactly <b>0.5000</b>", "Empirical confirmation of Theorem 2"],
        ["Greedy Jain Index", "Collapses to <b>0.5694</b>", "Severe volunteer overload & burnout"]
    ]
    story.append(make_styled_table(rev_table, [1.8*inch, 2.5*inch, 2.7*inch], styles))
    story.append(Spacer(1, 6))

    story.append(make_callout(
        "When explaining your results to the professor, conclude with: "
        "<b>'Our experimental evaluation proves both halves of the project: it verifies the theoretical 0.50 worst-case barrier for Greedy, "
        "and it demonstrates that our proposed FTPS algorithm achieves 0.99+ consistency while preserving volunteer workload equity.'</b>",
        styles,
        callout_type="tip",
        title="Final Viva Closing Summary"
    ))
