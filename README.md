# **MicroQiskit**

**MicroQiskit** is a lightweight MicroPython single file library for simulating quantum circuits on microcontrollers. It is designed to be minimal, easy to understand, and simple to use. It supports basic quantum operations, measurements, and circuit visualization.

---

## **Features**
- **Qiskit like syntax**
- **Basic Gates**: Includes `H`, `X`, `CX`, `CZ`, and more.
- **Rotations**: Supports `RX`, `RY`, `RZ` operations with specified angles.
- **Measurements**: Simulate quantum measurements with classical registers.
- **Circuit Visualization**: Outputs a text-based diagram of the circuit over serial terminal.

---

## **Installation**

To start using **MicroQiskit**, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/salva00/microqiskit.git
   cd microqiskit
   ```

2. Copy the Python script to your development board (e.g., a compatible microcontroller):

   ```bash
   ampy --port [your board serial port] put microqiskit.py
   ```

3. Run the test file to verify functionality:

   ```bash
   ampy --port [your board serial port] run test.py
   ```

---

## **Usage Example**

Here is a basic example of code using **MicroQiskit**:

```python
from microqiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

NUM_QUBITS = 4

# Create a quantum circuit with 4 qubits and 4 classical bits
qreg = QuantumRegister(NUM_QUBITS)
creg = ClassicalRegister(NUM_QUBITS)
circuit = QuantumCircuit(qreg, creg)

circuit.h(0)
for i in range(NUM_QUBITS - 1):
  circuit.cx(i, i + 1)

# Perform a measurement
circuit.measure(range(NUM_QUBITS), range(NUM_QUBITS))
circuit.barrier()

# Visualize the circuit
circuit.draw()
circuit.execute()
```

This will produce output similar to:

```
q0_0:┤ H ├──■────────────────┤M├──────────────────────|────
q0_1:─────┤ X ├───■────────────────┤M├────────────────|────
q0_2:───────────┤ X ├───■────────────────┤M├──────────|────
q0_3:─────────────────┤ X ├────────────────────┤M├────|────
c0: 4/────────────────────────c0─────c1─────c2─────c3──────
Classical register: [1, 1, 1, 1]
```

---

## **Contributing**

Contributions to this project are welcome! To contribute:

1. Fork this repository.
2. Create a branch for your feature:
   ```bash
   git checkout -b feature/your-branch
   ```
3. Submit a pull request with a detailed description.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## **Contact**

For questions or bug reports, you can reach out to the project maintainer via [GitHub Issues](https://github.com/salva00/microqiskit/issues).

---
