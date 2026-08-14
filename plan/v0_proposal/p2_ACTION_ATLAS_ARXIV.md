# ACTION-ATLAS: Beyond Action Prediction: What Must World Models Achieve to Surpass Vision-Language-Action Systems?

**Amitava Das\***

\*Pragya Lab, BITS Pilani Goa, India

## Abstract

Recent advances in robotics have produced competing narratives for embodied intelligence. One view argues that increasingly capable **Vision-Language-Action (VLA)** models can achieve general-purpose robotic behavior through direct observation-to-action mappings. Representative systems include **OpenVLA, Octo, $\pi_0$/$\pi_{0.5}$, GR00T, Gemini Robotics**, and **Helix**. A second view argues that direct action prediction is insufficient, motivating a broader class of predictive architectures: *(i)* **Latent World Models (LWMs)** such as **I-JEPA, V-JEPA, V-JEPA2, MC-JEPA**, and **H-JEPA**; *(ii)* **Executable World Action Models (WAMs)** such as **DreamZero, Fast-WAM, $\tau_0$-WM**, and **Unified Video Action (UVA)**; and *(iii)* **World Foundation Models (WFMs)** such as **Cosmos 3, Cosmos Transfer**, and **Cosmos Policy**. Despite growing enthusiasm for these predictive systems, the field lacks a principled framework for determining when world models actually improve robotic intelligence over action-centric policies.

We introduce **ACTION-ATLAS**, a capability-centric benchmark and evaluation framework designed to measure *when world modeling matters for robotics*. Existing evaluations are fundamentally misaligned: VLA systems are typically measured through task success, while world models are often evaluated through future prediction quality, rollout realism, latent consistency, or generative fidelity. ACTION-ATLAS instead evaluates whether predictive representations improve *closed-loop embodied behavior*. The benchmark is organized around four capability domains: **Absent Objects**, covering hidden-object retrieval, occluded manipulation, and object permanence; **Counterfactual Futures**, covering route replanning, dynamic obstacle avoidance, and alternative-action selection; **Temporal Coordination**, covering kitchen setup, table preparation, multi-room delivery, and other long-horizon tasks; and **Interactive Others Navigation (ION)**, covering pedestrian crossing, crowd navigation, and multi-agent interaction.

To compare model families under a unified protocol, ACTION-ATLAS evaluates systems from four classes: *(I)* **VLA policies**, which directly map observation and language to action; *(II)* **JEPA-style latent world models**, which learn predictive state representations but require downstream policies for execution; *(III)* **world-action models**, which jointly predict future states and executable actions; and *(IV)* **world foundation models**, which act as large-scale simulators, planners, or policy backbones. We introduce the **World Advantage Score (WAS)**, a capability-level metric measuring whether predictive representations yield statistically significant gains over direct action prediction.

Our analysis is designed to test a concrete hypothesis: **VLAs should remain highly competitive on short-horizon manipulation and instruction-following tasks**, while **LWMs should improve hidden-state reasoning and object persistence**, **WAMs should provide the strongest gains in counterfactual planning and long-horizon coordination**, and **WFMs should be most useful for social forecasting and open-world interaction**. Crucially, ACTION-ATLAS tests whether these gains survive in closed-loop robotic execution rather than only in open-loop prediction.

The expected finding is not that one family universally dominates. Instead, ACTION-ATLAS reframes the debate from *"Do world models beat VLAs?"* to *"Which robotic capabilities require which form of world modeling?"* By jointly evaluating **OpenVLA/Octo/$\pi_0$/GR00T/Gemini Robotics**-style VLAs, **JEPA**-style LWMs, **DreamZero/Fast-WAM/$\tau_0$-WM/UVA**-style WAMs, and **Cosmos**-style WFMs, ACTION-ATLAS provides a rigorous burden-of-proof framework for future claims that predictive world representations surpass direct action prediction in robotics.

## 1 World Modeling as a Capability Hypothesis

Robotics is entering a phase in which the central debate is no longer whether large-scale multimodal learning can produce useful robot policies. That question has largely been answered in the affirmative. Systems such as RT-1, RT-2, Octo, OpenVLA, $\pi_0$, GR00T N1, and Gemini Robotics have demonstrated that large models trained on heterogeneous robot data, vision-language pretraining, and instruction-conditioned action traces can produce increasingly general robot behaviors (Brohan et al., 2022, 2023; Octo Model Team et al., 2024; Kim et al., 2024; Black et al., 2024; Bjorck et al., 2025; Gemini Robotics Team et al., 2025). These systems have made the **Vision-Language-Action (VLA)** paradigm the dominant framing for general-purpose robotics: given visual observations and a language instruction, learn a policy that directly predicts executable robot actions.

**The action-centric hypothesis.** The success of VLA systems has shifted robotics toward what we call the *action-centric hypothesis*: sufficiently large multimodal policies, trained on sufficiently diverse robot demonstrations, may learn the perceptual, semantic, and motor regularities needed for broad embodied competence. This hypothesis is compelling because it scales with the ingredients that have already driven progress in language and vision: data diversity, model capacity, and transfer from internet-scale pretraining. RT-2 showed that vision-language models can transfer web-scale semantic knowledge into robotic control (Brohan et al., 2023); OpenVLA demonstrated that open-source VLA models trained on large robot demonstration corpora can serve as effective generalist manipulation policies (Kim et al., 2024); Octo showed that large transformer policies can be adapted across diverse robot platforms and sensory-action configurations (Octo Model Team et al., 2024); and $\pi_0$ introduced a flow-based action generation formulation for general robot control (Black et al., 2024). More recent humanoid-oriented systems such as GR00T N1 and Gemini Robotics further extend the VLA paradigm toward whole-body control, dexterous manipulation, and embodied reasoning (Bjorck et al., 2025; Gemini Robotics Team et al., 2025).

**The competing hypothesis.** Yet a competing view is now gaining force. The argument is not that VLA systems are weak; rather, it is that *direct action prediction may be the wrong abstraction for open-world robotics*. Real environments are partially observable, temporally extended, physically constrained, and populated by other agents. A robot must often act under uncertainty about what is hidden, what will move, what will fail, and what other agents are likely to do. In such settings, the relevant question is not only *which action should be taken now*, but also *what world state will result if this action is taken, what alternatives are possible, and how future observations should revise the current belief state*. These requirements motivate a second hypothesis: the *world-modeling hypothesis*.

**The world-modeling hypothesis.** We use the term **world-modeling hypothesis** to denote the claim that predictive internal representations of the environment enable robotic capabilities that cannot be reliably obtained from reactive observation-to-action mappings alone. This hypothesis appears in multiple architectural forms:

  (i) **Latent World Models (LWMs)**, including JEPA-family systems such as I-JEPA and V-JEPA2, learn predictive representations in latent space rather than reconstructing pixels directly (Assran et al., 2023, 2025).

  (ii) **Executable World Action Models (WAMs)**, such as DreamZero, aim to jointly model future world states and the robot actions that produce them (Ye et al., 2026).

  (iii) **World Foundation Models (WFMs)**, including recent Cosmos-style systems, attempt to scale world simulation using large multimodal datasets spanning images, videos, audio, text, and action traces.

Across these families, the shared claim is that prediction is not merely an auxiliary objective, but a mechanism for improved embodied decision making.

**Why existing evidence is inconclusive.** However, the current evidence for the world-modeling hypothesis remains difficult to interpret. Existing evaluations often compare different families of models using fundamentally different criteria:

  (i) VLA systems are typically evaluated through **task success**, **instruction following**, **manipulation accuracy**, and **closed-loop execution**.

  (ii) Latent and generative world models are often evaluated through **representation quality**, **future prediction accuracy**, **rollout realism**, **latent consistency**, or **generative fidelity**.

These metrics are not interchangeable. A model that predicts visually plausible futures may still fail to select better actions. Conversely, a VLA policy may solve a task without constructing an explicit predictive representation of the world. Thus, the field currently risks conflating *predicting the future* with *acting better in the future*.

