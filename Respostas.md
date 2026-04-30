# TDE 2 — Máquinas de Estado Finito e Gramáticas

**Disciplina:** Linguagens Formais e Autômatos
**Professor:** Frank Coelho de Alcantara

---

## Questão 1 — Diagramas de Transição (MEFD)

Para cada linguagem $L_i \subseteq \{0,1\}^*$ é apresentada uma Máquina de Estados Finitos Determinística (MEFD) na forma de quíntupla $M = (Q, \Sigma, \delta, q_0, F)$ e o respectivo diagrama de transição (imagens `Maquina N.png` no diretório do trabalho).

> Convenção dos diagramas: o estado inicial é apontado por uma seta de entrada; estados de aceitação são desenhados como círculos duplos. Quando necessário, foi acrescentado um estado de "armadilha" (*trap state*) `qd` para garantir o determinismo total (uma transição definida para cada símbolo em cada estado).

---

### a) MEFD-0 — $L_0 = \{x \in \{0,1\}^* \mid \text{cada } 0 \text{ em } x \text{ é seguido por pelo menos um } 1\}$

Intuição: nunca pode terminar em `0` e não pode haver `00`. Após ler um `0` é obrigatório ler um `1` antes de aceitar.

- $Q = \{q_0, q_1, q_d\}$
- $\Sigma = \{0,1\}$
- $q_0$ inicial; $F = \{q_0\}$
- $\delta$:
  - $\delta(q_0, 1) = q_0$ — continua em estado de aceitação
  - $\delta(q_0, 0) = q_1$ — leu um `0`, precisa de `1`
  - $\delta(q_1, 1) = q_0$ — `0` foi seguido de `1`, ok
  - $\delta(q_1, 0) = q_d$ — apareceu `00`, rejeita
  - $\delta(q_d, 0) = \delta(q_d, 1) = q_d$

![Diagrama MEFD-0](Maquina%200.png)

---

### b) MEFD-1 — $L_1 = \{x \in \{0,1\}^* \mid x \text{ termina com } 00\}$

- $Q = \{q_0, q_1, q_2\}$, $q_0$ inicial, $F = \{q_2\}$
- $\delta$:
  - $\delta(q_0, 0) = q_1$, $\delta(q_0, 1) = q_0$
  - $\delta(q_1, 0) = q_2$, $\delta(q_1, 1) = q_0$
  - $\delta(q_2, 0) = q_2$, $\delta(q_2, 1) = q_0$

![Diagrama MEFD-1](Maquina%201.png)

---

### c) MEFD-2 — $L_2 = \{x \in \{0,1\}^* \mid x \text{ contém exatamente 3 zeros}\}$

Conta-se a quantidade de `0` lidos. Se passar de 3 → estado armadilha.

- $Q = \{q_0, q_1, q_2, q_3, q_d\}$, $q_0$ inicial, $F = \{q_3\}$
- $\delta(q_i, 1) = q_i$ para $i \in \{0,1,2,3\}$
- $\delta(q_i, 0) = q_{i+1}$ para $i \in \{0,1,2\}$
- $\delta(q_3, 0) = q_d$; $\delta(q_d, 0) = \delta(q_d, 1) = q_d$

![Diagrama MEFD-2](Maquina%202.png)

---

### d) MEFD-3 — $L_3 = \{x \in \{0,1\}^* \mid x \text{ inicia com } 1\}$

Observação: como exige *iniciar* com 1, a palavra vazia $\varepsilon$ **não** pertence a $L_3$.

- $Q = \{q_0, q_1, q_d\}$, $q_0$ inicial, $F = \{q_1\}$
- $\delta(q_0, 1) = q_1$, $\delta(q_0, 0) = q_d$
- $\delta(q_1, 0) = \delta(q_1, 1) = q_1$
- $\delta(q_d, 0) = \delta(q_d, 1) = q_d$

![Diagrama MEFD-3](Maquina%203.png)

---

### e) MEFD-4 — $L_4 = \{x \in \{0,1\}^* \mid x \text{ não começa com } 1\}$

Aceita $\varepsilon$ e qualquer cadeia que comece com `0`.

- $Q = \{q_0, q_1, q_d\}$, $q_0$ inicial, $F = \{q_0, q_1\}$
- $\delta(q_0, 0) = q_1$, $\delta(q_0, 1) = q_d$
- $\delta(q_1, 0) = \delta(q_1, 1) = q_1$
- $\delta(q_d, 0) = \delta(q_d, 1) = q_d$

![Diagrama MEFD-4](Maquina%204.png)

