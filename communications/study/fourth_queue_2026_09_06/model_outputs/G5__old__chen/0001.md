## Analysis

### Scope and counting rules

The corpus contains one focal article—Yang Chen’s 2025 critique—and 45 referenced works. The network is therefore a **one-document ego network**, not a field-wide citation graph. All 45 observed citation edges run from Chen’s article to a referenced work; references made by those works are unavailable. “Citation count” below means the number of citing works in this corpus, not global citation impact. Most cited sources consequently tie at one incoming work, although Jaeggi (2023) and Kuhn (1970) are clearly the principal **textual authorities** because they recur across the article and structure its central dispute.

Chen’s article has three citation layers:

1. **Target theory:** Jaeggi’s works, especially *Fortschritt und Regression*, supply the position reconstructed and criticized.
2. **Counter-framework:** Kuhn’s works supply incommensurability, paradigm change, scientific communities, and the route to Chen’s psychologist alternative.
3. **Supporting traditions:** Kitcher, Dewey, Roth, Lakatos, Allen, Searle, Giddens, Honneth, Singer, and others provide subsidiary models, objections, examples, or conceptual tools.

The article explicitly characterizes its argument as a challenge to Jaeggi’s analogy: “Jaeggi’s pragmatism is based on a defected parallelism of social-moral and scientific progress.” Kuhn is the principal connecting authority because Chen uses him both to criticize cumulative progress and to construct the alternative: “Inspired by Kuhn’s discovery of the community-based character of scientific research, I argue that the alternative understanding … is the psychologist pattern.”

---

## Citation-network schema

### Works

Bibliographic metadata is transcribed from the supplied reference list. For every external work, `citation_count = 1` and `reference_count = 0` because it is cited by the sole in-corpus article but its own bibliography is not supplied.

