# Chatan YUK!
Tubes 3 Strategi Algoritma - Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant
#### A Web implementation Deadline Reminder Assistant

## Deskripsi Singkat Program
Aplikasi sederhana yang berfungsi untuk membantu mengingat berbagai deadline, tanggal penting, dan task-task tertentu kepada user yang menggunakannya.  Dengan memanfaatkan algoritma String Matching dan Regular Expression, dibuat sebuah chatbot interaktif sederhana layaknya Google Assistant yang akan menjawab segala pertanyaan Anda terkait informasi deadline tugas-tugas yang ada.

## Instalasi dan Requirements

### Instalasi
1. Install pyhton
```
Install python dari https://www.python.org/downloads/
```
2. Install library 
```
pip install regex
pip install flask
pip install flask_cors
pip install requests

jika ada method library nltk yang belum diunduh, ikuti petunjuk yang diberikan pada konsol
```
### Requirements 
#### File Requirements
```
1. Kata Penting

Kuis
Ujian
Tucil
Tubes
Praktikum
```
## Menjalankan Server
- menuju file directory src
```
cd src
```
- run server
```
python app.py
```
- kemudian akan muncul running applikasi lokal
``
Running on [http://127.0.0.1:5000/]([http://127.0.0.1:5000/) 
```
- atau bisa melalui pranala
```
[habibinaarif.pythonanywhere.com](habibinaarif.pythonanywhere.com)
```
- Buka link tersebut di browser dan program siap digunakan

## Cara penggunaan aplikasi
- Masukkan pesan sesuai perintah yang di inginkan, misalnya ingin menambahkan task
```

user : Tubes IF2211 String Matching pada 28 April 2021
chatbot : [TASK BERHASIL DICATAT] (ID:1) 28/04/2021-IF2211-Tubes-String Matching

```
## Interface Frontend
![ChatanYuk](https://github.com/hilalhmdy/tubes-3-stima/blob/main/img/ChatanYuk.png)
## Author
- [M. Hilal Alhamdy (13519024)](https://github.com/hilalhmdy)
- [Mohammad  Yahya Ibrahim (13519091)](https://github.com/ibrahimyahyaa)
- [Habibina Arif Muzayyan (13519125)](https://github.com/habibinaarif)