**Our position: prediction must improve action.** This distinction is central to our work. *Future prediction is not itself a robotic capability.* It is a computational mechanism that may or may not improve robotic behavior. A world model should therefore not be considered superior to a VLA merely because it produces realistic rollouts or accurate latent forecasts. It should be considered superior only when those predictions yield measurable gains in **closed-loop embodied performance**. In other words, the burden of proof for world modeling is behavioral: prediction must improve action.

**The missing benchmark.** We argue that this burden of proof has not yet been formalized. The community lacks a benchmark that asks, in a controlled and capability-specific way, when world modeling provides advantages over action-centric policies. This gap is especially important because different robotic capabilities may require different forms of prediction:

  (i) **Hidden-state reasoning** may benefit from latent predictive representations.

  (ii) **Counterfactual planning** may require executable world-action simulation.

  (iii) **Long-horizon coordination** may require temporally abstract future models.

  (iv) **Social interaction** may require large-scale generative models of other agents.

A single binary question---"Do world models beat VLAs?"---therefore obscures the more important scientific question: *which capabilities require which kinds of world modeling?*

**ACTION-ATLAS.** To address this gap, we introduce **ACTION-ATLAS**, a capability-centric benchmark and evaluation framework for predictive embodied intelligence. ACTION-ATLAS is built around four capability domains that we hypothesize are especially diagnostic of world-modeling benefits:

  (i) **Absent Objects**, which tests hidden-state reasoning and object permanence under partial observability.

  (ii) **Counterfactual Futures**, which tests the ability to evaluate alternative futures before acting.

  (iii) **Temporal Coordination**, which tests long-horizon planning and multi-stage execution.

  (iv) **Interactive Others Navigation (ION)**, which tests social forecasting and interaction-aware planning in multi-agent environments.

Rather than treating VLA, LWM, WAM, and WFM systems as mutually exclusive competitors, ACTION-ATLAS evaluates them as points along a spectrum of predictive embodied intelligence. The goal is not to declare a universal winner. Instead, the goal is to identify:

  (i) the capability regimes in which **direct action prediction is sufficient**;

  (ii) the regimes in which **latent prediction is useful**;

  (iii) the regimes in which **action-conditioned future simulation is necessary**; and

  (iv) the regimes in which **large-scale world simulation provides additional advantage**.

This framing turns the world-modeling debate from a contest of architectures into a testable set of capability hypotheses.

**Contributions.** Our contributions are as follows:

  (i) We formulate the **world-modeling hypothesis** as a behavioral claim: predictive representations matter only when they improve embodied decision making.

  (ii) We introduce **ACTION-ATLAS**, a benchmark organized around robotic capabilities rather than model architectures.

  (iii) We propose a unified taxonomy spanning **Vision-Language-Action Models**, **Latent World Models**, **Executable World Action Models**, and **World Foundation Models**.

  (iv) We define the **World Advantage Score (WAS)**, a capability-level metric for quantifying when predictive world representations produce statistically meaningful gains over direct action prediction.

In summary, ACTION-ATLAS asks a more precise question than whether world models are "better" than VLAs. It asks: *which robotic competencies genuinely require predictive world representations, and when does future simulation become more valuable than direct action prediction?*

## 2 A Taxonomy of Predictive Embodied Intelligence

The rapid emergence of world-modeling approaches has created a growing ambiguity in the robotics literature. The term *world model* is now used to describe a broad collection of systems, including latent predictive architectures such as JEPA, action-conditioned simulators such as World Action Models (WAMs), and large-scale generative systems such as Cosmos. Although these approaches differ substantially in objectives, representations, and deployment mechanisms, they are frequently discussed under a single umbrella. Consequently, comparisons between action-centric and world-centric robotics often conflate fundamentally different forms of prediction.

We argue that contemporary embodied intelligence should not be viewed as a binary distinction between **Vision-Language-Action (VLA)** systems and **world models**. Instead, it is more accurately understood as a spectrum of increasingly predictive architectures. Along this spectrum, systems differ in three fundamental dimensions:

  (i) **What is predicted**: actions, latent states, future observations, or complete world trajectories.

  (ii) **How prediction is represented**: implicit policies, latent embeddings, action-conditioned dynamics, or generative simulation.

  (iii) **How prediction is utilized**: direct action execution, planning, belief maintenance, counterfactual reasoning, or policy evaluation.

This perspective leads to a unified taxonomy consisting of four major families: **Vision-Language-Action Models (VLAs)**, **Latent World Models (LWMs)**, **World Action Models (WAMs)**, and **World Foundation Models (WFMs)**. Rather than representing competing paradigms, these families occupy different positions along a continuum of predictive embodied intelligence.

**A common notation.** Let $o_t$ denote the robot's observation at time $t$, $l$ a language instruction, $a_t$ an executable action, $s_t$ the underlying world state, and $z_t = f_\theta(o_{\leq t})$ a learned latent representation inferred from the observation history. The true world evolves according to an unknown transition process:

$$s_{t+1} \sim \mathcal{T}(s_t, a_t),$$

while the robot only observes a partial projection:

$$o_t \sim \mathcal{O}(s_t).$$

The central distinction among model families is therefore not whether they process observations, language, or actions, but whether they explicitly model some part of the transition:

$$\text{current evidence} \longrightarrow \text{future consequence}$$

This distinction will be crucial for ACTION-ATLAS: a model's predictive machinery matters only if it improves downstream embodied decision making.

> **Figure 1: The predictive embodied intelligence spectrum.**
> Reactive Policies → Vision-Language-Action Models → Latent World Models → World Action Models → World Foundation Models
>
> Modern robotics is not evolving through a simple replacement of VLAs by world models. Instead, successive families introduce increasingly explicit forms of prediction, ranging from direct action generation to latent prediction, action-conditioned simulation, and large-scale world modeling.

### 2.1 Vision-Language-Action Models

Vision-Language-Action models constitute the dominant paradigm for contemporary embodied intelligence. These systems directly map observations and language instructions to executable actions:

$$\pi_\theta(a_t \mid o_{\leq t}, l).$$

In many implementations, the model predicts either a single low-level action, a short action chunk, or a distribution over future motor commands:

$$a_{t:t+H} \sim \pi_\theta(\cdot \mid o_{\leq t}, l),$$

where $H$ denotes the action horizon.

Representative systems include RT-1, RT-2, OpenVLA, Octo, $\pi_0$, GR00T N1, and Gemini Robotics (Brohan et al., 2022, 2023; Octo Model Team et al., 2024; Kim et al., 2024; Black et al., 2024; Bjorck et al., 2025; Gemini Robotics Team et al., 2025). These models have demonstrated that large-scale multimodal learning can produce highly capable robotic policies without requiring explicit world simulation.

The defining characteristic of VLAs is that prediction is concentrated on the next action rather than on future world states. Any internal representation of future consequences remains implicit within the policy. A VLA may internally encode useful regularities about objects, affordances, and action outcomes, but it is not explicitly trained to expose a transition model of the form:

$$(o_t, a_t) \rightarrow o_{t+1} \quad \text{or} \quad (s_t, a_t) \rightarrow s_{t+1}.$$

**Example.** Given the instruction *"pick up the red mug and place it on the table"*, a VLA directly predicts motor commands conditioned on the current camera view and language instruction. If the mug remains visible and the task is short-horizon, direct action prediction may be sufficient. However, if the mug is moved behind an occluder, the model must rely on whatever memory is implicitly encoded in its hidden state rather than an explicit belief over the hidden object location.

**Strengths.** VLAs excel at:

  (i) language grounding,

  (ii) manipulation,

  (iii) skill composition,

  (iv) instruction following,

  (v) low-latency execution.

**Limitations.** However, VLAs often face challenges involving:

  (i) hidden-state reasoning,

  (ii) counterfactual evaluation,

  (iii) long-horizon planning,

  (iv) explicit uncertainty tracking.

### 2.2 Latent World Models

Latent World Models (LWMs) represent the first major departure from action-centric robotics. Rather than directly predicting actions, these systems learn predictive latent representations of the environment:

$$z_t = f_\theta(o_{\leq t}), \qquad \hat{z}_{t+k} = g_\phi(z_t, k).$$

where $z_t$ denotes a learned latent state and $\hat{z}_{t+k}$ denotes the predicted future representation after $k$ steps.

Representative examples include I-JEPA, V-JEPA, V-JEPA2, MC-JEPA, and H-JEPA (Assran et al., 2023, 2025). Unlike traditional generative models, JEPA-style systems learn to predict semantically meaningful latent representations rather than reconstructing pixels.

A generic latent predictive objective can be written as:

$$\mathcal{L}_{\text{LWM}} = d\big(g_\phi(f_\theta(o_{\leq t}), k),\, f_{\bar\theta}(o_{t+k})\big).$$

where $d(\cdot, \cdot)$ is a latent-space distance and $f_{\bar\theta}$ is a target encoder. The important point is that the model is encouraged to predict *future structure*, not necessarily future pixels.

This distinction is important. Predicting pixels often forces a model to allocate capacity to low-level visual details. Predicting latent representations instead encourages the model to focus on persistent structure, object relationships, and higher-level dynamics. Consequently, LWMs can be viewed as *belief-maintenance systems*. Their primary objective is not action generation but predictive state estimation.

**Example.** In an occlusion scenario, a JEPA-style model may not reconstruct the exact pixels of a hidden object. Instead, it may maintain a latent representation consistent with the object's continued existence and likely future reappearance. This is precisely the type of capability needed for **Absent Objects** tasks in ACTION-ATLAS.

**Strengths.** LWMs naturally support:

  (i) hidden-state tracking,

  (ii) object permanence,

  (iii) predictive memory,

  (iv) representation learning.

**Limitations.** However, they generally:

  (i) do not directly generate actions,

  (ii) require downstream policies,

  (iii) lack explicit planning mechanisms.

### 2.3 World Action Models

World Action Models extend predictive representation learning by explicitly coupling future prediction with action generation. Instead of predicting only latent states, WAMs model the consequences of actions:

$$\hat{s}_{t+1} = F_\theta(s_t, a_t).$$

where $\hat{\tau}_{t:t+H}$ denotes a predicted future trajectory over states, observations, and possibly actions.

Representative systems include DreamZero, Fast-WAM, $\tau_0$-WM, and Unified Video Action (UVA) (Ye et al., 2026).

The defining idea behind WAMs is that actions should be selected through future simulation rather than direct policy execution. A WAM therefore enables **counterfactual reasoning**: the robot can evaluate multiple possible futures before deciding which action to execute.

A generic WAM decision rule can be written as:

$$a_t^\star = \arg\max_{a_t \in \mathcal{A}} U\big(F_\theta(s_t, a_t, l)\big).$$

where $U(\cdot)$ is a task utility function measuring whether the predicted future satisfies the instruction. For longer horizons, this becomes:

$$a_{t:t+H}^\star = \arg\max_{a_{t:t+H}} U\big(F_\theta(s_t, a_{t:t+H}, l)\big).$$

**Example.** Consider a robot navigating to a goal when the direct route becomes blocked. A VLA may react to the obstacle locally. A WAM can evaluate multiple candidate futures: continuing forward, turning left, turning right, or backtracking. It can then select the action sequence whose predicted future best satisfies the goal while avoiding collision.

**Strengths.** WAMs are particularly well suited for:

  (i) counterfactual planning,

  (ii) action-conditioned prediction,

  (iii) long-horizon coordination,

  (iv) model-based control.

**Limitations.** Their primary challenges include:

  (i) rollout drift,

  (ii) simulation-reality mismatch,

  (iii) computational cost.

### 2.4 World Foundation Models

World Foundation Models represent the most ambitious form of predictive embodied intelligence. These systems seek to learn general-purpose simulators of environments, objects, agents, and interactions from large-scale multimodal data.

Representative examples include Cosmos 3, Cosmos Transfer, and Cosmos Policy.

Unlike LWMs and WAMs, which are often trained on robotics-specific datasets, WFMs are typically trained on internet-scale collections of images, videos, text, audio, and action traces. Their objective is not merely to predict the next state but to construct a broadly transferable model of world dynamics.

A WFM can be abstractly described as a generative simulator:

$$p_\theta(x_{t:t+H} \mid x_{\leq t}, c).$$

where $x$ may include video, audio, text, object states, agent trajectories, or actions, and $c$ denotes conditioning information such as language, scene context, or task goal.

In robotics, WFMs may be used in multiple modes:

$$\text{WFM-as-Simulator}: \quad p_\theta(x_{t:t+H} \mid x_{\leq t}, c).$$

$$\text{WFM-as-Critic}: \quad R_\theta(\tau, l).$$

$$\text{WFM-as-Policy-Backbone}: \quad \pi_\theta(a_t \mid o_{\leq t}, l, \hat{x}_{t:t+H}).$$

Thus, WFMs may not always be executable robot policies by themselves. Their value may lie in simulating futures, ranking plans, generating synthetic experience, or providing predictive priors to downstream controllers.

WFMs therefore move beyond robotic control and toward general predictive intelligence.

**Example.** In a dense street scene, a WFM may forecast the likely motion of pedestrians, vehicles, animals, and vendors even when the robot has limited prior experience in that exact environment. Such forecasting can be used to score candidate robot trajectories or generate risk-aware plans.

**Strengths.** WFMs naturally support:

  (i) open-world prediction,

  (ii) social forecasting,

  (iii) agent interaction modeling,

  (iv) large-scale transfer.

**Limitations.** However, they often suffer from:

  (i) embodiment mismatch,

  (ii) expensive inference,

  (iii) weak grounding to specific robot platforms.

### 2.5 Comparative Analysis

The proposed taxonomy reveals that these families differ not merely in architecture but in the type of predictive capability they provide. Table 1 summarizes the distinction.

**Table 1: Comparison of predictive embodied intelligence families.** The four families differ in the nature of prediction, the degree of coupling between prediction and action, and the capabilities they are expected to support.

| Property | VLA | LWM | WAM | WFM |
|---|---|---|---|---|
| Direct Action Generation | Yes | No | Yes | Optional |
| Primary Prediction Target | Action | Latent State | State–Action Trajectory | World Trajectory |
| Future State Prediction | Implicit | Yes | Yes | Yes |
| Prediction Representation | Policy Hidden State | Latent Embedding | Action-Conditioned Dynamics | Generative Simulation |
| Hidden-State Reasoning | Limited | Yes | Yes | Yes |
| Counterfactual Planning | Limited | Limited | Yes | Yes |
| Long-Horizon Coordination | Limited | Moderate | Yes | Yes |
| Social Forecasting | Limited | Moderate | Moderate | Yes |
| Open-World Transfer | Moderate | Moderate | Moderate | Yes |
| Closed-Loop Execution | Yes | Requires Policy | Yes | Optional |
| Main Failure Mode | Reactive Myopia | Non-Executable Latents | Rollout Drift | Embodiment Mismatch |

### 2.6 The Capability Hierarchy Hypothesis

The taxonomy suggests a final hypothesis that motivates the remainder of this paper.

*Predictive architectures should not be viewed as replacements for one another, but as mechanisms supporting different robotic capabilities.*

Specifically, we hypothesize that:

  (i) **VLAs** will remain highly competitive on manipulation and instruction-following tasks.

  (ii) **LWMs** will provide advantages for hidden-state reasoning and object permanence.

  (iii) **WAMs** will provide the largest gains in counterfactual planning and long-horizon coordination.

  (iv) **WFMs** will be most beneficial for social forecasting and open-world interaction.

This hypothesis can be expressed as a capability-family alignment:

$$\mathcal{C}_{\text{short}} \to \text{VLA}, \qquad \mathcal{C}_{\text{hidden}} \to \text{LWM}, \qquad \mathcal{C}_{\text{counterfactual}} \to \text{WAM}, \qquad \mathcal{C}_{\text{open}} \to \text{WFM}.$$

