"""
Exhaustive Study Guide Content for Member 2:
Classical Online Algorithms, Competitive Analysis & Baselines.
"""

from reportlab.platypus import Paragraph, Spacer, KeepTogether, HRFlowable
from reportlab.lib.units import inch
from .styles import make_callout, make_code_box, make_styled_table


def build_member2_content(story, styles):
    story.append(Paragraph("MEMBER 2: COMPREHENSIVE VIVA STUDY GUIDE", styles['DocTitle']))
    story.append(Paragraph("Specialization: Classical Online Algorithms, Competitive Analysis & Baselines", styles['DocSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=styles['DocTitle'].textColor, spaceAfter=10))

    # SECTION A
    story.append(Paragraph("A. Section Overview", styles['SectionH1']))
    story.append(Paragraph(
        "This section focuses on the online decision-making paradigm, competitive analysis, adversarial worst-case barriers, "
        "and classical online dispatch heuristics. As Member 2, you own the formalization of online algorithms under uncertainty, "
        "the mathematical proof of the 1/2 competitive ratio barrier for deterministic algorithms, the Karp-Vazirani-Vazirani (KVV 1990) "
        "randomized Ranking algorithm achieving the optimal 1 - 1/e &approx; 0.632 ratio, and the Water-Filling (Balance) heuristic.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Why this section is critical:</b> Online algorithms represent the real-world reality of emergency dispatch. "
        "Because human dispatchers and automated software cannot foresee future 911 calls, they must make irrevocable assignments immediately. "
        "You prove why standard intuitive approaches (like assigning the nearest volunteer) fail catastrophically in the worst case, "
        "and establish the foundational baselines that our learning-augmented algorithm must beat.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Connection to other members:</b><br/>"
        "• <i>To Member 1:</i> You use Member 1's exact offline OPT formulation as the competitive benchmark in your competitive ratio.<br/>"
        "• <i>To Member 3:</i> Your randomized Ranking and Water-Filling algorithms serve as the vital 'safeguard fallback' when Member 3's predictions fail.<br/>"
        "• <i>To Member 4:</i> Your adversarial instance generator and baseline implementations are used by Member 4 in the experimental benchmark suite.",
        styles['Body']
    ))

    # SECTION B
    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Conceptual Understanding", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. Online Computation under Irrevocability:</b><br/>"
        "In an offline setting, all data is available upfront. In an online setting, requests arrive one by one at discrete time steps "
        "<i>t</i> = 1, 2, ..., <i>m</i>. When request <i>r<sub>t</sub></i> arrives, the algorithm must immediately either assign an available "
        "eligible volunteer or reject the request. Once an assignment is made, it cannot be revoked or swapped later.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>2. Competitive Analysis Framework:</b><br/>"
        "Because input distributions in real disasters are unpredictable, average-case analysis can be dangerously optimistic. "
        "Instead, we use <i>competitive analysis</i>, introduced by Sleator and Tarjan (1985). We pit our online algorithm against "
        "a malicious, omniscient <i>Adversary</i> who knows our algorithm's code and constructs the worst possible request sequence.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>3. The Competitive Ratio:</b><br/>"
        "For a maximization problem, the competitive ratio is the worst-case infimum of the ratio between the online algorithm's objective "
        "and the offline optimal objective across all valid instances:",
        styles['Body']
    ))

    cr_box = "Competitive Ratio:   CR(ALG) = inf_{all instances I} [ ALG(I) / OPT(I) ]"
    story.append(make_code_box(cr_box, styles))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>4. Why Nearest-First Greedy Fails:</b><br/>"
        "Greedy is myopic: it optimizes the immediate gain of the current request. "
        "If volunteer <i>v</i> is capable of handling rare trauma emergencies but is currently closest to a common minor sprain, "
        "Greedy dispatches <i>v</i> immediately. When a fatal trauma arrives moments later, <i>v</i> is occupied, leading to tragic rejection.",
        styles['Body']
    ))

    # SECTION C
    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Technical Explanation & Theoretical Proofs", styles['SectionH1']))
    story.append(Paragraph(
        "<b>1. Formal Proof: The Deterministic 1/2 Competitive Barrier (Theorem 2)</b><br/>"
        "<i>Theorem:</i> No deterministic online algorithm for bipartite matching can achieve a competitive ratio strictly greater than 1/2.<br/>"
        "<i>Proof by Adversarial Construction:</i><br/>"
        "Let the volunteer set be <i>V</i> = {v<sub>1</sub>, ..., v<sub>k</sub>, v<sub>k+1</sub>, ..., v<sub>2k</sub>}, all with capacity &kappa; = 1.<br/>"
        "The adversary releases requests in two sequential phases:<br/>"
        "• <b>Phase 1:</b> <i>k</i> requests <i>r</i><sub>1</sub>, ..., <i>r<sub>k</sub></i> arrive. "
        "For each <i>i</i> &isin; {1, ..., k}, request <i>r<sub>i</sub></i> is eligible for exactly two volunteers: {v<sub>i</sub>, v<sub>k+i</sub>}. "
        "Any deterministic online algorithm must assign <i>r<sub>i</sub></i> to one of them. "
        "By setting the coordinates such that <i>c</i>(v<sub>i</sub>, r<sub>i</sub>) &lt; <i>c</i>(v<sub>k+i</sub>, r<sub>i</sub>), "
        "the deterministic greedy algorithm is forced to assign <i>r<sub>i</sub> &rarr; v<sub>i</sub></i>.<br/>"
        "• <b>Phase 2:</b> <i>k</i> requests <i>r</i><sub>k+1</sub>, ..., <i>r</i><sub>2k</sub> arrive. "
        "For each <i>i</i> &isin; {1, ..., k}, request <i>r</i><sub>k+i</sub> is eligible <b>only</b> for volunteer <i>v<sub>i</sub></i>.<br/>"
        "<b>Outcome Analysis:</b><br/>"
        "- In Phase 2, the online algorithm finds that volunteer <i>v<sub>i</sub></i> is already saturated (&kappa;<sub>v<sub>i</sub></sub> = 0). "
        "Therefore, the online algorithm must reject all <i>k</i> requests in Phase 2! Total matches = <i>k</i>.<br/>"
        "- The offline optimal (OPT), knowing Phase 2 in advance, matches Phase 1 requests to the second group: <i>r<sub>i</sub> &rarr; v<sub>k+i</sub></i>, "
        "leaving <i>v<sub>1</sub>, ..., v<sub>k</sub></i> completely free for Phase 2: <i>r</i><sub>k+i</sub> &rarr; <i>v<sub>i</sub></i>. Total matches = 2<i>k</i>.<br/>"
        "Competitive Ratio = <i>k</i> / 2<i>k</i> = <b>1/2 = 0.50</b>. Q.E.D.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>2. Breaking the 1/2 Barrier: Karp-Vazirani-Vazirani (KVV 1990) Ranking</b><br/>"
        "Deterministic algorithms fail because the adversary knows exactly which volunteer the algorithm will pick. "
        "To defeat the adversary, KVV introduced randomized <b>Ranking</b>:<br/>"
        "1. Prior to the arrival of any requests, choose a random permutation &pi; of the volunteers <i>V</i>. "
        "Equivalently, draw an independent continuous rank <i>Y<sub>v</sub></i> &sim; Uniform(0, 1) for each volunteer.<br/>"
        "2. When request <i>r</i> arrives, examine all available, eligible volunteers and assign <i>r</i> to the volunteer with the "
        "highest priority (lowest <i>Y<sub>v</sub></i>).<br/>"
        "<b>Theoretical Guarantee:</b> KVV proved using a gain-sharing differential equation that Ranking achieves an expected competitive ratio of:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>CR(KVV Ranking) = 1 - 1/e &approx; 0.6321</b><br/>"
        "This is strictly optimal: no online algorithm (even randomized) can beat 1 - 1/e against an adaptive adversary.",
        styles['Body']
    ))

    story.append(Paragraph(
        "<b>3. Water-Filling / Balance Algorithm:</b><br/>"
        "While KVV randomizes priority, the <i>Water-Filling (Balance)</i> algorithm optimizes workload leveling:<br/>"
        "When request <i>r</i> arrives, choose eligible volunteer: <i>v* = argmin_{v &isin; eligible(r)} ( current_load(v), -w_{vr} )</i>.<br/>"
        "By always directing demand to the volunteer with the fewest assignments, Water-Filling preserves capacity across the network "
        "and directly maximizes Jain's Fairness Index.",
        styles['Body']
    ))

    # SECTION D
    story.append(Spacer(1, 4))
    story.append(Paragraph("D. Step-by-Step Working: The 2k Adversarial Counterexample", styles['SectionH1']))
    story.append(Paragraph(
        "Let us trace a concrete adversarial instance with <i>k</i> = 2 (4 volunteers, 4 requests, all capacities = 1, utility = 20):",
        styles['Body']
    ))

    adv_table = [
        ["Step", "Incoming Request", "Eligible Volunteers", "Greedy Action", "KVV Ranking Action", "OPT Action"],
        ["t = 1", "r1 (Phase 1)", "{v1, v3}", "Assigns v1 (closest)", "50% v1, 50% v3", "Assigns v3"],
        ["t = 2", "r2 (Phase 1)", "{v2, v4}", "Assigns v2 (closest)", "50% v2, 50% v4", "Assigns v4"],
        ["t = 3", "r3 (Phase 2)", "{v1 only}", "REJECTED (v1 busy!)", "Matches if v1 free", "Assigns v1"],
        ["t = 4", "r4 (Phase 2)", "{v2 only}", "REJECTED (v2 busy!)", "Matches if v2 free", "Assigns v2"],
        ["Total", "4 Requests", "---", "<b>2 Matched (CR=0.50)</b>", "<b>3 Matched (CR=0.75)</b>", "<b>4 Matched (CR=1.0)</b>"]
    ]
    story.append(make_styled_table(adv_table, [0.8*inch, 1.2*inch, 1.2*inch, 1.3*inch, 1.3*inch, 1.2*inch], styles))
    story.append(Spacer(1, 4))

    # SECTION E
    story.append(Paragraph("E. Important Decisions & Justifications", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Decision 1: Why evaluate both Greedy and Random baselines?</b><br/>"
        "<i>Justification:</i> Greedy represents the standard industry practice (dispatch the closest responder). "
        "Random represents the unguided stochastic lower bound. Showing that Greedy can collapse to 0.5 highlights the real-world vulnerability of naive heuristics.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Decision 2: Why choose Water-Filling as the primary fallback policy for Member 3?</b><br/>"
        "<i>Justification:</i> In emergency response, volunteer burnout is a major cause of network collapse. "
        "Water-Filling guarantees workload distribution across volunteers, keeping maximum load low while maintaining high competitive ratios.",
        styles['Body']
    ))

    # SECTION F: VIVA QUESTIONS
    story.append(Spacer(1, 4))
    story.append(Paragraph("F. Comprehensive Viva Preparation & Defense", styles['SectionH1']))

    qas = [
        ("Q1: What is an online algorithm, and how is its performance evaluated?",
         "An online algorithm processes its input piece-by-piece in serial order without knowing the entire input sequence. Its performance is evaluated using the Competitive Ratio: the worst-case ratio of the algorithm's objective value to the offline optimal objective value (ALG / OPT) across all possible input sequences."),

        ("Q2: State and explain the 1/2 competitive ratio barrier for deterministic online matching.",
         "No deterministic online algorithm can achieve a competitive ratio greater than 1/2 for bipartite matching. The adversary presents requests in two waves: Phase 1 requests have multiple choices including bottleneck volunteers; the deterministic algorithm consumes the bottlenecks. Phase 2 requests strictly require those consumed bottlenecks, forcing the algorithm to reject them while OPT satisfies all requests."),

        ("Q3: What is the difference between an Oblivious Adversary and an Adaptive Adversary?",
         "An Oblivious Adversary must fix the complete sequence of requests in advance before the online algorithm begins execution. An Adaptive Adversary can observe the algorithm's randomized choices at each step and dynamically choose the next request to inflict maximum damage."),

        ("Q4: How does the Karp-Vazirani-Vazirani (KVV) Ranking algorithm beat the 1/2 barrier?",
         "KVV randomizes the volunteer preference order upfront by drawing independent uniform ranks Y_v ~ Uniform(0, 1). Because the adversary cannot predict which volunteer has the highest priority rank, the adversary cannot reliably force the algorithm into exhausting bottleneck volunteers, achieving an expected ratio of 1 - 1/e &approx; 0.632."),

        ("Q5: Where does the constant 1 - 1/e come from mathematically in KVV?",
         "It arises from the differential equation governing the probability that a volunteer is matched when ranks are continuous. In the continuous limit, the gain-sharing function g(y) = e^{y-1} satisfies g'(y) = g(y) with boundary condition integral_0^1 g(y) dy = 1 - 1/e."),

        ("Q6: How does the Water-Filling (Balance) algorithm work in our implementation?",
         "In `src/online_algorithms.py`, when a request arrives, Water-Filling identifies all eligible volunteers with remaining capacity and selects the volunteer who has the minimum current load: argmin (current_load, -weight). Ties are broken by the highest net utility weight."),

        ("Q7: In your experimental results, how did Greedy perform on random arrivals vs adversarial arrivals?",
         "On random synthetic city-grid arrivals, Greedy achieved a competitive ratio of &approx; 0.924 because random arrivals rarely trigger pathological upper-triangular bottleneck structures. However, on our adversarial generator, Greedy collapsed immediately to exactly 0.5000, confirming the theoretical theorem!"),

        ("Q8: Why does the Random baseline perform worse than Greedy on random instances?",
         "The Random baseline picks any eligible volunteer uniformly at random, frequently picking distant volunteers with high travel times c_{vr}. This reduces the net objective w_{vr} = u_r - &lambda; c_{vr} and exhausts capacities indiscriminately."),

        ("Q9: What happens if all requests have the same utility u_r = 1 and &lambda; = 0?",
         "The problem reduces to unweighted online bipartite matching. On unweighted graphs, KVV Ranking achieves exactly 1 - 1/e in expectation, and Greedy achieves at least 1/2 on any graph."),

        ("Q10: Challenging Follow-up: Can any online algorithm achieve a competitive ratio strictly greater than 1 - 1/e for general bipartite graphs without predictions?",
         "No! KVV (1990) proved an information-theoretic matching upper bound: 1 - 1/e is the absolute upper limit for randomized online bipartite matching without advice. Breaking 1 - 1/e requires additional assumptions or predictions (which is what Member 3's learning-augmented algorithm accomplishes!).")
    ]

    for q, a in qas:
        story.append(Paragraph(q, styles['Question']))
        story.append(Paragraph(a, styles['Answer']))

    # SECTION G: PRACTICAL UNDERSTANDING
    story.append(Spacer(1, 4))
    story.append(Paragraph("G. Practical Understanding & Code Implementation", styles['SectionH1']))
    story.append(Paragraph(
        "<b>Key Source Files Owned by Member 2:</b><br/>"
        "• `src/online_algorithms.py`: Contains `OnlineAlgorithms.run_greedy()`, `run_ranking()`, `run_water_filling()`, and `run_random()`.<br/>"
        "• `src/generator.py`: Contains `InstanceGenerator.generate_adversarial_instance(k)` which constructs the hard 2k counterexample.",
        styles['Body']
    ))

    code_snippet = (
        "# KVV Ranking implementation in src/online_algorithms.py\n"
        "ranks = {v.id: random.random() for v in instance.volunteers}\n"
        "for req in instance.requests:\n"
        "    candidates = [v.id for v in instance.volunteers\n"
        "                  if v.is_available() and instance.is_eligible(v.id, req.id)]\n"
        "    if candidates:\n"
        "        # Pick volunteer with lowest Y_v (highest priority)\n"
        "        chosen_v_id = min(candidates, key=lambda v_id: ranks[v_id])\n"
        "        instance.v_map[chosen_v_id].assign(req.id)"
    )
    story.append(make_code_box(code_snippet, styles))
    story.append(Spacer(1, 4))

    # SECTION H: QUICK REVISION
    story.append(Paragraph("H. Quick Revision & Cheat Sheet", styles['SectionH1']))
    rev_table = [
        ["Algorithm", "Decision Rule", "Competitive Ratio", "Vulnerability"],
        ["Greedy", "argmax w_{vr}", "At most 1/2 in worst-case", "Vulnerable to adversarial traps"],
        ["Random", "Uniform random eligible", "Arbitrarily low weights", "High travel times, poor utility"],
        ["KVV Ranking", "argmin Y_v ~ U(0, 1)", "1 - 1/e &approx; 0.632", "Ignores edge weight heterogeneity"],
        ["Water-Filling", "argmin current_load", "Heuristic (Fairness)", "Guards against volunteer burnout"]
    ]
    story.append(make_styled_table(rev_table, [1.3*inch, 2.0*inch, 1.8*inch, 1.9*inch], styles))
    story.append(Spacer(1, 6))

    story.append(make_callout(
        "When asked by the professor why Greedy is dangerous in real hospitals or 911 dispatch, state: "
        "<b>'Greedy is spatially greedy but temporally blind. It exhausts scarce, specialized responders on mundane early calls, "
        "leaving zero capacity when high-severity emergencies strike later.'</b>",
        styles,
        callout_type="warning",
        title="Professor's Favorite Real-World Question"
    ))