| ID | Work |
|---|---|
| W00 | **Yang Chen (2025), “The progress without ‘progress’: Critique of Jaeggi’s pragmatist theory of progress,” European Journal of Social Theory, article.** In corpus: true; citation count: 0; observed reference count: 45. |
| W01 | Amy Allen (2016), *The End of Progress: Decolonizing the Normative Foundations of Critical Theory*, Columbia University Press, book. |
| W02 | Amy Allen, Rahel Jaeggi, and Eva von Redecker (2016), “Progress, normativity, and the dynamics of social change,” *Graduate Faculty Philosophy Journal*, article. |
| W03 | Elizabeth Anderson (2014), *Social Movements, Experiments in Living, and Moral Progress*, University of Kansas, report/lecture. |
| W04 | Aristotle (1998), *Politics*, Hackett, book. |
| W05 | Aristotle (2009), *The Nicomachean Ethics*, Oxford University Press, book. |
| W06 | E. Bodde (2020), “The Lebensform as organism,” *Philosophy & Social Criticism*, article. |
| W07 | Yang Chen (2024), *The Genesis and Transformation of Social Consciousness*, Palgrave Macmillan, book. |
| W08 | Joshua Cohen (1997), “The arc of the moral universe,” *Philosophy & Public Affairs*, article. |
| W09 | G. A. Cohen (2000), *If You’re an Egalitarian, How Come You’re So Rich?*, Harvard University Press, book. |
| W10 | G. A. Cohen (2001), *Karl Marx’s Theory of History: A Defence*, Princeton University Press, book. |
| W11 | John Dewey (1997), *Experience and Education*, Touchstone, book. |
| W12 | Pierre Duhem (1954), *The Aim and Structure of Physical Theory*, Princeton University Press, book. |
| W13 | Rainer Forst (2017), *Normativity and Power*, Oxford University Press, book. |
| W14 | Rainer Forst (2020), “Gesellschaftlicher Zusammenhalt,” in *Gesellschaftlicher Zusammenhalt*, chapter. |
| W15 | Anthony Giddens (1990), *The Consequences of Modernity*, Polity, book. |
| W16 | Anthony Giddens (1991), *Modernity and Self-Identity*, Polity, book. |
| W17 | Jürgen Habermas (1973), “What does a crisis mean today?”, *Social Research*, article. |
| W18 | Jonathan Haidt (2012), *The Righteous Mind*, Penguin, book. |
| W19 | G. W. F. Hegel (2011), *Lectures on the Philosophy of World History, Volume I*, Oxford University Press, book. |
| W20 | Axel Honneth (2002), “Grounding recognition,” *Inquiry*, article. |
| W21 | Axel Honneth (2009), *Pathologies of Reason*, Columbia University Press, book. |
| W22 | Axel Honneth (2015), “Rejoinder,” *Critical Horizons*, article. |
| W23 | Rahel Jaeggi (2018a), *Critique of Forms of Life*, Harvard University Press, book. |
| W24 | Rahel Jaeggi (2018b), “Resistance to the perpetual danger of relapse,” in *From Alienation to Forms of Life*, chapter. |
| W25 | Rahel Jaeggi (2021), “Progress as the dynamics of crisis,” in *Moral Progress*, chapter. |
| W26 | Rahel Jaeggi (2023), *Fortschritt und Regression*, Suhrkamp, book. |
| W27 | Andrea Kern (2017), *Sources of Knowledge*, Harvard University Press, book. |
| W28 | Philip Kitcher (2011), *The Ethical Project*, Harvard University Press, book. |
| W29 | Philip Kitcher (2021), *Moral Progress*, Oxford University Press, book. |
| W30 | Thomas Kuhn (1970), *The Structure of Scientific Revolutions*, University of Chicago Press, book. |
| W31 | Thomas Kuhn (1977), *The Essential Tension*, University of Chicago Press, book. |
| W32 | Thomas Kuhn (2024), “Does Knowledge ‘Grow’?”, in *Rethinking Thomas Kuhn’s Legacy*, chapter. |
| W33 | Jouni-Matti Kuukkanen (2024), “Kuhn, progress, and knowing-how,” in *Rethinking Thomas Kuhn’s Legacy*, chapter. |
| W34 | Imre Lakatos (1980), *The Methodology of Scientific Research Programmes*, Cambridge University Press, book. |
| W35 | Charles Larmore (2004), “History & truth,” *Daedalus*, article. |
| W36 | Larry Laudan (1978), *Progress and Its Problems*, University of California Press, book. |
| W37 | Karl Marx and Friedrich Engels (1976), “Manifesto of the Communist Party,” in *MECW*, chapter. |
| W38 | Michele Moody-Adams (2016), “Moral progress and human agency,” *Ethical Theory and Moral Practice*, article. |
| W39 | Terry Pinkard (2017), *Does History Make Sense?*, Harvard University Press, book. |
| W40 | Amanda Roth (2012), “Ethical progress as problem-resolving,” *Journal of Political Philosophy*, article. |
| W41 | John Searle (1995), *The Construction of Social Reality*, Penguin, book. |
| W42 | John Searle (2010), *Making the Social World*, Oxford University Press, book. |
| W43 | Peter Singer (2011), *The Expanding Circle*, Princeton University Press, book. |
| W44 | Michael Thompson (2001), “Two forms of practical generality,” in *Practical Rationality and Preference*, chapter. |
| W45 | Albrecht Wellmer (1991), *The Persistence of Modernity*, Polity, book. |

All W01–W45 have: `in_corpus = false`, `citation_count = 1`, and corpus-observed `reference_count = 0`.

---

### Citations

The table records the analytically consequential citation instances. All have W00 as the citing work. Importance estimates how necessary the citation is to Chen’s argument, not the source’s general scholarly prestige.

