# Riva API - Platform Backend Open Source untuk Bisnis Penjualan Sepak Bola

Selamat datang di Riva API, platform backend open source yang dirancang khusus untuk bisnis penjualan produk sepak bola. Riva API memberikan fleksibilitas kepada pengguna untuk memodifikasi dan mengintegrasikan aplikasi ini sesuai kebutuhan mereka. Apakah Anda ingin bergabung dalam bisnis penjualan sepak bola atau membuat situs web Anda sendiri dengan cepat, Riva API siap mendukung Anda.

## Fitur Utama
1. **Registrasi Jadi Penjual**<br> Bergabunglah dengan komunitas Riva dan daftarkan diri sebagai penjual produk sepak bola dengan mudah.
2. **Backend yang Dapat Dimodifikasi**<br> Riva API menggunakan Django sebagai backend-nya, dengan database PostgreSQL bawaan. Ini memungkinkan pengguna untuk melakukan modifikasi dan penyesuaian sesuai kebutuhan bisnis mereka.
3. **Pembuatan Situs Web Cepat**<br> Buat situs web Anda sendiri dengan mudah dengan hanya merancang tampilan frontend, sementara Riva API menyediakan infrastruktur backend yang kuat.

## Instalasi dan Konfigurasi
1. install dengan perintah : <br>

```sh
 $ git clone https://github.com/said-boy/Projects.git 
```

2. membuat virtual environment
```python
$ python3 -m venv venv
```

3. copy aplikasi backend
```sh
$ cp -r Projects/E-Commers\ -\ Riva\ Sport/Backend/. .
```

4. hapus yang tidak digunakan (opsional)
```sh
$ rm -rf Projects/
```

5. menjalankan virtual environment
```sh
$ source venv/bin/activate
```

6. masuk kedalam aplikasi
```sh
$ cd rest_api/
```
7. install dependensi
```python
$ pip install -r requirements.txt
```

8. setting database
   **pastikan anda sudah membuat database pada postgresql**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api', # ubah sesuai nama database anda
        'USER': 'postgres', # ubah sesuai password database anda
        'PASSWORD': 'postgres', # ubah sesuai password database anda
        'HOST': '127.0.0.1', 
        'PORT': '5432'
    }
}
```

9. migrasi database
```python
$ ./manage.py makemigrations
$ ./manage.py migrate
```

10. jalankan server
```python
$ ./manage.py runserver
```
11. instalasi selesai.

## Dokumentasi Penggunaan
Menggunakan Riva API: Pelajari cara menggunakan API ini dengan mengunjungi [dokumentasi penggunaan](http://localhost:9000/docs).

## Kontribusi
Kami sangat menghargai kontribusi dari komunitas. Jika Anda ingin berkontribusi pada proyek ini, silakan buka pull request atau lapor masalah (issue) di repositori kami.

## Lisensi
Riva API berlisensi di bawah lisensi open source yang memungkinkan pengguna untuk menggunakannya, mengubahnya, dan mendistribusikannya sesuai dengan persyaratan lisensi.

## Kontak
Jika Anda memiliki pertanyaan atau membutuhkan bantuan lebih lanjut, jangan ragu untuk menghubungi kami di alkhudrimsaid733@gmail.com.

### Selamat menggunakan Riva API, dan semoga sukses dalam bisnis penjualan sepak bola Anda atau dalam pembuatan situs web yang inovatif!