If this hypothesis is correct, then no single architecture should dominate all robotic competencies. Instead, different capabilities will require different forms of predictive world modeling. This observation motivates the central question of ACTION-ATLAS: *which robotic capabilities genuinely benefit from prediction, and what form of prediction is required?*

## 3 ACTION-ATLAS: Evaluating Predictive Embodied Intelligence

The central premise of ACTION-ATLAS is that predictive representations should be evaluated through the robotic capabilities they enable rather than the architectures that produce them. Existing benchmarks typically compare systems at the model level, reporting aggregate task success rates across manipulation, navigation, or instruction-following datasets. While useful for measuring overall performance, such evaluations provide little insight into *why* a model succeeds or which forms of predictive reasoning contribute to that success.

As argued in Sections 1 and 2, the emerging debate surrounding Vision-Language-Action Models (VLAs), Latent World Models (LWMs), World Action Models (WAMs), and World Foundation Models (WFMs) is fundamentally a debate about capabilities. A world model should not be considered superior merely because it predicts future states accurately. Rather, it should be considered superior only when those predictions translate into improved embodied decision making.

ACTION-ATLAS therefore adopts a capability-centric perspective. Instead of asking whether one architecture outperforms another, the benchmark asks:

*Which robotic capabilities genuinely require predictive world representations, and what form of prediction is necessary to support them?*

The benchmark is designed around three principles and four capability domains.

### 3.1 Benchmark Design Principles

**Principle I: Capability Before Architecture.** Most contemporary evaluations compare architectures directly. Such comparisons implicitly assume that a single model family should dominate across all robotic tasks. ACTION-ATLAS rejects this assumption.

We hypothesize that different robotic competencies require different predictive mechanisms. Consequently, evaluation should be organized around capabilities rather than architectures.

Formally, let

$$c \in \mathcal{C}$$

denote a robotic capability and

$$f \in \{\text{VLA}, \text{LWM}, \text{WAM}, \text{WFM}\}$$

denote a model family. The objective is not to determine

$$\arg\max_f P(\text{success} \mid f)$$

thereby identifying which predictive mechanisms best support each capability.

**Principle II: Closed-Loop Evaluation.** Many predictive systems are evaluated through future prediction quality, latent consistency, reconstruction accuracy, or rollout realism. However, prediction quality alone does not guarantee improved behavior.

ACTION-ATLAS therefore evaluates models through closed-loop robotic execution.

$$\text{Prediction} \neq \text{Behavior}$$

A model that predicts realistic futures but selects poor actions should not be rewarded. Conversely, a model that acts successfully despite limited predictive ability should receive credit for effective control.

**Principle III: Behavioral Burden of Proof.** The burden of proof for world modeling is behavioral rather than generative.

A predictive representation is useful only if:

$$[\text{ Prediction} \rightarrow \text{Better Decisions }]$$

and ultimately

$$[\text{ Prediction} \rightarrow \text{Better Decisions} \rightarrow \text{Better Outcomes. }]$$

This principle underlies all metrics introduced later in the paper, including the proposed World Advantage Score (WAS).

### 3.2 Capability Domains

ACTION-ATLAS organizes predictive embodied intelligence into four capability domains. These domains were selected because they progressively increase the need for explicit predictive reasoning while remaining grounded in practical robotic deployment.

#### 3.2.1 Absent Objects

The first domain evaluates whether a system can reason about entities that are not directly observable.

Many real-world environments are partially observable. Objects may move behind obstacles, disappear from the field of view, or remain hidden for extended periods. Successful behavior therefore requires maintaining beliefs about hidden states.

The central question is:

*Can a robot reason about objects that it cannot currently see?*

Representative tasks include:

  (i) hidden-object retrieval,

  (ii) object permanence,

  (iii) occluded manipulation,

  (iv) delayed re-identification,

  (v) multi-room object search.

This domain primarily tests latent state maintenance and predictive memory, making it a natural target for LWM-style architectures.

#### 3.2.2 Counterfactual Futures

The second domain evaluates the ability to reason about futures that never actually occur.

Many robotic decisions require evaluating alternatives before execution. The robot must consider multiple possible actions and estimate their consequences.

The central question is:

*Can a robot evaluate alternative futures before acting?*

Representative tasks include:

  (i) route replanning,

  (ii) dynamic obstacle avoidance,

  (iii) alternative manipulation strategies,

  (iv) intervention planning,

  (v) recovery from execution failures.

These tasks naturally favor WAM-style systems capable of action-conditioned simulation.

#### 3.2.3 Temporal Coordination

The third domain evaluates the ability to coordinate behavior over extended horizons.

Many tasks require maintaining consistency across dozens or hundreds of actions while preserving intermediate goals and constraints.

The central question is:

*Can a robot coordinate behavior across long temporal horizons?*

Representative tasks include:

  (i) table preparation,

  (ii) kitchen organization,

  (iii) assembly procedures,

  (iv) warehouse fulfillment,

  (v) multi-stage delivery.

These tasks test planning depth, temporal abstraction, and cumulative error management.

#### 3.2.4 Interactive Others Navigation (ION)

The fourth domain evaluates reasoning about other agents.

Real environments contain pedestrians, vehicles, cyclists, animals, vendors, and other robots. Effective behavior requires anticipating their future actions.

The central question is:

*Can a robot predict and respond to the behavior of other agents?*

Representative tasks include:

  (i) pedestrian crossing,

  (ii) crowd navigation,

  (iii) multi-agent path planning,

  (iv) vehicle interaction,

  (v) animal-aware navigation.

ION represents the most demanding predictive domain because the future depends not only on physical dynamics but also on the behavior of other decision-making agents.

### 3.3 ACTION-ATLAS Task Matrix

Table 2 summarizes the capability structure of ACTION-ATLAS.

**Table 2: Capability structure of ACTION-ATLAS.** The four domains are designed to progressively increase the demand for predictive reasoning while isolating different forms of world understanding.

| Domain | Hidden State | Counterfactual | Long Horizon | Social Reasoning |
|---|---|---|---|---|
| Absent Objects | High | Low | Moderate | Low |
| Counterfactual Futures | Moderate | High | Moderate | Low |
| Temporal Coordination | Moderate | Moderate | High | Moderate |
| Interactive Others Navigation | High | High | High | High |

### 3.4 DenseWorld Stress Test

While existing robotics benchmarks predominantly evaluate robots in structured indoor environments, real-world deployment often occurs in crowded, dynamic, and partially observable settings.

To evaluate robustness under such conditions, ACTION-ATLAS includes a dedicated **DenseWorld** split.

DenseWorld contains:

  (i) crowded marketplaces,

  (ii) mixed traffic environments,

  (iii) buses and rickshaws,

  (iv) street vendors,

  (v) pedestrians,

  (vi) domestic animals,

  (vii) weather and lighting variation.

Unlike conventional robotics datasets, DenseWorld emphasizes uncertainty, interaction density, and long-range dependencies. The objective is not merely to measure task success but to expose predictive failures that remain hidden in highly structured environments.

### 3.5 Benchmark Outputs

Each ACTION-ATLAS task produces four categories of outputs:

  (i) **Action Outputs**: executed robot actions.

  (ii) **State Outputs**: predicted future states.

  (iii) **Trajectory Outputs**: predicted future rollouts.

  (iv) **Uncertainty Outputs**: confidence and calibration estimates.

These outputs enable unified evaluation across VLA, LWM, WAM, and WFM families and provide the foundation for the metrics introduced in the next section.

ACTION-ATLAS is therefore not a benchmark of prediction quality alone. It is a benchmark of **when prediction becomes behaviorally useful**.

## 4 Model Families and Evaluation Protocol

Having established the world-modeling hypothesis (Section 1), a taxonomy of predictive embodied intelligence (Section 2), and the capability-centric design of ACTION-ATLAS (Section 3), we now specify the model families evaluated in the benchmark.

The objective of ACTION-ATLAS is not to construct a leaderboard of individual systems. Rather, the goal is to compare representative instances of distinct predictive paradigms and quantify the relationship between predictive representations and embodied capabilities.