| Citation ID | Cited work | Context | Location | Importance | Citation text |
|---|---|---|---|---:|---|
| C01 | W21 Honneth 2009 | background | introduction | 0.45 | “recovering from the idea of a social pathology of reason an explosive charge” |
| C02 | W26 Jaeggi 2023 | background | introduction | 1.00 | “progress is an accumulating process, while regression is a systematically blocked process” |
| C03 | W03 Anderson 2014 | background | literature review | 0.35 | “the expansion of the moral circle can be represented by the constant bias-correction” |
| C04 | W43 Singer 2011 | supporting | literature review | 0.55 | “reason leads us to develop and expand our moral concerns” |
| C05 | W24 Jaeggi 2018b | supporting | literature review | 0.75 | “our understanding of what it means to be a human being or a person has changed” |
| C06 | W13 Forst 2017 | critical | literature review | 0.50 | “every progressive process must be constantly questioned” |
| C07 | W22 Honneth 2015 | background | literature review | 0.55 | “what we now must do in order to realize them more fully and adequately” |
| C08 | W37 Marx–Engels 1976 | background | literature review | 0.35 | “within the old society, the elements of a new one have been created” |
| C09 | W09 G. A. Cohen 2000 | critical | literature review | 0.50 | “Scientific socialism offers no ideals or values to the proletariat” |
| C10 | W19 Hegel 2011 | background | literature review | 0.40 | “human history means a process of self-comprehension of the ‘freedom’ spirit” |
| C11 | W39 Pinkard 2017 | background | literature review | 0.40 | “Such an end is not one for which the other ends are simply means” |
| C12 | W10 G. A. Cohen 2001 | background | literature review | 0.35 | “The arrival of profound but profoundly compatible needs signifies history’s end” |
| C13 | W29 Kitcher 2021 | methodological | literature review | 0.80 | “Pragmatic progress consists in solving problems and overcoming limitations” |
| C14 | W28 Kitcher 2011 | background | literature review | 0.55 | “morality plays a functional role in overcoming the problems and difficulties” |
| C15 | W25 Jaeggi 2021 | supporting | literature review | 0.75 | “identifying problems in the realm of the social is not as easy as discovering engine damage” |
| C16 | W23 Jaeggi 2018a | methodological | literature review | 0.85 | “sharing the interpretations—but above all the schemata of interpretation” |
| C17 | W06 Bodde 2020 | background | literature review | 0.25 | “forms of life are both ‘spiritual’ and ‘material’” |
| C18 | W11 Dewey 1997 | methodological | literature review | 0.85 | “any experience is mis-educative that has the effect of arresting or distorting” |
| C19 | W30 Kuhn 1970 | methodological | discussion | 1.00 | “in both political and scientific development the sense of malfunction … is prerequisite to revolution” |
| C20 | W30 Kuhn 1970 | critical | discussion | 1.00 | “there is incommensurability between different paradigms” |
| C21 | W32 Kuhn 2024 | supporting | discussion | 0.80 | “if … we take a purely instrumental view of knowledge – then knowledge clearly does grow” |
| C22 | W33 Kuukkanen 2024 | supporting | discussion | 0.70 | “an embodied skill distributed among the members of a scientific community” |
| C23 | W31 Kuhn 1977 | supporting | discussion | 0.75 | “the solution of a difficult conceptual or instrumental puzzle is a principal goal” |
| C24 | W40 Roth 2012 | critical | discussion | 0.75 | “a real solution … only if it does not create more serious or intractable problems” |
| C25 | W16 Giddens 1991 | critical | discussion | 0.65 | “Childhood became concealed and domesticated” |
| C26 | W15 Giddens 1990 | background | discussion | 0.40 | “the ‘lifting out’ of local social relations” |
| C27 | W34 Lakatos 1980 | critical | discussion | 0.70 | “falls totally within the realm of the (social) psychology of discovery” |
| C28 | W07 Chen 2024 | supporting | discussion | 0.65 | “We can achieve scientific progress without presuming any rational law of progress” |
| C29 | W45 Wellmer 1991 | methodological | discussion | 0.70 | “‘right’ would denote that which can justifiably be demanded” |
| C30 | W41 Searle 1995 | methodological | discussion | 0.75 | “X counts as Y in context C” |
| C31 | W42 Searle 2010 | methodological | discussion | 0.75 | “social facts are essentially intentionality-relative” |
| C32 | W01 Allen 2016 | critical | discussion | 0.90 | “our politics cannot be truly progressive unless we have some way of conceptualizing what would count as progress” |
| C33 | W02 Allen–Jaeggi–von Redecker 2016 | supporting | discussion | 0.80 | “giving up on the notion of progress on a meta-normative level” |
| C34 | W36 Laudan 1978 | critical | discussion | 0.55 | “Laudan rejects Kuhn’s discontinuous version of scientific revolution” |
| C35 | W17 Habermas 1973 | background | literature review | 0.30 | “the relation between crisis and decision-making” |
| C36 | W18 Haidt 2012 | background | literature review | 0.25 | “the advantage of conservative morality” |
| C37 | W04 Aristotle 1998 | background | literature review | 0.20 | “man is a political animal” |
| C38 | W05 Aristotle 2009 | background | literature review | 0.20 | “man is a rational animal” |
| C39 | W12 Duhem 1954 | background | discussion | 0.25 | “the theory-ladenness of science” |
| C40 | W20 Honneth 2002 | background | literature review | 0.30 | “Honneth’s method of normative reconstruction is still in the strong Hegelian fashion” |
| C41 | W27 Kern 2017 | background | discussion | 0.20 | “the analysis of human capacity” |
| C42 | W44 Thompson 2001 | background | discussion | 0.20 | “the analysis of human capacity” |
| C43 | W35 Larmore 2004 | supporting | discussion | 0.25 | “A similar argument can also be found in Larmore” |
| C44 | W38 Moody-Adams 2016 | background | literature review | 0.25 | “moralist understandings of progress” |
| C45 | W14 Forst 2020 | background | literature review | 0.20 | “different notions of toleration” |

