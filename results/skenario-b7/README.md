# Skenario dataset B7 (25 Nov 2026)
Pembanding dua skenario: heiDATA + Essig vs Illinois + Essig. Dokumen utama: `docs/materi/SKENARIO-DATASET-B7.md`.

## illinois-metrics/
Bagian Illinois dievaluasi dengan metrik WO-15 yang sama dengan heiDATA dan Essig (`results/wo15-metrics/`).
- Perintah: `python -I src/wo15_metrics.py --config configs/skenario_illinois_metrics.yaml` (±20 menit di laptop, SVM paling lama).
- Data: lintasan intensitas penulis, sumur kontrol saja, maks. 20 sel/sumur (seed 42), 9 fitur sel sendiri (tanpa fitur *noise* yang bocor).
- Tugas: TNF vs tanpa perlakuan (positif = TNF), alsterpaullone vs tanpa perlakuan (positif = Alp).
- Skema: leave-one-plate-out (7 fold) dan k-fold 5 per sel; ambang bawaan dan recall ≥ 0,90 (dipilih di data latih).
- Keluaran: `metrics_full.json`, `summary_metrics.csv`, `confusion_matrices.png`.

Ringkasan (MCC tertinggi, ambang bawaan): TNF plate baru SVM AUC 0,874, recall 0,827, spesifisitas 0,762, MCC 0,563;
Alp plate baru RF AUC 0,950, recall 0,840, spesifisitas 0,912, MCC 0,750. Selisih plate baru vs k-fold ≤ 0,01.
