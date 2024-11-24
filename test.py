from microqiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import time
import math

NUM_QUBITS = 4

while True:
    qreg = QuantumRegister(NUM_QUBITS)
    creg = ClassicalRegister(NUM_QUBITS)

    circuit = QuantumCircuit(qreg, creg)
    circuit.h(0)
    for i in range(NUM_QUBITS - 1):
        circuit.cx(i, i + 1)
    circuit.measure(range(NUM_QUBITS), range(NUM_QUBITS))
    circuit.barrier()
    circuit.i(0)
    circuit.swap(1,2)
    circuit.barrier()
    circuit.rx(math.pi / 4, 0) 
    circuit.ry( math.pi / 2, 1)
    circuit.rz(math.pi,2)
    circuit.draw()
    circuit.execute()

    time.sleep(0.6)