---

### Citation clusters

```text
[
  {
    "cluster_id": "CL1",
    "cluster_name": "Jaeggi and pragmatist progress",
    "theme": "Progress as problem-solving, crisis response, and enrichment of experience",
    "member_works": ["W23", "W24", "W25", "W26", "W28", "W29", "W11", "W36", "W40"],
    "internal_density": 0.31,
    "key_connecting_works": ["W26", "W29", "W11"]
  },
  {
    "cluster_id": "CL2",
    "cluster_name": "Kuhn and scientific change",
    "theme": "Paradigms, incommensurability, puzzle-solving, community choice, and know-how",
    "member_works": ["W30", "W31", "W32", "W33", "W34", "W36", "W12"],
    "internal_density": 0.38,
    "key_connecting_works": ["W30", "W32", "W33"]
  },
  {
    "cluster_id": "CL3",
    "cluster_name": "Moral progress",
    "theme": "Expansion, deepening, agency, normativity, and abolition",
    "member_works": ["W03", "W08", "W13", "W22", "W24", "W38", "W43"],
    "internal_density": 0.22,
    "key_connecting_works": ["W24", "W43", "W13"]
  },
  {
    "cluster_id": "CL4",
    "cluster_name": "Historicism and critical theory",
    "theme": "Teleology, dialectical development, social pathology, and historical necessity",
    "member_works": ["W09", "W10", "W19", "W20", "W21", "W22", "W37", "W39"],
    "internal_density": 0.24,
    "key_connecting_works": ["W21", "W22", "W19"]
  },
  {
    "cluster_id": "CL5",
    "cluster_name": "Social construction and collective intentionality",
    "theme": "Psychologist progress, normative judgment, and intentionality-relative social facts",
    "member_works": ["W01", "W02", "W07", "W35", "W41", "W42", "W45"],
    "internal_density": 0.29,
    "key_connecting_works": ["W01", "W41", "W42"]
  },
  {
    "cluster_id": "CL6",
    "cluster_name": "Modernity and experiential loss",
    "theme": "Disembedding, sequestration of experience, crisis, and conservative responses",
    "member_works": ["W15", "W16", "W17", "W18"],
    "internal_density": 0.17,
    "key_connecting_works": ["W16"]
  }
]
```

Density values are interpretive estimates based on explicit cross-references in Chen’s discussion, not complete bibliographic links among the external works.

---

### Hub works

| Work | Hub score | Cited-by count | Influence breadth |
|---|---:|---:|---|
| W26 Jaeggi 2023 | 1.00 | 1 | Dominant target throughout the article: moralism, historicism, crisis, forms of life, progress, regression, and experience. |
| W30 Kuhn 1970 | 0.98 | 1 | Connects philosophy of science, social revolution, incommensurability, community choice, and Chen’s alternative. |
| W23 Jaeggi 2018a | 0.77 | 1 | Supplies forms of life, practical routines, interpretation, and know-how. |
| W24 Jaeggi 2018b | 0.75 | 1 | Connects moral progress, conceptual transformation, and formal accounts of progress. |
| W11 Dewey 1997 | 0.72 | 1 | Supplies the cumulative, educational model of experience that Chen later challenges. |
| W29 Kitcher 2021 | 0.70 | 1 | Supplies the distinction between “progress to” and “progress from.” |
| W01 Allen 2016 | 0.68 | 1 | Frames the concluding paradox of progress as fact versus imperative. |
| W41/W42 Searle | 0.64 | 1 each | Connect progress judgments to collective intentionality and constructed social facts. |

The chief bridge is Kuhn (1970): Chen says that “keywords such as problem-solving, paradigm shift, crisis, and revolution make the correlation between social and scientific progress plausible.”

---

### Authority works

Here “authority” means breadth of synthesis or conceptual leverage within Chen’s argument; external bibliography sizes are unavailable.

