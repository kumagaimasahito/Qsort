from Qsort.Qsort import Qsort

def test_Qsort():
    qsort = Qsort()
    qsort.set_random_numbers()

    qubo = qsort.set_qubo()