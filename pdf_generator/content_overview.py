"""
Comprehensive Document 5 Content:
Complete Project Overview, Team Coordination & Professor's Viva Defense Guide.
"""

from reportlab.platypus import Paragraph, Spacer, KeepTogether, HRFlowable
from reportlab.lib.units import inch
from .styles import make_callout, make_code_box, make_styled_table


def build_overview_content(story, styles):
    story.append(Paragraph("ONLINE VOLUNTEER DISPATCH FOR EMERGENCY RESPONSE", styles['DocTitle']))
    story.append(Paragraph("Complete Project Overview, Team Coordination & Professor's Viva Defense Guide", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=styles['DocTitle'].textColor, spaceAfter=10))

    # SECTION 1: OVERALL PROJECT EXPLANATION
    story.append(Paragraph("1. Executive Project Overview & Motivation", styles['SectionH1']))
    story.append(Paragraph(
        "In sudden medical emergencies (such as cardiac arrest or severe trauma), brain death begins within 4 to 6 minutes. "
        "Municipal ambulances frequently require 8 to 12 minutes to navigate urban traffic. Modern volunteer-alert systems "
        "(e.g., GoodSAM, PulsePoint) alert trained civilian volunteers who can reach the victim before the ambulance arrives. "
        "However, emergency incidents occur unpredictably in an online fashion. When a 911 incident occurs, the dispatcher must make an "
        "immediate and irrevocable volunteer assignment without knowing what emergencies will arrive later in the shift.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Core Technical Dilemma:</b> Standard dispatch software assigns the nearest eligible volunteer (Greedy heuristic). "
        "However, myopic greedy assignment can rapidly exhaust the shift capacity of specialized volunteers (e.g., pediatric or trauma specialists) "
        "on non-critical early calls, leading to catastrophic failure when life-threatening incidents arrive later. "
        "Furthermore, over-dispatching central volunteers induces severe volunteer burnout. "
        "This research project provides a complete mathematical, algorithmic, and empirical investigation into online volunteer dispatch, "
        "developing an exact offline optimization model, proving the theoretical 1/2 competitive barrier of greedy dispatch, "
        "and proposing a novel learning-augmented algorithm (<b>Follow-the-Prediction with Safeguard - FTPS</b>) that breaks online barriers.",
        styles['Body']
    ))

    # SECTION 2: DIVISION OF RESPONSIBILITIES
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Balanced Division of Work Among Four Team Members", styles['SectionH1']))
    story.append(Paragraph(
        "The project is structured into four balanced, non-overlapping, yet tightly integrated domains. "
        "Each member has full ownership over their specialized domain and code assets:",
        styles['Body']
    ))

    team_table = [
        ["Member & Role", "Specialized Domain & Technical Scope", "Primary Code Assets", "Core Viva Defense Topic"],
        [
            "<b>Member 1</b><br/>Lead Theorist",
            "Problem formalization, eligibility graph E, edge weights w_{vr}, exact ILP formulation, Min-Cost Flow reduction (&mu;=0), Total Unimodularity proof, SciPy HiGHS solver.",
            "`src/models.py`<br/>`src/offline_solver.py`",
            "Why offline is in P (&mu;=0), flow reduction, TUM proof, and LP relaxation."
        ],
        [
            "<b>Member 2</b><br/>Online Theorist",
            "Online paradigm, competitive ratio definition (ALG/OPT), proof of deterministic 1/2 barrier, 2k adversarial counterexample trace, KVV Ranking (1 - 1/e), Water-Filling.",
            "`src/online_algorithms.py`<br/>`src/generator.py` (Adv)",
            "Proof of 1/2 barrier, why Greedy collapses, and how KVV beats 1/2 with random ranks."
        ],
        [
            "<b>Member 3</b><br/>Algorithm Architect",
            "Learning-augmented online algorithms, prediction error metric &eta;, Follow-the-Prediction with Safeguard (FTPS), trust parameter &beta;, Consistency, Robustness, Smoothness proofs.",
            "`src/learning_augmented.py`<br/>`src/generator.py` (Pred)",
            "Consistency proof (&eta;&rarr;0), robustness under noise (&eta;&rarr;1), and safeguard switching."
        ],
        [
            "<b>Member 4</b><br/>Experimental Lead",
            "City-grid simulation, Monte Carlo harness, Exp 1 (&eta;-sweep), Exp 2 (Fairness), Exp 3 (Adversarial), Exp 4 (&lambda;), Jain's Fairness Index, automated unit test suite.",
            "`experiments/run_experiments.py`<br/>`tests/test_suite.py`<br/>`src/metrics.py`",
            "Jain's index trends, 0.50 greedy verification, experimental findings, and unit tests."
        ]
    ]
    story.append(make_styled_table(team_table, [1.4*inch, 2.5*inch, 1.4*inch, 1.7*inch], styles))
    story.append(Spacer(1, 4))

    # SECTION 3: SYSTEM ARCHITECTURE & INTERCONNECTIONS
    story.append(Paragraph("3. End-to-End System Workflow & Component Interconnections", styles['SectionH1']))
    story.append(Paragraph(
        "The project components do not exist in isolation; they form a closed-loop algorithmic pipeline:",
        styles['Body']
    ))

    pipeline_text = (
        "<b>[Historical Data / ML Predictor]</b> &rarr; Generates predicted request sequence &circ;R<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "<b>[Member 1: Exact Flow Solver]</b> &rarr; Solves offline optimum on &circ;R &rarr; Produces planned dispatch table M*_{pred}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "<b>[Member 3: Proposed FTPS Policy]</b> &rarr; Ingests real requests r_t online; tracks running error &circ;&eta;_t<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull; If error &le; &tau;(&beta;) &rarr; Dispatch planned volunteer from M*_{pred}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull; If error &gt; &tau;(&beta;) &rarr; <b>[Member 2: Water-Filling Safeguard]</b> levels workload<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "<b>[Member 4: Benchmark & Test Harness]</b> &rarr; Simulates 100x100km city grid &amp; 2k adversarial traps;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Computes CR = ALG / OPT_{Member 1} and evaluates Jain's Fairness Index"
    )
    story.append(make_code_box(pipeline_text, styles))
    story.append(Spacer(1, 4))

    # SECTION 4: TECHNOLOGIES USED
    story.append(Paragraph("4. Technologies and Scientific Libraries Used", styles['SectionH1']))
    tech_table = [
        ["Technology / Library", "Role in Project", "Key Functions / Modules Employed"],
        ["Python 3.12", "Core implementation language", "Dataclasses, object-oriented design, typing"],
        ["SciPy (HiGHS)", "Exact offline MILP solver", "`scipy.optimize.milp` with continuous L and binary x_{vr}"],
        ["NetworkX 3.7", "Exact offline polynomial solver", "`nx.DiGraph`, `nx.min_cost_flow` for Maximum-Weight b-Matching"],
        ["NumPy 2.5", "Vectorized calculations", "Euclidean distances, matrix constraints, Jain's index sums"],
        ["Pandas 2.2", "Experimental data management", "Grouping, aggregation, and CSV export for 4 experiments"],
        ["Matplotlib 3.8", "Publication visualizer", "300 DPI high-resolution figures with error curves"],
        ["ReportLab 5.1", "Academic PDF generation", "Platypus flowables, two-pass NumberedCanvas, table layout"],
        ["Python Unittest", "Verification & Invariants", "6 automated test cases verifying capacities and bounds"]
    ]
    story.append(make_styled_table(tech_table, [1.5*inch, 2.5*inch, 3.0*inch], styles))
    story.append(Spacer(1, 4))

    # SECTION 5: MASTER VIVA DEFENSE GUIDE (ALL MEMBERS MUST KNOW)
    story.append(Paragraph("5. Master Viva Defense Guide (Questions for Any Team Member)", styles['SectionH1']))
    story.append(Paragraph(
        "Regardless of assigned section, every team member must be able to answer the following core cross-cutting viva questions:",
        styles['Body']
    ))

    master_qas = [
        ("Q1: What is the formal problem statement of Problem Statement 6?",
         "Online Volunteer Dispatch for Emergency Response. A set of volunteers V with skills S_v and capacities &kappa;_v are available. Emergency requests R arrive online sequentially with required skills Q_r, utilities u_r, and survival deadlines &theta;_r. The goal is to immediately and irrevocably match volunteers to incoming requests to maximize total net utility minus travel costs, while ensuring workload fairness."),

        ("Q2: Is the offline problem polynomial or NP-hard? Explain clearly.",
         "When fairness penalty &mu; = 0, the offline problem is in P (polynomial time) because it reduces to Maximum-Weight b-Matching on a bipartite graph, which is solvable via Minimum Cost Flow in O(V^2 E) time. When &mu; &gt; 0, it becomes a Mixed-Integer Linear Program (MILP) with a min-max load envelope."),

        ("Q3: What makes this problem fundamentally hard?",
         "The hardness is not offline computation—the hardness is ONLINE UNCERTAINTY. Requests arrive one by one without future knowledge. Decisions are irrevocable. An omniscient adversary can release early requests that trick the algorithm into consuming scarce specialized volunteers, leaving zero capacity for critical later requests."),

        ("Q4: What is the competitive ratio, and what are the theoretical limits for online matching?",
         "Competitive ratio is min ALG / OPT across all instances. For unweighted online bipartite matching: (1) Deterministic algorithms cannot beat 1/2. (2) Randomized algorithms (KVV Ranking) can reach 1 - 1/e &approx; 0.632. (3) Breaking 1 - 1/e requires predictions!"),

        ("Q5: What is our proposed algorithm, and how does it break the 1 - 1/e barrier?",
         "Our proposed algorithm is Follow-the-Prediction with Safeguard (FTPS). It uses predicted emergency demand &circ;R to pre-compute an optimal offline plan using Min-Cost Flow. In real time, it tracks running error &circ;&eta;_t. When predictions are accurate, it follows the plan to achieve a competitive ratio near 1.0 (we achieved 0.9903). When predictions fail, it switches to a robust baseline (Water-Filling) to ensure safety."),

        ("Q6: What is Jain's Fairness Index, and why is it critical in volunteer dispatch?",
         "J = (&sum; x_i)^2 / (n &sum; x_i^2). Unlike paid staff, volunteers receive no salary. Overloading central volunteers leads to volunteer burnout and app abandonment. Jain's index quantifies workload equity. Water-Filling and FTPS preserved fairness above 0.72, whereas Greedy collapsed to 0.56."),

        ("Q7: How did you prove that Greedy collapses to 0.50 in your code?",
         "We implemented an adversarial instance generator `generate_adversarial_instance(k)` where Phase 1 requests force Greedy to take bottleneck volunteers, causing Phase 2 requests to be rejected. In Experiment 3, across all values of k from 4 to 16, Greedy achieved a competitive ratio of exactly 0.5000, perfectly verifying Theorem 2!"),

        ("Q8: What are the three properties guaranteed by our learning-augmented algorithm?",
         "Consistency (CR &rarr; 1.0 as &eta; &rarr; 0), Robustness (CR &ge; baseline as &eta; &rarr; 1), and Smoothness (monotonic graceful degradation as error grows)."),

        ("Q9: What happens if the travel cost parameter &lambda; is set to 0?",
         "If &lambda; = 0, travel time does not detract from utility as long as c_{vr} &le; &theta;_r. The edge weight is simply w_{vr} = u_r. As &lambda; increases, long-distance dispatches become unprofitable (w_{vr} &le; 0) and are pruned from the graph."),

        ("Q10: What are the primary real-world limitations of our current project model?",
         "Current limitations: (1) Volunteers are assumed static during the shift; (2) Each request requires exactly one volunteer (single-responder model); (3) Travel times are computed via Euclidean distance divided by speed rather than live road traffic networks. Extending to multi-volunteer teams (e.g. CPR + Defibrillator) makes the problem NP-hard (3D matching).")
    ]

    for q, a in master_qas:
        story.append(Paragraph(q, styles['Question']))
        story.append(Paragraph(a, styles['Answer']))

    story.append(Spacer(1, 6))
    story.append(make_callout(
        "<b>TEAM COORDINATION RULE FOR THE VIVA:</b><br/>"
        "• If the professor asks a general question (e.g., 'What is this project about?'), start with the Executive Overview.<br/>"
        "• When the question drills into math, proofs, or Min-Cost Flow &rarr; <b>Member 1 speaks</b>.<br/>"
        "• When the question drills into online lower bounds, KVV, or adversarial examples &rarr; <b>Member 2 speaks</b>.<br/>"
        "• When the question drills into learning-augmented advice, FTPS, or &eta; error bounds &rarr; <b>Member 3 speaks</b>.<br/>"
        "• When the question drills into simulation, graphs, Jain's index, or code tests &rarr; <b>Member 4 speaks</b>.<br/>"
        "This seamless coordination demonstrates outstanding team preparation and project mastery!",
        styles,
        callout_type="tip",
        title="Professor's Panel Viva Strategy"
    ))