| Work | Authority score | References count | Synthesis quality |
|---|---:|---:|---|
| W26 Jaeggi 2023 | 1.00 | unavailable | high |
| W30 Kuhn 1970 | 0.98 | unavailable | high |
| W01 Allen 2016 | 0.78 | unavailable | high |
| W29 Kitcher 2021 | 0.76 | unavailable | high |
| W23 Jaeggi 2018a | 0.75 | unavailable | high |
| W11 Dewey 1997 | 0.72 | unavailable | high |
| W40 Roth 2012 | 0.65 | unavailable | medium |
| W16 Giddens 1991 | 0.63 | unavailable | medium |
| W41 Searle 1995 | 0.62 | unavailable | high |
| W33 Kuukkanen 2024 | 0.60 | unavailable | medium |

---

### Meta

```text
{
  "total_works": 46,
  "total_citations": 45,
  "average_citations_per_work": 0.978,
  "network_density": 0.0217,
  "most_cited_work": "W26",
  "citation_time_span": "1954–2024"
}
```

`most_cited_work` identifies the most frequently and centrally invoked work in the prose, not unique incoming degree; on incoming degree, all 45 references tie at one. The density is `45 / (46 × 45)` for a directed graph without self-loops.

---

## Findings ledger

- [F1] The citation network is organized around a direct dispute with Jaeggi rather than a neutral literature survey. — anchor: “I examine whether the arguments Jaeggi offers for her pragmatist theory of progress are valid.” — confidence: high

- [F2] Jaeggi (2023) is the dominant target work because it supplies the definitions of progress and regression repeatedly reconstructed across the article. — anchor: “progress is an accumulating process, while regression is a systematically blocked process” — confidence: high

- [F3] Chen presents Jaeggi’s theory as an alternative to both moralism and historicism. — anchor: “I reconstruct Jaeggi’s criticism of moralism and historicism.” — confidence: high

- [F4] Singer and Anderson represent the “expanding” moral-progress tradition rather than Chen’s own position. — anchor: “the expansion of the moral circle can be represented by the constant bias-correction” — confidence: high

- [F5] Honneth functions in two clusters: as a source for critical theory’s contemporary task and as an example of a potentially historicist “deepening” model. — anchor: “the deepening thesis has the potential to yield the outcomes of historicism” — confidence: high

- [F6] Kitcher supplies the immediate pragmatist vocabulary through the distinction between teleological and obstacle-removing progress. — anchor: “Pragmatic progress consists in solving problems and overcoming limitations.” — confidence: high

- [F7] Dewey is cited as the principal authority for construing experience as cumulative and open-ended. — anchor: “Experience is valuable only if is offers the possibility of further experiences in the future.” — confidence: high

- [F8] Chen treats Jaeggi’s “forms of life” as simultaneously material, institutional, interpretive, and normative. — anchor: “forms of life involve not only the functional significance of making social practices possible, but also the normative meaning” — confidence: high

- [F9] The pivotal citation bridge joins Jaeggi’s social theory to Kuhn’s philosophy of scientific revolutions. — anchor: “Jaeggi distinctly outlines a parallelism between forms of life and the scientific paradigm.” — confidence: high

- [F10] Kuhn (1970) is used critically against Jaeggi because incommensurability undermines cumulative experience across paradigm shifts. — anchor: “scientific progress cannot be regarded as an accumulative process” — confidence: high

- [F11] Chen argues that paradigm differences concern more than theories: they include methods, problems, evidence, and worldviews. — anchor: “The difference in paradigm means differences in methods, problems, standards of evidence, and world views.” — confidence: high

- [F12] Kuhn’s later account of know-how initially appears to rescue cumulative progress. — anchor: “if … we take a purely instrumental view of knowledge – then knowledge clearly does grow” — confidence: high

- [F13] Kuukkanen and Kuhn (1977) are used to show that know-how grows only within a scientific community organized around shared puzzle-solving commitments. — anchor: “an embodied skill distributed among the members of a scientific community” — confidence: high

- [F14] Chen’s decisive disanalogy is that societies lack the scientific community’s jointly shared principal goal. — anchor: “such a shared and jointly committed version of the principal goal is absent in social forms of life” — confidence: high

- [F15] The slavery example is used to show that opposed social groups may not merely propose different solutions but identify different problems. — anchor: “abolitionists view the very existence of a slavery system as a problem” — confidence: high

- [F16] Roth is cited as a rival pragmatist attempt to constrain genuine solutions, but Chen rejects both of Roth’s proposed tests. — anchor: “Unfortunately, both of the theses are flawed as pragmatist.” — confidence: high

- [F17] Giddens supplies counterexamples in which accepted progress can reduce or sequester practical experience. — anchor: “the separated time and space of childhood still impedes children’s experiences” — confidence: high

