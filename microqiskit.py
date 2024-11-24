import math
import random


class Complex:
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        else:
            return Complex(self.real * other, self.imag * other)

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def magnitude_squared(self):
        return self.real ** 2 + self.imag ** 2


class QuantumRegister:
    def __init__(self, size):
        self.size = size
        self.num_states = 1 << size
        self.state_vector = [Complex() for _ in range(self.num_states)]
        self.initialize_state()

    def initialize_state(self):
        for i in range(self.num_states):
            self.state_vector[i] = Complex(0, 0)
        self.state_vector[0] = Complex(1, 0)


class ClassicalRegister:
    def __init__(self, size):
        self.size = size
        self.values = [0] * size


class QuantumCircuit:
    def __init__(self, quantum_register, classical_register=None):
        self.qreg = quantum_register
        self.creg = classical_register
        self.num_qubits = quantum_register.size
        self.operations = []

    def execute(self):
        if self.creg:
            print(f"Classical register: {self.creg.values}")

    def h(self, qubit):
        self.operations.append({"type": "h", "qubit": qubit})
        sqrt_2_inv = 1 / math.sqrt(2)
        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                temp = self.qreg.state_vector[i]
                self.qreg.state_vector[i] = self.qreg.state_vector[i ^ (1 << qubit)] * sqrt_2_inv - temp * sqrt_2_inv
                self.qreg.state_vector[i ^ (1 << qubit)] = temp * sqrt_2_inv + self.qreg.state_vector[
                    i ^ (1 << qubit)] * sqrt_2_inv

    def x(self, qubit):
        self.operations.append({"type": "x", "qubit": qubit})
        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                self.qreg.state_vector[i], self.qreg.state_vector[i ^ (1 << qubit)] = (
                    self.qreg.state_vector[i ^ (1 << qubit)],
                    self.qreg.state_vector[i],
                )

    def cx(self, control, target):
        self.operations.append({"type": "cx", "control": control, "target": target})
        for i in range(self.qreg.num_states):
            if (i & (1 << control)) and not (i & (1 << target)):
                new_index = i ^ (1 << target)

                self.qreg.state_vector[i], self.qreg.state_vector[new_index] = (
                    self.qreg.state_vector[new_index],
                    self.qreg.state_vector[i],
                )

    def y(self, qubit):
        self.operations.append({"type": "y", "qubit": qubit})

        I = Complex(0, 1)
        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                temp = self.qreg.state_vector[i]
                self.qreg.state_vector[i] = self.qreg.state_vector[i ^ (1 << qubit)] * I
                self.qreg.state_vector[i ^ (1 << qubit)] = temp * Complex(0, -1)

    def z(self, qubit):
        self.operations.append({"type": "z", "qubit": qubit})

        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                self.qreg.state_vector[i] = self.qreg.state_vector[i] * Complex(-1, 0)

    def s(self, qubit):
        self.operations.append({"type": "s", "qubit": qubit})
        I = Complex(0, 1)
        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                self.qreg.state_vector[i] = self.qreg.state_vector[i] * I

    def t(self, qubit):
        self.operations.append({"type": "t", "qubit": qubit})

        sqrt_2_inv = 1 / math.sqrt(2)
        exp_pi_4 = Complex(sqrt_2_inv, sqrt_2_inv)
        for i in range(self.qreg.num_states):
            if i & (1 << qubit):
                self.qreg.state_vector[i] = self.qreg.state_vector[i] * exp_pi_4

    def swap(self, qubit1, qubit2):
        if qubit1 == qubit2:
            raise ValueError("You cannot swap a qubit with itself.")

        num_states = len(self.qreg.state_vector)
        for i in range(num_states):
            if ((i >> qubit1) & 1) != ((i >> qubit2) & 1):
                swapped_index = i ^ (1 << qubit1) ^ (1 << qubit2)
                self.qreg.state_vector[i], self.qreg.state_vector[swapped_index] = (
                    self.qreg.state_vector[swapped_index],
                    self.qreg.state_vector[i],
                )
        self.operations.append({"type": "swap", "qubits": (qubit1, qubit2)})

    def i(self, qubit):
        self.operations.append({"type": "i", "qubit": qubit})

    def cz(self, control, target):
        if control == target:
            raise ValueError("Control and target qubits must be different.")

        num_states = len(self.qreg.state_vector)
        for i in range(num_states):
            if ((i >> control) & 1) and ((i >> target) & 1):
                self.qreg.state_vector[i] = self.qreg.state_vector[i] * Complex(-1, 0)

        self.operations.append({"type": "cz", "control": control, "target": target})

    def barrier(self):
        self.operations.append({"type": "barrier"})

    def measure(self, qubits, classical_bits):
        if len(qubits) != len(classical_bits):
            raise ValueError("The number of qubits and classical bits must be the same.")

        for qubit, classical_bit in zip(qubits, classical_bits):
            probabilities = [
                state.magnitude_squared() for state in self.qreg.state_vector
            ]
            cumulative_prob = sum(probabilities)

            if cumulative_prob == 0:
                raise ValueError("Error: State vector is invalid (all probabilities are zero).")

            probabilities = [p / cumulative_prob for p in probabilities]
            random_value = random.random()

            measured_state = 0
            for i, prob in enumerate(probabilities):
                if random_value <= prob:
                    measured_state = i
                    break
                random_value -= prob

            result = (measured_state >> qubit) & 1

            for i in range(self.qreg.num_states):
                if ((i >> qubit) & 1) == result:
                    self.qreg.state_vector[i] = self.qreg.state_vector[i]
                else:
                    self.qreg.state_vector[i] = Complex(0, 0)

            self.creg.values[classical_bit] = result
            self.operations.append({"type": "measure", "qubit": qubit, "classical_bit": classical_bit})

    def rx(self, theta, qubit):
        cos = math.cos(theta / 2)
        isin = Complex(0, - math.sin(theta / 2))

        num_states = len(self.qreg.state_vector)
        for i in range(num_states):
            if (i >> qubit) & 1:
                opposite_index = i ^ (1 << qubit)
                a = self.qreg.state_vector[i]
                b = self.qreg.state_vector[opposite_index]
                self.qreg.state_vector[i] = a * cos + b * isin
                self.qreg.state_vector[opposite_index] = b * cos + a * isin

        self.operations.append({"type": "rx", "qubit": qubit, "theta": theta})

    def ry(self, theta, qubit):
        cos = math.cos(theta / 2)
        sin = math.sin(theta / 2)

        num_states = len(self.qreg.state_vector)
        for i in range(num_states):
            if (i >> qubit) & 1:
                opposite_index = i ^ (1 << qubit)
                a = self.qreg.state_vector[i]
                b = self.qreg.state_vector[opposite_index]
                self.qreg.state_vector[i] = a * cos - b * sin
                self.qreg.state_vector[opposite_index] = b * cos + a * sin

        self.operations.append({"type": "ry", "qubit": qubit, "theta": theta})

    def rz(self, theta, qubit):
        exp_pos = Complex(math.cos(theta / 2), math.sin(theta / 2))
        exp_neg = Complex(math.cos(theta / 2), -math.sin(theta / 2))

        num_states = len(self.qreg.state_vector)
        for i in range(num_states):
            if (i >> qubit) & 1:
                self.qreg.state_vector[i] *= exp_neg
            else:
                self.qreg.state_vector[i] *= exp_pos

        self.operations.append({"type": "rz", "qubit": qubit, "theta": theta})

    def draw(self):

        num_qubits = self.qreg.size
        max_operations = len(self.operations)
        diagram_width = max_operations * 10 + 1

        circuit_diagram = [["─" for _ in range(diagram_width)] for _ in range(num_qubits + 1)]

        for i in range(num_qubits):
            circuit_diagram[i][0:5] = list(f"q0_{i}:")
        circuit_diagram[num_qubits][0:5] = list(f"c0: {self.creg.size}/")

        position = 6  # position padding for qubit labels
        for op in self.operations:
            if op["type"] == "h":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + 5] = list("┤ H ├")
            elif op["type"] == "cx":
                control = op["control"]
                target = op["target"]
                circuit_diagram[control][position] = "■"
                circuit_diagram[target][position - 2:position + 4] = list("┤ X ├")
                for i in range(min(control, target) + 1, max(control, target)):
                    circuit_diagram[i][position] = "│"
            elif op["type"] == "cz":
                control = op["control"]
                target = op["target"]
                circuit_diagram[control][position] = "■"
                circuit_diagram[target][position - 2:position + 4] = list("┤ Z ├")
                for i in range(min(control, target) + 1, max(control, target)):
                    circuit_diagram[i][position] = "│"
            elif op["type"] == "barrier":
                for i in range(num_qubits):
                    circuit_diagram[i][position] = "|"
            elif op["type"] == "x":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + len("┤ X ├") - 2] = list("┤ X ├")
            elif op["type"] == "y":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + len("┤ Y ├") - 2] = list("┤ Y ├")
            elif op["type"] == "z":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + len("┤ Z ├") - 2] = list("┤ Z ├")
            elif op["type"] == "s":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + len("┤ S ├") - 2] = list("┤ S ├")
            elif op["type"] == "t":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + len("┤ T ├") - 2] = list("┤ T ├")
            elif op["type"] == "i":
                qubit = op["qubit"]
                circuit_diagram[qubit][position - 1:position + 5] = list("┤ I ├")
            elif op["type"] == "swap":
                qubit1, qubit2 = op["qubits"]
                circuit_diagram[qubit1][position] = "×"
                circuit_diagram[qubit2][position] = "×"
                for i in range(min(qubit1, qubit2) + 1, max(qubit1, qubit2)):
                    circuit_diagram[i][position] = "│"
            elif op["type"] in ["rx", "ry", "rz"]:
                qubit = op["qubit"]
                theta = op["theta"]
                gate_representation = f"┤ {op['type'].upper()}({round(theta, 2)}) ├"
                circuit_diagram[qubit][position - 1:position + len(gate_representation) - 2] = list(gate_representation)
            elif op["type"] == "measure":
                qubit = op["qubit"]
                classical_bit = op["classical_bit"]
                circuit_diagram[qubit][position - 1:position + 5] = list("┤M├")
                circuit_diagram[num_qubits][position] = f"c{classical_bit}"
            position += 6

        for line in circuit_diagram:
            print("".join(line).rstrip())