"""Tests simples du projet final."""
from projet_final_solution import (
    alertes, indice_capteur, statistiques, tri_insertion_temperature
)

assert statistiques([2.0, 4.0, 6.0]) == (2.0, 6.0, 4.0)
assert indice_capteur([{"id": "C01"}, {"id": "C02"}], "C02") == 1
assert indice_capteur([{"id": "C01"}], "ABSENT") is None
assert len(alertes([{"statut": "OK"}, {"statut": "ALERTE"}])) == 1
triees = tri_insertion_temperature([
    {"temperature": 5.0}, {"temperature": -1.0}, {"temperature": 3.0}
])
assert [m["temperature"] for m in triees] == [-1.0, 3.0, 5.0]
print("Tous les tests passent.")