Accordingly, ACTION-ATLAS evaluates models at two levels:

  (i) **Model Level**: individual systems such as OpenVLA, V-JEPA2, DreamZero, or Cosmos.

  (ii) **Family Level**: broader predictive paradigms including Vision-Language-Action Models (VLAs), Latent World Models (LWMs), World Action Models (WAMs), and World Foundation Models (WFMs).

We define the family space as:

$$\mathcal{F} = \{\text{VLA}, \text{LWM}, \text{WAM}, \text{WFM}\}.$$

Similarly, the complete model space is:

$$\mathcal{M} = \mathcal{M}_{\text{VLA}} \cup \mathcal{M}_{\text{LWM}} \cup \mathcal{M}_{\text{WAM}} \cup \mathcal{M}_{\text{WFM}}.$$

The benchmark is therefore designed to answer two complementary questions:

  (i) Which individual systems perform best on a given capability?

  (ii) Which predictive paradigm is most effective for that capability?

### 4.1 Model Selection Criteria

Model selection follows four principles.

  (i) **Representative**: the model should be representative of a distinct predictive paradigm.

  (ii) **Influential**: the model should have significant impact on contemporary robotics research.

  (iii) **Reproducible**: sufficient public information should exist to enable evaluation.

  (iv) **Architecturally Distinct**: the model should contribute unique predictive mechanisms.

ACTION-ATLAS is intentionally extensible. Future VLA, LWM, WAM, and WFM systems can be incorporated without modifying the benchmark itself.

### 4.2 Vision-Language-Action Models

Vision-Language-Action models represent the dominant action-centric paradigm in modern robotics. These systems directly map observations and language instructions to executable robot actions.

Formally, a VLA policy is represented as

$$\pi_\theta : (o_{\leq t}, l) \to a_t,$$

or more generally

$$a_{t:t+H} \sim \pi_\theta(\cdot \mid o_{\leq t}, l),$$

where $H$ denotes the action horizon.

Unlike predictive world models, VLAs are optimized primarily for action generation rather than future simulation.

ACTION-ATLAS evaluates the following representative VLA systems:

  (i) RT-1 (Brohan et al., 2022)

  (ii) RT-2 (Brohan et al., 2023)

  (iii) Octo (Octo Model Team et al., 2024)

  (iv) OpenVLA (Kim et al., 2024)

  (v) $\pi_0$ (Black et al., 2024)

  (vi) GR00T N1 (Bjorck et al., 2025)

  (vii) Gemini Robotics (Gemini Robotics Team et al., 2025)

These systems collectively span transformer policies, vision-language-action transfer models, flow-based action generation, and humanoid foundation policies.

**Expected strengths.** VLAs are expected to perform strongly on:

  (i) manipulation,

  (ii) language grounding,

  (iii) instruction following,

  (iv) skill composition,

  (v) short-horizon control.

**Expected limitations.** VLAs may struggle with:

  (i) hidden-state reasoning,

  (ii) explicit uncertainty estimation,

  (iii) counterfactual planning,

  (iv) long-horizon coordination.

### 4.3 Latent World Models

Latent World Models learn predictive representations of future states without necessarily generating actions.

A generic LWM learns

$$z_t = f_\theta(o_{\leq t}).$$

and predicts

$$\hat{z}_{t+k} = g_\phi(z_t, k).$$

where $z_t$ denotes a latent representation of the current world state.

Unlike VLAs, LWMs focus on predictive state estimation rather than direct control.

ACTION-ATLAS evaluates:

  (i) I-JEPA (Assran et al., 2023)

  (ii) V-JEPA (?)

  (iii) V-JEPA2 (Assran et al., 2025)

These systems represent the most influential family of latent predictive architectures currently available.

**Expected strengths.** LWMs are expected to perform strongly on:

  (i) object permanence,

  (ii) hidden-state tracking,

  (iii) predictive memory,

  (iv) belief maintenance.

**Expected limitations.** LWMs generally require external policies for execution and therefore may underperform on tasks requiring direct action generation.

### 4.4 World Action Models

World Action Models couple future prediction with action generation.

Rather than predicting future representations alone, WAMs explicitly model action-conditioned futures:

$$\hat{s}_{t+1} = F_\theta(s_t, a_t).$$

or more generally

$$\hat{\tau}_{t:t+H} = F_\theta(s_t, a_{t:t+H}, l).$$

where $\hat{\tau}_{t:t+H}$ denotes a predicted future trajectory.

Actions are selected through future simulation:

$$a_{t:t+H}^\star = \arg\max_{a_{t:t+H}} U\big(F_\theta(s_t, a_{t:t+H}, l)\big).$$

where $U(\cdot)$ measures task utility.

ACTION-ATLAS currently evaluates:

  (i) DreamZero (Ye et al., 2026)

which represents the first large-scale demonstration that world action models can function as zero-shot robot policies.

**Expected strengths.** WAMs are expected to excel at:

  (i) counterfactual planning,

  (ii) long-horizon decision making,

  (iii) recovery from execution failures,

  (iv) action-conditioned reasoning.

**Expected limitations.** Potential challenges include:

  (i) rollout drift,

  (ii) simulation-reality mismatch,

  (iii) increased computational cost.

### 4.5 World Foundation Models

World Foundation Models represent the most ambitious form of predictive embodied intelligence.

A generic WFM models:

$$p_\theta(x_{t:t+H} \mid x_{\leq t}, c),$$

where $x$ may include observations, trajectories, object states, videos, actions, or multimodal context.

WFMs may serve several roles:

$$\text{Simulator}: \; p_\theta(x_{t:t+H} \mid x_{\leq t}, c), \qquad \text{Critic}: \; R_\theta(\tau, l), \qquad \text{Policy Backbone}: \; \pi_\theta(a_t \mid o_{\leq t}, l, \hat{x}_{t:t+H}).$$

ACTION-ATLAS evaluates the Cosmos family of World Foundation Models.

Unlike LWMs and WAMs, WFMs attempt to model broad world dynamics spanning multiple environments, agents, and interaction types.

**Expected strengths.** WFMs are expected to perform strongly on:

  (i) open-world forecasting,

  (ii) social reasoning,

  (iii) multi-agent prediction,

  (iv) transfer across environments.

**Expected limitations.** Potential challenges include:

  (i) embodiment mismatch,

  (ii) weak robot grounding,

  (iii) expensive inference.

### 4.6 Family-Level Comparison

Table 3 summarizes the model families evaluated in ACTION-ATLAS.

**Table 3: Representative model families evaluated in ACTION-ATLAS.** Models are selected to represent distinct predictive paradigms rather than to form an exhaustive leaderboard.

| Family | Representative Models | Primary Output | Predictive Mechanism |
|---|---|---|---|
| VLA | RT-1, RT-2, Octo, OpenVLA, $\pi_0$, GR00T, Gemini Robotics | Action | Direct Policy Prediction |
| LWM | I-JEPA, V-JEPA, V-JEPA2 | Latent State | Predictive Representation Learning |
| WAM | DreamZero | State–Action Trajectory | Action-Conditioned Future Simulation |
| WFM | Cosmos Family | World Trajectory | Generative World Simulation |

### 4.7 Cross-Family Evaluation Protocol

A major challenge in evaluating predictive embodied intelligence is that different model families produce fundamentally different outputs.

To unify evaluation, ACTION-ATLAS defines a common output space:

$$\mathcal{O} = \left\{ o^{(a)}, o^{(s)}, o^{(\tau)}, o^{(u)} \right\},$$

Whenever a model does not natively produce a required output, the benchmark attaches the minimal downstream module necessary to perform evaluation while preserving the model's original predictive mechanism.

For example:

  (i) LWMs receive lightweight policy heads for action execution.

  (ii) WFMs receive planning interfaces for trajectory generation.

  (iii) VLA systems receive rollout modules for trajectory prediction when required.

The goal is not to equalize architectures but to evaluate their predictive capabilities under a common protocol.

Formally, ACTION-ATLAS measures

$$P(\text{success} \mid c, m),$$

where

$$c \in \mathcal{C}$$

