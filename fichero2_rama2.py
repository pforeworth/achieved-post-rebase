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
        print("\nEjecutando tareas:\n cambio 3cambio 3")
        while self.queue:
            task = self.queue.popleft()
            print(f"→ {task.name} ({task.duration}s) cambio 3")
            time.sleep(task.duration)
            print(f"✓ {task.name} completada\n cambio 3")


def main() -> None:
    q = TaskQueue()
    q.add(Task("Descargar datos cambio 3", 1))
    q.add(Task("Procesar datos cambio 3", 2))
    q.add(Task("Generar reporte cambio 3", 1.5))
    q.run()


if __name__ == "__main__":
    main()
