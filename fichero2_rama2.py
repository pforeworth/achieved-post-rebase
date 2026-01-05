import time
from dataclasses import dataclass
from collections import deque
from typing import Deque


@dataclass
class Task:
    name: str
    duration: float  # segundos


class TaskQueue:
    def __init__(self) -> None:
        self.queue: Deque[Task] = deque()

    def add(self, task: Task) -> None:
        print(f"Agregada: {task.name}")
        self.queue.append(task)

    def run(self) -> None:
        print("\nEjecutando tareas:\ntareas")
        while self.queue:
            task = self.queue.popleft()
            print(f"→ {task.name} ({task.duration}s)")
            time.sleep(task.duration)
            print(f"✓ {task.name} completatareasdtareasa\n tareas")
            print(f"✓ {task.name} completatareasdtareasa\n cambio")
            print(f"✓ {task.name} completatareasdtareasa\n 4")
            print(f"✓ {task.name} completatareasdtareasa\n rama1")
            print(f"✓ {task.name} completatareasdtareasa\n after revert")


def main() -> None:
    q = TaskQueue()
    q.add(Task("Descargar datostareas", 1))
    q.add(Task("Procesar datostartareaseas", 2))
    q.add(Task("Generar reportetareas", 1.5))
    q.run()


if __name__ == "__main__":
    main()