---

## Questão 2 — Simulador em Python

A implementação a seguir simula **a máquina** (e não um algoritmo equivalente). Cada autômato é descrito como uma quíntupla $(Q, \Sigma, \delta, q_0, F)$ usando um dicionário e a função `simular` apenas executa a função de transição $\delta$ a cada símbolo lido — exatamente o comportamento de uma MEFD.

```python
# tde2_mefd.py
# Simulador genérico de Máquinas de Estados Finitos Determinísticas (MEFD)
# Frank Coelho de Alcantara - TDE 2

from dataclasses import dataclass
from typing import Dict, Tuple, Set, Iterable


@dataclass
class MEFD:
    """Máquina de Estados Finitos Determinística: (Q, Sigma, delta, q0, F)."""
    Q: Set[str]
    Sigma: Set[str]
    delta: Dict[Tuple[str, str], str]
    q0: str
    F: Set[str]

    def simular(self, cadeia: str, verbose: bool = False) -> bool:
        estado = self.q0
        if verbose:
            print(f"  inicio: {estado}")
        for i, simbolo in enumerate(cadeia):
            if simbolo not in self.Sigma:
                if verbose:
                    print(f"  simbolo invalido '{simbolo}' -> rejeita")
                return False
            chave = (estado, simbolo)
            if chave not in self.delta:
                if verbose:
                    print(f"  sem transicao para {chave} -> rejeita")
                return False
            proximo = self.delta[chave]
            if verbose:
                print(f"  passo {i+1}: {estado} --{simbolo}--> {proximo}")
            estado = proximo
        aceita = estado in self.F
        if verbose:
            print(f"  estado final: {estado} -> {'ACEITA' if aceita else 'REJEITA'}")
        return aceita


# ---------------------------------------------------------------------------
# Definicao das cinco maquinas pedidas no enunciado
# ---------------------------------------------------------------------------

SIGMA = {"0", "1"}

# (a) L0: cada 0 e seguido por pelo menos um 1
MEFD_0 = MEFD(
    Q={"q0", "q1", "qd"},
    Sigma=SIGMA,
    delta={
        ("q0", "1"): "q0",
        ("q0", "0"): "q1",
        ("q1", "1"): "q0",
        ("q1", "0"): "qd",
        ("qd", "0"): "qd",
        ("qd", "1"): "qd",
    },
    q0="q0",
    F={"q0"},
)

# (b) L1: termina com 00
MEFD_1 = MEFD(
    Q={"q0", "q1", "q2"},
    Sigma=SIGMA,
    delta={
        ("q0", "0"): "q1", ("q0", "1"): "q0",
        ("q1", "0"): "q2", ("q1", "1"): "q0",
        ("q2", "0"): "q2", ("q2", "1"): "q0",
    },
    q0="q0",
    F={"q2"},
)

# (c) L2: contem exatamente 3 zeros
MEFD_2 = MEFD(
    Q={"q0", "q1", "q2", "q3", "qd"},
    Sigma=SIGMA,
    delta={
        ("q0", "1"): "q0", ("q0", "0"): "q1",
        ("q1", "1"): "q1", ("q1", "0"): "q2",
        ("q2", "1"): "q2", ("q2", "0"): "q3",
        ("q3", "1"): "q3", ("q3", "0"): "qd",
        ("qd", "0"): "qd", ("qd", "1"): "qd",
    },
    q0="q0",
    F={"q3"},
)

# (d) L3: inicia com 1
MEFD_3 = MEFD(
    Q={"q0", "q1", "qd"},
    Sigma=SIGMA,
    delta={
        ("q0", "1"): "q1", ("q0", "0"): "qd",
        ("q1", "0"): "q1", ("q1", "1"): "q1",
        ("qd", "0"): "qd", ("qd", "1"): "qd",
    },
    q0="q0",
    F={"q1"},
)

# (e) L4: NAO comeca com 1 (aceita epsilon e qualquer cadeia iniciada por 0)
MEFD_4 = MEFD(
    Q={"q0", "q1", "qd"},
    Sigma=SIGMA,
    delta={
        ("q0", "0"): "q1", ("q0", "1"): "qd",
        ("q1", "0"): "q1", ("q1", "1"): "q1",
        ("qd", "0"): "qd", ("qd", "1"): "qd",
    },
    q0="q0",
    F={"q0", "q1"},
)


MAQUINAS = {
    "MEFD-0 (L0)": (MEFD_0, ["", "1111", "010111", "01110111011", "00", "10", "0"]),
    "MEFD-1 (L1)": (MEFD_1, ["00", "100", "1100", "0", "001", "", "11000"]),
    "MEFD-2 (L2)": (MEFD_2, ["000", "1010101", "0001110", "00", "0000", "", "1000010"]),
    "MEFD-3 (L3)": (MEFD_3, ["1", "10", "1010", "01", "0", "", "111"]),
    "MEFD-4 (L4)": (MEFD_4, ["", "0", "010", "0111", "1", "10", "0000"]),
}


def main() -> None:
    for nome, (maquina, testes) in MAQUINAS.items():
        print(f"\n=== {nome} ===")
        for w in testes:
            mostrado = w if w else "(vazia)"
            res = maquina.simular(w)
            print(f"  '{mostrado}' -> {'ACEITA' if res else 'REJEITA'}")


if __name__ == "__main__":
    main()
```

