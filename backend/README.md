## API

- ``/video`` **GET** zwraca listę wgranych filmów jako lista w json
- ``/video/<name>`` **GET** zwraca film o podanej nazwie
- ``/thumbnail/<name>`` **GET** zwraca miniaturkę do filmu. **UWAGA** ``<name>`` musi zawierać pełną nazwę pliku wideo z rozszerzeniem
- ``/upload`` **POST** pozwala wysłać plik do serwera (obsługiwane rozszerzenia ``mp4``, ``mov``)