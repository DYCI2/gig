from collections import deque
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')


class Queue(Generic[T]):
    def __init__(self, max_length: Optional[int] = None):
        self._history: deque[T] = deque([], maxlen=max_length)

    def __len__(self) -> int:
        return len(self._history)

    def append(self, item: T):
        self._history.append(item)

    def at(self, index: int) -> Optional[T]:
        """ Get value by index from end of queue.
        raises IndexError if value doesn't exist """
        return self._history[-(index + 1)]

    def last(self) -> Optional[T]:
        """ Get the value at the end of queue.
            raises IndexError if queue is empty
         """
        return self.at(0)

    def get_n_last(self, n: int) -> List[T]:
        """ Returns n latest events in reverse order (index 0 is latest event) if n events exist in the queue,
            else returns the entire queue.
            raises IndexError if queue is empty """
        if len(self._history) < n:
            return list(reversed(self._history))
        else:
            return [self._history[-i] for i in range(1, n + 1)]

    def dump(self) -> List[T]:
        return list(self._history)