### Saída esperada (resumo)

```
=== MEFD-0 (L0) ===
  '(vazia)'      -> ACEITA
  '1111'         -> ACEITA
  '010111'       -> ACEITA
  '01110111011'  -> ACEITA
  '00'           -> REJEITA
  '10'           -> REJEITA
  '0'            -> REJEITA

=== MEFD-1 (L1) ===
  '00'    -> ACEITA
  '100'   -> ACEITA
  '1100'  -> ACEITA
  '0'     -> REJEITA
  '001'   -> REJEITA
  ''      -> REJEITA
  '11000' -> ACEITA

=== MEFD-2 (L2) ===
  '000'      -> ACEITA
  '1010101'  -> ACEITA   # tem exatamente 3 zeros
  '0001110'  -> REJEITA  # tem 4 zeros
  '00'       -> REJEITA
  '0000'     -> REJEITA
  ''         -> REJEITA
  '1000010'  -> REJEITA  # tem 5 zeros

=== MEFD-3 (L3) ===
  '1'   -> ACEITA
  '10'  -> ACEITA
  '1010'-> ACEITA
  '01'  -> REJEITA
  '0'   -> REJEITA
  ''    -> REJEITA
  '111' -> ACEITA

=== MEFD-4 (L4) ===
  ''     -> ACEITA
  '0'    -> ACEITA
  '010'  -> ACEITA
  '0111' -> ACEITA
  '1'    -> REJEITA
  '10'   -> REJEITA
  '0000' -> ACEITA
```

> Observação: o núcleo do simulador é a função `simular`, que apenas aplica $\delta(q, a)$ enquanto há símbolos. Isso caracteriza uma simulação **da máquina** — não um programa que reconheça a linguagem por outros meios (como expressões regulares ou contagens em alto nível).

---

## Questão 3 — Hierarquia de Chomsky

Em 1956, **Noam Chomsky** classificou as gramáticas formais (e, por consequência, as linguagens que elas geram e as máquinas que as reconhecem) em quatro níveis encaixados, conhecidos como **Hierarquia de Chomsky**. Cada nível é mais expressivo que o anterior, mas paga esse poder com mais restrições computacionais para o reconhecimento.

Uma **gramática** é uma quádrupla $G = (V, \Sigma, P, S)$ onde:

- $V$ — conjunto de símbolos **não terminais** (variáveis);
- $\Sigma$ — conjunto de símbolos **terminais**, $V \cap \Sigma = \emptyset$;
- $P$ — conjunto de **regras de produção** da forma $\alpha \to \beta$;
- $S \in V$ — **símbolo inicial**.

A diferença entre os tipos da hierarquia está exatamente no formato permitido em $\alpha$ e $\beta$ nas regras de $P$.

| Tipo | Nome | Linguagem gerada | Reconhecida por |
|:---:|---|---|---|
| 0 | Irrestrita / Recursivamente Enumerável | RE | Máquina de Turing |
| 1 | Sensível ao contexto | CSL | Autômato Linearmente Limitado |
| 2 | Livre de contexto | CFL | Autômato com Pilha (PDA) |
| 3 | Regular | REG | Autômato Finito (AFD/AFN) |

A inclusão é **estrita**: $\text{REG} \subsetneq \text{CFL} \subsetneq \text{CSL} \subsetneq \text{RE}$.

---

### Tipo 0 — Gramáticas Irrestritas (Recursivamente Enumeráveis)

**Forma das regras:** $\alpha \to \beta$ com $\alpha \in (V \cup \Sigma)^* V (V \cup \Sigma)^*$ e $\beta \in (V \cup \Sigma)^*$.
Ou seja, $\alpha$ pode ser qualquer cadeia desde que contenha pelo menos um não terminal; $\beta$ pode ser qualquer cadeia, **inclusive vazia** ($\varepsilon$).

