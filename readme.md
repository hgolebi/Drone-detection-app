# System śledzący poruszające się obiekty 

Projekt polega na opracowaniu systemu detekcji i śledzenia dronów. Celem projektu jest stworzenie aplikacji webowej, która będzie w stanie wykryć i śledzić drony na podstawie nagrań wideo, a także umożliwi użytkownikom wstawienie własnych filmów do analizy.

W ramach projektu wykorzystujemy architekturę sieci neuronowych YOLO (You Only Look Once), która jest jedną z najbardziej popularnych metod detekcji obiektów w czasie rzeczywistym (szybka skuteczna w wykrywaniu obiektów). W naszym projekcie korzystamy z pre-trenowanych wag modelu YOLO, które zostały wytrenowane na dużym zbiorze danych COCO. Następnie przeprowadzamy dalsze treningi, aby model był w stanie wyspecjalizować się w wykrywaniu dronów.

Do treningu modelu wykorzystujemy zbiór nagrań wideo z dronami oraz odpowiadające im adnotacje (udostępnione przez właścicielkę tematu). Aby przygotować dane do treningu, musimy najpierw przetworzyć nagrania, aby uzyskać pojedyncze klatki. Adnotacje również potrzebują przerobienia, aby były w formacie kompatybilnym z modelem YOLO.

Gotowy model będzie działał jako aplikacja webowa, która umożliwi użytkownikom wstawienie swoich własnych filmów do analizy lub wybranie dostępnych nagrań z dronami. Aplikacja będzie w stanie na bieżąco przetwarzać wideo, wykrywać drony i śledzić ich ruch. Wynikiem analizy będzie wideo z zaznaczoną ramką śledzącą drona (które użytkonik będzie mógł pobrać) oraz adnotacje zawierające informacje o wykrytych dronach.

W aplikacji będzie również możliwość wyboru progu pewności, od którego chcemy, aby dron był zaznaczony ramką na filmie. Dzięki temu użytkownicy będą mogli dostosować wyniki detekcji do swoich potrzeb i wymagań.

W projekcie korzystamy z różnych metod śledzenia obiektów, takie jak:

•	metody bazujące na pokrywaniu się detekcji z określonym wskaźnikiem IoU, 

•	SORT lub DeepSORT,

•	wykrywanie dronów bazując na optycznym przepływie (optical flow) i identyfikacja wykrytych obiektów,

•	metody śledzenia obiektu po cechach i wzorcach poruszania się

Użytkownicy po wybraniu bądź wstawieniu filmu do detekcji będą mogli dokonać wyboru odnośnie tego, która metoda zostanie wykorzystana do śledzenia dronów. Dzięki temu mogą przetestować różne opcje oraz dostosować działanie programu do swoich potrzeb i wymagań.
