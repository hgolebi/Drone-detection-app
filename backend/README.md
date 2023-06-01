## API

- ``/videos`` **GET** zwraca listę wgranych filmów jako lista w json
- ``/videos/<name>`` **GET** zwraca film o podanej nazwie
- ``/thumbnails/<name>`` **GET** zwraca miniaturkę do filmu. **UWAGA** ``<name>`` musi zawierać pełną nazwę pliku wideo z rozszerzeniem
- ``/videos`` **POST** pozwala wysłać plik do serwera (obsługiwane rozszerzenia ``mp4``, ``mov``)
- ``/processed_videos/<name>`` **GET** przetwarza film. Wamagane argumenty ``threshold``, ``tracker``