denotes a capability domain and

$$m \in \mathcal{M}$$

denotes a model.

Family-level performance is then computed as

$$P(\text{success} \mid c, f) = \frac{1}{|\mathcal{M}_f|} \sum_{m \in \mathcal{M}_f} P(\text{success} \mid c, m).$$

This formulation enables direct comparison between predictive paradigms while preserving architectural diversity. It also provides the foundation for the metrics and World Advantage Score introduced in the next section.

## 5 Metrics and the World Advantage Score

A central challenge in evaluating predictive embodied intelligence is that prediction quality and robotic performance are not equivalent. A model may accurately predict future observations yet fail to improve action selection. Conversely, a model may achieve strong task success without constructing explicit predictive representations.

Accordingly, ACTION-ATLAS distinguishes between **behavioral performance**, **predictive competence**, and **uncertainty calibration**. The proposed **World Advantage Score (WAS)** then measures the extent to which predictive mechanisms translate into measurable gains in embodied decision making.

### 5.1 Evaluation Philosophy

Existing evaluations frequently assume that improved future prediction implies improved robotic intelligence. However, this assumption is not necessarily valid.

$$\text{Prediction Quality} \not\equiv \text{Behavioral Utility}.$$

The objective of ACTION-ATLAS is therefore not to reward prediction for its own sake. Rather, the benchmark evaluates whether predictive representations improve robotic outcomes.

A useful predictive model should satisfy:

$$\text{Prediction} \to \text{Better Decisions} \to \text{Better Outcomes}.$$

This principle motivates the metric hierarchy introduced below.

### 5.2 Behavioral Metrics

Behavioral metrics quantify the robot's ability to accomplish tasks in closed-loop execution.

**Task Success Rate (TSR).** Task Success Rate measures the fraction of tasks completed successfully.

$$\text{TSR} = \frac{N_{\text{success}}}{N_{\text{total}}}.$$

TSR serves as the primary measure of practical robotic competence.

**Long-Horizon Completion Rate (LHCR).** Many ACTION-ATLAS tasks consist of multiple sequential subgoals.

$$\text{LHCR} = \frac{N_{\text{completed subgoals}}}{N_{\text{total subgoals}}}.$$

This metric is particularly important for Temporal Coordination tasks.

**Recovery Success Rate (RSR).** Recovery Success Rate evaluates the ability to recover after perturbations, failures, or unexpected events.

$$\text{RSR} = \frac{N_{\text{recovered}}}{N_{\text{failure events}}}.$$

This metric is especially relevant for Counterfactual Futures tasks.

**Safety Preservation Rate (SPR).** For navigation and interaction scenarios, we additionally measure the proportion of trajectories that satisfy safety constraints.

$$\text{SPR} = 1 - \frac{N_{\text{unsafe}}}{N_{\text{episodes}}}.$$

### 5.3 Predictive Metrics

Predictive metrics evaluate whether a model maintains useful representations of future world states.

**Hidden-State Localization Accuracy (HSLA).** HSLA measures whether a model correctly reasons about hidden entities.

$$\text{HSLA} = \frac{N_{\text{correct hidden state queries}}}{N_{\text{hidden state queries}}}.$$

This metric is central to the Absent Objects domain.

**Counterfactual Selection Accuracy (CSA).** CSA measures the frequency with which a model selects the best available future among competing alternatives.

$$\text{CSA} = \frac{N_{\text{optimal futures}}}{N_{\text{counterfactual trials}}}.$$

This metric directly evaluates the utility of future simulation.

**Future Rollout Error (FRE).** Future Rollout Error quantifies deviation between predicted and realized futures.

$$\text{FRE} = \frac{1}{T} \sum_{t=1}^{T} d(\hat{s}_t, s_t).$$

Here, $d(\cdot, \cdot)$ denotes a task-specific state distance.

**Action Consequence Prediction Error (ACPE).** ACPE evaluates whether a model correctly predicts the consequences of its own actions.

$$\text{ACPE} = \frac{1}{N} \sum_{i=1}^{N} d(\hat{o}_i, o_i).$$

This metric is particularly informative for WAM and WFM systems.

### 5.4 Calibration Metrics

Predictive models should not only be accurate; they should also know when they are uncertain.

**Expected Calibration Error (ECE).** We measure calibration using Expected Calibration Error.

$$\text{ECE} = \sum_{b=1}^{B} \frac{|B_b|}{N} \left| \text{acc}(B_b) - \text{conf}(B_b) \right|.$$

Lower values indicate better calibration.

**Risk-Calibrated Success (RCS).** We combine task success and calibration into a single metric.

$$\text{RCS} = \frac{\text{TSR}}{1 + \text{ECE}}.$$

A model that succeeds frequently but remains poorly calibrated is therefore penalized.

### 5.5 Capability Scores

Each ACTION-ATLAS domain contains multiple tasks and metrics. We therefore aggregate measurements into capability-specific scores.

Let the capability space be:

$$\mathcal{C} = \{\mathcal{C}_{\text{Absent}}, \mathcal{C}_{\text{Counterfactual}}, \mathcal{C}_{\text{Temporal}}, \mathcal{C}_{\text{ION}}\}.$$

For a model $m$ and capability $c$, the capability score is defined as:

$$S(c, m) = \sum_{j=1}^{K} w_j M_j(c, m).$$

Here, $M_j(c, m)$ denotes the $j$-th normalized metric for model $m$ on capability $c$, and $w_j$ denotes its weight. The weights satisfy:

$$\sum_{j=1}^{K} w_j = 1.$$

This formulation allows different capability domains to emphasize different metrics while maintaining a common scale.

**Table 4: Interpretation of the World Advantage Score.** Positive values indicate that predictive representations improve capability-level performance relative to the reference VLA baseline.

| WAS | Interpretation |
|---|---|
| $> 0$ | Prediction provides advantage |
| $= 0$ | No measurable advantage |
| $< 0$ | Prediction hurts performance |

### 5.6 World Advantage Score

We now introduce the central metric of ACTION-ATLAS.

The purpose of the World Advantage Score is to quantify whether predictive world representations provide measurable benefits relative to direct action prediction.

Let $m_{\text{VLA}}$ denote a reference VLA baseline. The World Advantage Score for model $m$ on capability $c$ is defined as:

$$\text{WAS}(c, m) = \frac{S(c, m) - S(c, m_{\text{VLA}})}{S(c, m_{\text{VLA}}) + \epsilon}.$$

Here, $\epsilon$ is a small constant used for numerical stability.

Interpretation is straightforward:

Importantly, WAS does not reward prediction directly. Instead, it rewards improvements in capability-level performance attributable to predictive mechanisms.

### 5.7 Family-Level World Advantage

Individual models may exhibit substantial variance. To compare predictive paradigms, we therefore define a family-level World Advantage Score.

For a family $f \in \mathcal{F}$, the family-level score is:

$$\text{WAS}(c, f) = \frac{1}{|\mathcal{M}_f|} \sum_{m \in \mathcal{M}_f} \text{WAS}(c, m).$$

This quantity answers the central scientific question of ACTION-ATLAS:

*Which predictive paradigm provides the greatest advantage for a given robotic capability?*

### 5.8 Statistical Significance

All reported scores are accompanied by confidence intervals computed using bootstrap resampling.

For two model families $f_1$ and $f_2$, the capability difference is:

$$\Delta(c) = \text{WAS}(c, f_1) - \text{WAS}(c, f_2).$$

We report:

  (i) mean performance,

  (ii) 95% confidence intervals,

  (iii) paired significance tests,

  (iv) effect sizes.

This enables rigorous comparison between predictive paradigms and ensures that observed differences are statistically meaningful rather than artifacts of task selection.

In summary, ACTION-ATLAS moves beyond task success alone and introduces a capability-centric evaluation framework for predictive embodied intelligence. The World Advantage Score provides a direct quantitative answer to the question that motivates this paper: *when does world modeling become behaviorally useful?*

**Table 5: ACTION-ATLAS capability domains and representative task categories.** Each domain is designed to isolate a distinct form of predictive embodied intelligence.