- [F18] Nazism and right-wing populism are deployed against Jaeggi’s equation of regression with blocked problem-recognition. — anchor: “right-wing populism is not simply ignorance of the crisis” — confidence: high

- [F19] Lakatos and Roth represent the standard objection that Kuhnian community choice collapses into irrational psychologism. — anchor: “falls totally within the realm of the (social) psychology of discovery” — confidence: high

- [F20] Chen reverses that objection, treating community-based psychology as Kuhn’s insight rather than his failure. — anchor: “taking the psychological elements of scientists into account is a rational attitude” — confidence: high

- [F21] Searle provides the mechanism for Chen’s positive alternative: judgments of progress help constitute intentionality-relative social facts. — anchor: “progressive movements exist because we intentionally count some social movements as progressive” — confidence: high

- [F22] Wellmer supports the claim that normative rightness cannot be reduced to a neutral truth criterion. — anchor: “the term ‘right’ would denote that which can justifiably be demanded” — confidence: high

- [F23] Allen supplies the article’s concluding meta-normative paradox between needing progress as an imperative and rejecting triumphalist history. — anchor: “our politics cannot be truly progressive unless we have some way of conceptualizing what would count as progress” — confidence: high

- [F24] Chen’s final position is nonteleological because collective agents’ intentions, rather than an objective historical end, determine judgments of progress. — anchor: “it relies entirely on the collective intention of social members” — confidence: high

- [F25] The proposed psychologist account is also pluralist because intentions and aspirations are multidimensional. — anchor: “our intentions, desires, and hopes for the better are multidimensional” — confidence: high

- [F26] Chen’s title formula means retaining practical pursuit of improvement while abandoning a general historical law or sufficient account of progress. — anchor: “we can freely pursue and look forward to progress without concluding any conception or historical outcome of progress” — confidence: high

---

### Counter-evidence

- Jaeggi herself recognizes that social problems are contested, which weakens any suggestion that she straightforwardly assimilates social inquiry to technical puzzle-solving. — anchor: “The existence and identification of problems will be as disputed as their respective solutions.”

- Jaeggi allows revolutionary replacement rather than only cumulative reform, so her theory already contains an element of discontinuity. — anchor: “only with a revolution (a radical paradigm shift)”

- Kuhn’s instrumental account permits at least one meaningful sense in which knowledge accumulates across revolutions. — anchor: “if … we mean knowing how … then knowledge clearly does grow”

- Chen concedes that psychologist judgment does not eliminate reasons or standards altogether. — anchor: “that does not mean that we do not have any reason or standard to make judgments”

- Chen’s claim that collective recognition creates progress may risk collapsing the distinction between widely accepted change and justified progress. The article acknowledges the danger indirectly through the possibility that “the psychological understanding of progress can favor populist movements.” — confidence: high

- The scientific/social analogy remains imperfect even in Chen’s alternative because scientific communities are specialized groups, whereas “social members” may be internally divided and may lack a determinate decision procedure. — anchor: “members of old and new forms of life can hardly share a similar consciousness of problems.” — confidence: medium

---

### Open questions

1. What threshold turns a group’s judgment into the “collective intention” that constitutes progress: majority acceptance, institutional authority, democratic legitimacy, or something else?

2. How can Chen condemn genocide if collective intentionality rather than an independent normative criterion makes a movement progressive? The article raises but does not fully settle this concern: “The psychological understanding of progress can favor populist movements.”

3. Does “psychologist” describe causal explanation, social ontology, or normative justification? Chen moves among all three when he discusses community decisions, intentionality-relative facts, and progress judgments.

4. Can opposed groups constitute different progress facts simultaneously? This possibility follows from the claim that “the consciousness of problems varies from group to group.”

5. Is Kuhnian incommensurability complete or partial? Chen often treats paradigms and forms of life as radically discontinuous, but the quoted Kuhnian account of shared values and evidence suggests overlap remains.

6. Are Jaeggi’s “experience enrichment” and Kuhn’s “know-how growth” genuinely equivalent? Chen connects them, but Jaeggi’s experience is ethical-social while Kuhn’s know-how is professional and puzzle-directed.

7. The external works’ own citation relations cannot be reconstructed from this document. A field-level assessment of hubs, authorities, and cluster density would require their bibliographies and incoming-citation data.

8. The article notes a disagreement between Laudan and Kuhn—“Laudan rejects Kuhn’s discontinuous version”—but does not systematically test whether Laudan’s theory could support Jaeggi better than Kuhn does.