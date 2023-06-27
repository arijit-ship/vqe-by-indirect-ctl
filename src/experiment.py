from qulacs import QuantumCircuit
from qulacs.gate import Pauli

circuit = QuantumCircuit(3)
target_list = [0,1,2]
pauli_index = [0,1,1] # 1:X , 2:Y, 3:Z
m1 = Pauli(target_list, pauli_index).get_matrix() # = X_0 Z_3 X_5

target_list = [0,1,2]
pauli_index = [1,1,0]
m2 = Pauli(target_list, pauli_index).get_matrix()

target_list = [0,1,2]
pauli_index = [2,0,0]
m3 = Pauli(target_list, pauli_index).get_matrix()

target_list = [0,1,2]
pauli_index = [0,2,0]
m4 = Pauli(target_list, pauli_index).get_matrix()

target_list = [0,1,2]
pauli_index = [0,0,2]
m5 = Pauli(target_list, pauli_index).get_matrix()

print(m1 + m2 + m3 + m4 + m5)