| Capability Domain | Representative Tasks | Primary Capability Tested |
|---|---|---|
| Absent Objects | Object Permanence, Occluded Retrieval, Delayed Re-Identification, Multi-Room Search | Hidden-State Reasoning |
| Counterfactual Futures | Route Replanning, Alternative Manipulation, Intervention Planning, Failure Recovery | Counterfactual Evaluation |
| Temporal Coordination | Assembly, Table Preparation, Warehouse Fulfillment, Multi-Stage Delivery | Long-Horizon Planning |
| Interactive Others Navigation | Crowd Navigation, Pedestrian Interaction, Vehicle Interaction, Animal Interaction | Social Forecasting |

## 6 Experimental Evaluation and Analysis

Having established the capability-centric evaluation framework and the World Advantage Score (WAS), we now describe the experimental protocol used to compare Vision-Language-Action Models (VLAs), Latent World Models (LWMs), World Action Models (WAMs), and World Foundation Models (WFMs) within ACTION-ATLAS.

The objective of the evaluation is not merely to identify the highest-performing model. Rather, the objective is to determine which predictive paradigm provides the greatest advantage for each robotic capability domain.

### 6.1 Experimental Setup

All models are evaluated under a unified protocol designed to isolate the contribution of predictive representations.

Let

$$\mathcal{C} = \{\mathcal{C}_{\text{Absent}}, \mathcal{C}_{\text{Counterfactual}}, \mathcal{C}_{\text{Temporal}}, \mathcal{C}_{\text{ION}}\}.$$

denote the four capability domains introduced in Section 3.

Similarly, let

$$\mathcal{F} = \{\text{VLA}, \text{LWM}, \text{WAM}, \text{WFM}\}.$$

denote the model-family space.

For every model-family pair, evaluation is conducted using:

  (i) identical task specifications,

  (ii) identical observation streams,

  (iii) identical evaluation horizons,

  (iv) identical success criteria,

  (v) identical metric definitions.

This ensures that performance differences arise from predictive capabilities rather than evaluation artifacts.

### 6.2 Benchmark Composition

ACTION-ATLAS consists of four capability domains and sixteen representative task categories.

Each task category contains multiple task instances with varying levels of environmental complexity, uncertainty, and interaction density.

### 6.3 Evaluation Horizon

Different robotic capabilities require different planning horizons.

Let

$$H$$

denote the evaluation horizon measured in decision steps.

ACTION-ATLAS evaluates three horizon regimes:

  (i) **Short Horizon** ($H \leq 10$),

  (ii) **Medium Horizon** ($10 < H \leq 50$),

  (iii) **Long Horizon** ($H > 50$).

This enables direct analysis of how predictive representations scale with temporal complexity.

### 6.4 Overall Benchmark Performance

For every model $m$, we report:

  (i) Task Success Rate (TSR),

  (ii) Long-Horizon Completion Rate (LHCR),

  (iii) Recovery Success Rate (RSR),

  (iv) Safety Preservation Rate (SPR),

  (v) World Advantage Score (WAS).

Overall benchmark performance is computed as:

$$S_{\text{overall}}(m) = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} S(c, m).$$

This quantity summarizes capability-level performance across all benchmark domains.

### 6.5 Capability-Level Analysis

While aggregate performance is informative, the primary objective of ACTION-ATLAS is capability-specific analysis.

For every capability domain, we compute:

$$S(c, f) = \frac{1}{|\mathcal{M}_f|} \sum_{m \in \mathcal{M}_f} S(c, m).$$

where

$$f \in \mathcal{F}.$$

This enables direct comparison between predictive paradigms.

The resulting capability matrix takes the form shown in Table 6.

**Table 6: Capability-level evaluation matrix.** Cells report capability scores aggregated across all tasks belonging to a given domain.

| Family | Absent Objects | Counterfactual Futures | Temporal Coordination | ION |
|---|---|---|---|---|
| VLA | – | – | – | – |
| LWM | – | – | – | – |
| WAM | – | – | – | – |
| WFM | – | – | – | – |

### 6.6 Prediction Quality versus Behavioral Utility

A central hypothesis of this paper is that future prediction quality alone is insufficient for embodied intelligence.

To test this hypothesis, ACTION-ATLAS evaluates the relationship between predictive metrics and behavioral metrics.

For each model:

$$\rho = \text{corr}\big(S_{\text{predictive}}, S_{\text{behavioral}}\big).$$

where

$$S_{\text{predictive}}$$

denotes aggregate predictive performance and

$$S_{\text{behavioral}}$$

denotes aggregate behavioral performance.

If prediction alone is sufficient, we expect strong positive correlation. If predictive competence and behavioral utility diverge, this correlation should weaken.

### 6.7 DenseWorld Stress Test

Most existing robotics benchmarks evaluate systems in relatively structured environments.

ACTION-ATLAS introduces a dedicated DenseWorld evaluation split to measure performance under high-density, high-uncertainty conditions.

The DenseWorld split includes:

  (i) crowded marketplaces,

  (ii) mixed traffic environments,

  (iii) buses and rickshaws,

  (iv) street vendors,

  (v) domestic animals,

  (vi) dynamic pedestrian flows,

  (vii) weather variation,

  (viii) lighting variation.

These environments contain substantially higher interaction complexity than conventional robotics benchmarks.

For every model, DenseWorld degradation is computed as:

$$D_{\text{Dense}} = \frac{S_{\text{standard}} - S_{\text{Dense}}}{S_{\text{standard}}}.$$

Lower values indicate greater robustness under dense-world conditions.

### 6.8 World Advantage Analysis

The primary analysis performed by ACTION-ATLAS is based on the World Advantage Score.

For every capability domain and model family, we compute:

$$\text{WAS}(c, f) = \frac{1}{|\mathcal{M}_f|} \sum_{m \in \mathcal{M}_f} \text{WAS}(c, m).$$

This allows the benchmark to answer the central question motivating this work:

*Which robotic capabilities genuinely benefit from predictive world representations, and which predictive paradigm provides the largest advantage?*

Unlike traditional leaderboards, ACTION-ATLAS therefore evaluates not only who performs best, but also *why* performance improves.

### 6.9 Statistical Evaluation

All reported metrics are accompanied by confidence intervals obtained through bootstrap resampling.

For two model families $f_1$ and $f_2$, the capability-level difference is:

$$\Delta(c) = S(c, f_1) - S(c, f_2).$$

For every comparison we report:

  (i) mean performance,

  (ii) standard deviation,

  (iii) 95

  (iv) paired significance tests,

  (v) effect sizes.

This enables rigorous comparison between predictive paradigms and prevents conclusions from being driven by individual tasks or environments.

### 6.10 Visualization and Reporting

ACTION-ATLAS reports results at three complementary levels:

  (i) **Model Level**: comparison of individual systems.

  (ii) **Family Level**: comparison of predictive paradigms.

  (iii) **Capability Level**: comparison of robotic competencies.

The primary visualization is a capability radar plot spanning:

  (i) Absent Objects,

  (ii) Counterfactual Futures,

  (iii) Temporal Coordination,

  (iv) Interactive Others Navigation.

This representation provides an intuitive view of where each predictive paradigm succeeds and where it fails.

In summary, the experimental protocol is designed to move beyond aggregate task success and provide a capability-centric understanding of predictive embodied intelligence. The resulting analyses enable direct evaluation of the world-modeling hypothesis and establish a quantitative framework for determining when predictive representations become behaviorally useful.

## 7 What Must World Models Actually Do?

The central motivation of ACTION-ATLAS is that the current debate surrounding Vision-Language-Action Models (VLAs), Latent World Models (LWMs), World Action Models (WAMs), and World Foundation Models (WFMs) is often framed as a competition between architectures. Such framing is misleading. The scientific question is not whether one architecture universally dominates another, but rather which robotic capabilities require which predictive mechanisms.

We therefore reinterpret the world-modeling debate as a hierarchy of capability requirements. ACTION-ATLAS is designed to test a series of capability hypotheses regarding when predictive representations become behaviorally useful and what forms of prediction are necessary to support increasingly complex robotic competencies.

