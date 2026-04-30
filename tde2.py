# tde2_mefd.py
# Simulador generico de Maquinas de Estados Finitos Deterministicas (MEFD)
# Frank Coelho de Alcantara - TDE 2

from dataclasses import dataclass
from typing import Dict, Tuple, Set


@dataclass
class MEFD:
    """Maquina de Estados Finitos Deterministica: (Q, Sigma, delta, q0, F)."""
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
