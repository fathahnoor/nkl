# 🤝 Kontribusi Nusuk Keys List

Terima kasih sudah membantu menambah daftar! 🔑✨ Sertakan kode yang benar-benar terlihat di sumber publik, kapitalisasi asli, URL post, dan timestamp baca.

Format JSON untuk pull request (data di bawah hanya contoh, jangan dimasukkan ke paket pengguna):

```json
{
  "rows": [
    {
      "code": "NG-EXAMPLE1",
      "source": "https://example.com/public-post",
      "collectedAt": "2026-11-11T05:00:00+07:00"
    }
  ]
}
```

📂 Letakkan usulan di `contributions/` dengan nama file yang jelas. Maintainer memeriksa sumber serta duplikat sebelum mengintegrasikan ke batch. Jangan mengubah ID atau urutan kode pada batch yang sudah dirilis karena progres pengguna bergantung pada data tersebut.

🧰 Updater di `Kumpulan-Key/update_web_malam.py` merekam pengumpulan malam 10-11 November 2026 dengan plafon khusus 5.000 tambahan. Konfigurasi kampanye itu bukan batas permanen proyek. Baca `Kumpulan-Key/UPDATE-WEB.md` sebelum menggunakannya. CLI memakai penguncian berkas Windows.

🧪 Jalankan pemeriksaan dari root repo (Python 3.14 dan Node.js):

```powershell
python Kumpulan-Key/test_update_web_malam.py
```

🌐 Untuk menguji tampilan secara lokal:

```powershell
python -m http.server 8000 --directory Salin-Kode-Nusuk
```

Buka `http://localhost:8000`. GitHub Pages hanya memublikasikan folder `Salin-Kode-Nusuk/`. Arsip spreadsheet dan pengumpulan tetap tersedia di repo sebagai rujukan.

🔒 Jangan sertakan credential atau backup progres pribadi. Tidak perlu menguji redeem untuk mengusulkan kode, dan jangan menyatakan kode diterima tanpa bukti. 💚
