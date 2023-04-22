Folder Trackers zawiera cztery klasy śledzące:
- Deepsort
- Sort
- OpenCV MultiTracker (CSRT, MEDIANFLOW, KCF)

Klasy te przyjmują listę wykrytych przez system detekcji obiektów. Za pomocą cech obiektu, jesteśmy w stanie śledzić ich trasę.

Trackery Deepsort oraz Sort przyjmują wykryte bounding boxy i zwracają przewidywaną trasę na podstawie wybranej metody odróżniania obiektów.
Tracker OpenCV przyjmuje bounding boxy do aktualizacji trackerów, jednak nie używa ich do śledzenia obiektów.

Każdy Tracker posiada zaimplementowaną metodę update, która po przekazaniu ramki w formacie xywh, stopnia pewności oraz klatki filmu zwraca uaktualnione wykrycie obiektu, a także jego id. Id jest konieczne w celu rozpoznania śledzonego obiektu i zakodowaniu tego na filmie.