**Limitação:** praticamente nenhuma sobre o formato; o problema da pertinência é, em geral, **indecidível**.

**Exemplo prático** — gera $L = \{a^n b^n c^n \mid n \ge 1\}$ (mesmo padrão usado em provas de não-livre-de-contexto):

```
S  -> a S B C | a B C
C B -> H B
H B -> H C
H C -> B C
a B -> a b
b B -> b b
b C -> b c
c C -> c c
```

Note a regra `C B -> H B`: o lado esquerdo possui dois símbolos e o direito também — algo proibido nos níveis inferiores.

---

### Tipo 1 — Gramáticas Sensíveis ao Contexto

**Forma das regras:** $\alpha A \beta \to \alpha \gamma \beta$, com $A \in V$, $\alpha, \beta \in (V \cup \Sigma)^*$ e $\gamma \in (V \cup \Sigma)^+$ (não vazio). De modo equivalente, exige-se $|\alpha| \le |\beta|$ em toda regra $\alpha \to \beta$ — as derivações **não encurtam**. A única exceção permitida é $S \to \varepsilon$, desde que $S$ não apareça do lado direito de nenhuma regra.

**Limitação:** o lado direito não pode ser menor que o lado esquerdo; substituir $A$ depende do "contexto" $\alpha$ e $\beta$ ao redor.

**Exemplo prático** — também $L = \{a^n b^n c^n \mid n \ge 1\}$, mas agora respeitando o não encurtamento:

```
S       -> a S B C | a B C
C B     -> C Z       (no contexto onde C antecede B)
C Z     -> W Z
W Z     -> W C
W C     -> B C
a B     -> a b
b B     -> b b
b C     -> b c
c C     -> c c
```

Toda regra tem $|\text{esq}| \le |\text{dir}|$.

---

### Tipo 2 — Gramáticas Livres de Contexto (CFG)

**Forma das regras:** $A \to \gamma$, onde $A \in V$ (**um único** não terminal do lado esquerdo) e $\gamma \in (V \cup \Sigma)^*$ (qualquer cadeia, inclusive $\varepsilon$).

**Limitação:** o lado esquerdo é restrito a **um** não terminal — a substituição independe do contexto em que $A$ aparece. É a base da maioria das sintaxes de linguagens de programação (BNF).

**Exemplo prático** — parênteses balanceados $L = \{w \in \{(,)\}^* \mid w \text{ está balanceado}\}$:

```
S -> ( S ) S | ε
```

Outro exemplo clássico — expressões aritméticas:

```
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
```

---

### Tipo 3 — Gramáticas Regulares

**Forma das regras** (gramática **linear à direita**): $A \to a B$, $A \to a$ ou $A \to \varepsilon$, com $A, B \in V$ e $a \in \Sigma$.
Equivalentemente, podem ser **lineares à esquerda** ($A \to B a$, $A \to a$, $A \to \varepsilon$). **Não se pode misturar** as duas formas na mesma gramática.

**Limitação:** só **um** terminal por regra e, no máximo, **um** não terminal — sempre na mesma extremidade. Por isso são equivalentes a **autômatos finitos** e **expressões regulares**.

**Exemplo prático** — a linguagem $L_1$ da Questão 1 (cadeias sobre $\{0,1\}$ que terminam em `00`):

```
S -> 0 S | 1 S | 0 A
A -> 0 B
B -> ε
```

Outro exemplo — identificadores simples (uma letra seguida de letras ou dígitos):

```
S -> l A
A -> l A | d A | ε
```

onde `l` representa uma letra e `d` um dígito.

---

### Resumo das restrições de produção

| Tipo | Lado esquerdo | Lado direito | Pode encurtar? |
|:---:|---|---|:---:|
| 0 | qualquer cadeia contendo ao menos um não terminal | qualquer cadeia (inclusive $\varepsilon$) | sim |
| 1 | qualquer cadeia contendo ao menos um não terminal | $\|\text{dir}\| \ge \|\text{esq}\|$ (exceto $S \to \varepsilon$) | não |
| 2 | **exatamente um** não terminal | qualquer cadeia | sim |
| 3 | **exatamente um** não terminal | um terminal, opcionalmente seguido (ou precedido) de **um** não terminal; ou $\varepsilon$ | sim |

A cada nível que se desce na hierarquia, mais restrita fica a forma das regras — e mais simples (e decidível) se torna o problema de reconhecimento.