### 7.1 Finding I: Action Prediction Remains Surprisingly Strong

A common assumption in recent robotics discourse is that explicit world modeling will inevitably replace action-centric policies. However, decades of robotics research suggest that many embodied tasks can be solved effectively through direct observation-to-action mappings.

Modern VLAs such as RT-2, OpenVLA, $\pi_0$, GR00T, and Gemini Robotics demonstrate that large-scale multimodal policies can acquire substantial embodied competence without explicitly simulating future world states. For many short-horizon manipulation and navigation tasks, action selection appears to depend primarily on local observations and instruction grounding.

This observation motivates the first capability hypothesis:

$$\mathcal{C}_{\text{short}} \to \text{VLA}.$$

In other words, short-horizon embodied competence may emerge from sufficiently large and diverse policy learning alone. If this hypothesis holds, explicit predictive world models should provide only marginal gains on tasks dominated by immediate perception and action.

The implication is important: world modeling should not be treated as a prerequisite for all forms of robotic intelligence. Instead, its value must be demonstrated through capabilities that cannot be obtained from reactive policies alone.

### 7.2 Finding II: Hidden-State Reasoning Creates the First Need for Prediction

The limitations of purely reactive policies become apparent when the environment is only partially observable.

Objects frequently move behind obstacles, leave the robot's field of view, or remain hidden for extended periods. Successful behavior therefore requires maintaining beliefs about states that cannot be directly observed.

The Absent Objects domain is specifically designed to probe this requirement.

We hypothesize that:

$$\mathcal{C}_{\text{hidden}} \to \text{LWM}.$$

This hypothesis reflects the intuition that latent predictive representations provide a natural mechanism for maintaining hidden-state information over time.

Unlike VLAs, which primarily optimize action generation, LWMs explicitly learn predictive latent representations capable of preserving information beyond the current observation window. Consequently, we expect latent world models to exhibit measurable advantages on tasks involving object permanence, delayed retrieval, occlusion reasoning, and long-term belief maintenance.

Importantly, this does not imply that latent prediction is universally superior. Rather, it suggests that hidden-state reasoning represents the first capability regime in which predictive representations become behaviorally valuable.

### 7.3 Finding III: Counterfactual Reasoning Requires Executable Futures

Many robotic decisions require evaluating futures before acting.

Consider a robot navigating around obstacles, selecting a manipulation strategy, or recovering from execution failure. In each case, the robot must estimate the consequences of multiple possible actions and select among competing futures.

This capability differs fundamentally from hidden-state reasoning. Maintaining beliefs about the present is not sufficient. The robot must evaluate futures that have not yet occurred.

This motivates the third capability hypothesis:

$$\mathcal{C}_{\text{counterfactual}} \to \text{WAM}.$$

World Action Models are uniquely positioned to support this capability because they explicitly model action-conditioned futures.

A generic WAM computes:

$$\hat{\tau}_{t:t+H} = F_\theta(s_t, a_{t:t+H}, l),$$

allowing future trajectories to be evaluated before execution.

Action selection then becomes:

$$a_{t:t+H}^\star = \arg\max_{a_{t:t+H}} U\big(\hat{\tau}_{t:t+H}\big).$$

This capability is difficult to obtain from direct action prediction alone because it requires explicit comparison between alternative futures.

If ACTION-ATLAS confirms this hypothesis, it would provide evidence that executable future simulation represents a distinct computational advantage rather than a different implementation of policy learning.

### 7.4 Finding IV: Social Intelligence Requires World Simulation

The most challenging environments are not merely physical. They are social.

Pedestrians change direction unexpectedly. Vehicles negotiate implicit right-of-way rules. Crowds exhibit collective dynamics. Animals behave unpredictably. Human intentions influence future outcomes.

These settings require prediction not only of physical dynamics but also of other decision-making agents.

This motivates the fourth capability hypothesis:

$$\mathcal{C}_{\text{social}} \to \text{WFM}.$$

World Foundation Models attempt to capture broad multimodal regularities spanning environments, agents, interactions, and behaviors. Unlike task-specific world models, they are designed to support open-world forecasting across diverse scenarios.

The Interactive Others Navigation domain therefore serves as a critical test of whether large-scale world simulation yields measurable advantages in socially complex environments.

If confirmed, this finding would suggest that the value of world models increases as the future becomes increasingly dependent on other intelligent agents.

### 7.5 Finding V: Prediction Quality Is Not Behavioral Utility

Perhaps the most important hypothesis tested by ACTION-ATLAS concerns the relationship between prediction and behavior.

Current evaluations often assume that more accurate future prediction necessarily implies better robotic intelligence. However, this assumption remains largely untested.

A model may generate visually plausible futures while still making poor decisions. Conversely, a model may exhibit strong task performance without constructing highly accurate predictive representations.

This motivates the final capability hypothesis:

$$\text{Prediction} \not\Rightarrow \text{Capability}.$$

The distinction between predictive competence and behavioral utility is precisely why ACTION-ATLAS introduces the World Advantage Score.

A world model should not be considered successful merely because it predicts the future accurately. It should be considered successful only when those predictions improve embodied outcomes.

### 7.6 The Capability Hierarchy Hypothesis

Taken together, the preceding findings suggest a broader organizational principle for predictive embodied intelligence.

Rather than viewing VLAs, LWMs, WAMs, and WFMs as competing architectures, we propose that they occupy different regions of a capability hierarchy.

$$\mathcal{C}_{\text{short}} \to \text{VLA},$$

$$\mathcal{C}_{\text{hidden}} \to \text{LWM},$$

$$\mathcal{C}_{\text{counterfactual}} \to \text{WAM},$$

$$\mathcal{C}_{\text{social}} \to \text{WFM}.$$

These relationships should not be interpreted as rigid boundaries. Rather, they represent hypotheses regarding the minimum predictive mechanisms required for different classes of robotic competencies.

The resulting picture is fundamentally different from the common narrative that world models will simply replace VLAs. Instead, ACTION-ATLAS suggests that predictive representations become progressively more valuable as tasks move from reactive control toward hidden-state reasoning, counterfactual planning, and social forecasting.

In this view, the future of robotics is unlikely to be characterized by the disappearance of action-centric policies. Rather, it will be characterized by the emergence of increasingly sophisticated predictive mechanisms layered on top of them.

The central question is therefore not whether world models outperform VLAs. The central question is: *which robotic capabilities genuinely require predictive world representations, and what form of prediction is necessary to support them?*

## References

- Mahmoud Assran, Quentin Duval, Ishan Misra, et al. 2023. Self-supervised learning from images with a joint-embedding predictive architecture. *arXiv preprint arXiv:2301.08243*.
- Mido Assran, Adrien Bardes, David Fan, et al. 2025. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. *arXiv preprint arXiv:2506.09985*.
- Johan Bjorck, Fernando Casta neda, Nikita Cherniadev, et al. 2025. Gr00t n1: An open foundation model for generalist humanoid robots. *arXiv preprint arXiv:2503.14734*.
- Kevin Black, Noah Brown, Danny Driess, et al. 2024. $\pi_0$: A vision-language-action flow model for general robot control. *arXiv preprint arXiv:2410.24164*.
- Anthony Brohan, Noah Brown, Justice Carbajal, et al. 2022. Rt-1: Robotics transformer for real-world control at scale. *arXiv preprint arXiv:2212.06817*.
- Anthony Brohan, Yevgen Chebotar, Chelsea Finn, et al. 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. *arXiv preprint arXiv:2307.15818*.
- Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, et al. 2025. Gemini robotics: Bringing ai into the physical world. *arXiv preprint arXiv:2503.20020*.
- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al. 2024. Openvla: An open-source vision-language-action model. *arXiv preprint arXiv:2406.09246*.
- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, et al. 2024. Octo: An open-source generalist robot policy. *arXiv preprint arXiv:2405.12213*.
- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, et al. 2026. World action models are zero-shot policies. *arXiv preprint arXiv:2602.15922*.

